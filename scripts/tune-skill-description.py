"""Tune a skill's description (the text that decides when an agent opens the skill) with local models only.

How it measures: for each test request, a local model sees a list of skills (the one being tuned among near-miss
alternatives from this library) and picks the one it would open, or none. A description scores by how often that
pick is right: the skill for requests marked should_trigger, anything else for the rest. Each request runs --runs
times so one lucky or unlucky sample doesn't decide it.

How it improves: the requests are split 60/40 into train and test. After scoring, the local model reads the train
misses and proposes a better description; this repeats for --iterations rounds. The best description is chosen by
its score on all requests (ties go to the test score, then the earlier round), and the starting description wins
unless a rewrite actually beats it.

The model is any OpenAI-compatible server (ModelMistress, llama-server, Ollama's /v1). Standard library only.

  python scripts/tune-skill-description.py --skill skills/claude-router --evals trigger-eval.json \
      --url http://100.101.98.77:7871 --key-env SMN_MM_SHIVATI_KEY --model Qwen3.8-27B-UD-Q5_K_XL --out report.json
"""
from __future__ import annotations

import argparse
import json
import os
import random
import re
import sys
import time
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / "skills" / "skill-library" / "catalog.jsonl"
WORD = re.compile(r"[a-z0-9]+")
STOP = set("a an and are as at be by can for from has have how i if in is it its me my of on or our so that the "
           "this to was we what when which with you your do does please need want just like".split())

# Skills an agent commonly has alongside this library: near misses for delegation, scheduling and settings.
COMMON = [
    ("schedule", "Create, update, list, or run scheduled cloud agents (routines) that execute on a cron schedule."),
    ("loop", "Run a prompt or slash command on a recurring interval, or poll for status repeatedly."),
    ("update-config", "Configure the agent harness via settings.json: hooks, permissions, environment variables."),
    ("code-review", "Review the current diff or a pull request for correctness bugs."),
    ("simplify", "Review changed code for reuse, simplification and efficiency, then apply the fixes."),
    ("deep-research", "Research a topic across many sources and synthesize a narrative report."),
    ("claude-api", "Reference for the Claude API: model ids, pricing, parameters, streaming, tool use, caching."),
    ("skill-library", "Searches a library of 10,000+ specialised skills and loads the one that fits."),
]


def words(text: str) -> set[str]:
    return {w for w in WORD.findall(text.lower()) if w not in STOP and len(w) > 2}


def frontmatter(skill_md: Path) -> tuple[str, str, str]:
    text = skill_md.read_text(encoding="utf-8")
    m = re.match(r"---\r?\n(.*?)\r?\n---", text, re.S)
    name = re.search(r"^name:\s*(.+)$", m.group(1), re.M).group(1).strip()
    desc = re.search(r"^description:\s*(.+)$", m.group(1), re.M).group(1).strip()
    return name, desc, text


def distractors(name: str, evals: list[dict], n: int, seed: int) -> list[tuple[str, str]]:
    """Library skills whose descriptions share the most words with the requests, plus a few random ones."""
    cat = [json.loads(line) for line in CATALOG.read_text(encoding="utf-8").splitlines() if line.strip()]
    cat = [c for c in cat if c["name"] != name and c["description"]]
    query_words = words(" ".join(e["query"] for e in evals))
    ranked = sorted(cat, key=lambda c: -len(words(c["name"] + " " + c["description"]) & query_words))
    rng = random.Random(seed)
    picked = ranked[: n * 2 // 3] + rng.sample(ranked[n * 2 // 3:], n - n * 2 // 3)
    common = [(k, v) for k, v in COMMON if k != name]
    return common + [(c["name"], c["description"]) for c in picked]


class Model:
    def __init__(self, url: str, key: str, model: str, timeout: float = 300) -> None:
        self.url, self.key, self.model, self.timeout = url.rstrip("/"), key, model, timeout

    def chat(self, system: str, user: str, schema: dict, temperature: float, max_tokens: int = 400) -> dict:
        body = {"model": self.model, "temperature": temperature, "max_tokens": max_tokens,
                "messages": [{"role": "system", "content": system}, {"role": "user", "content": user + "\n/no_think"}],
                "response_format": {"type": "json_schema", "json_schema": {"name": "answer", "schema": schema, "strict": True}}}
        req = urllib.request.Request(self.url + "/v1/chat/completions", data=json.dumps(body).encode(),
                                     headers={"Content-Type": "application/json", "Authorization": f"Bearer {self.key}"})
        for attempt in range(4):
            try:
                with urllib.request.urlopen(req, timeout=self.timeout) as r:
                    text = json.loads(r.read())["choices"][0]["message"]["content"] or ""
                text = re.sub(r"<think>.*?</think>", "", text, flags=re.S).strip()
                return json.loads(text[text.find("{"): text.rfind("}") + 1])
            except Exception as exc:  # noqa: BLE001 - a busy or loading server is retried
                if attempt == 3:
                    raise RuntimeError(f"model call failed: {exc}") from None
                time.sleep(5 * (attempt + 1))
        return {}


PICK_SYSTEM = (
    "You are an AI coding agent. You can open one of the skills below before acting, when it would genuinely help "
    "with the user's request. Open a skill only when its description covers what the request needs; for simple "
    "requests you can do directly, or requests no skill covers, open none. Answer with the skill's name or \"none\".")


def pick(model: Model, skills: list[tuple[str, str]], query: str, temperature: float) -> str:
    listing = "\n".join(f"- {n}: {d}" for n, d in skills)
    names = [n for n, _ in skills] + ["none"]
    schema = {"type": "object", "properties": {"skill": {"type": "string", "enum": names}}, "required": ["skill"],
              "additionalProperties": False}
    out = model.chat(PICK_SYSTEM, f"Available skills:\n{listing}\n\nUser request:\n{query}", schema, temperature, 60)
    return str(out.get("skill", "none"))


def score(model: Model, name: str, desc: str, others: list[tuple[str, str]], items: list[dict], runs: int,
          temperature: float, workers: int, seed: int) -> dict:
    jobs = []
    for i, item in enumerate(items):
        for r in range(runs):
            rng = random.Random(seed * 1000 + i * 10 + r)
            skills = others + [(name, desc)]
            rng.shuffle(skills)                   # position must not decide the pick
            jobs.append((i, skills, item["query"]))
    with ThreadPoolExecutor(workers) as pool:
        picks = list(pool.map(lambda j: (j[0], pick(model, j[1], j[2], temperature)), jobs))
    per = []
    for i, item in enumerate(items):
        got = [p for k, p in picks if k == i]
        rate = sum(p == name for p in got) / len(got)
        ok = rate >= 0.5 if item["should_trigger"] else rate < 0.5
        per.append({"query": item["query"], "should_trigger": item["should_trigger"], "trigger_rate": round(rate, 2),
                    "passed": ok, "picks": got})
    return {"accuracy": round(sum(p["passed"] for p in per) / len(per), 3), "items": per}


PROPOSE_SYSTEM = (
    "You improve the description of an AI agent skill. The description is the only thing an agent reads when "
    "deciding whether to open the skill, so it must say what the skill does and exactly when to use it, including "
    "requests that need it without naming it, and it must not attract requests it doesn't serve. Write in plain "
    "prose, at most 900 characters, no markdown, no line breaks.")


def propose(model: Model, name: str, desc: str, body: str, misses: list[dict], history: list[dict]) -> str:
    missed = "\n".join(f"- {'SHOULD have opened it' if m['should_trigger'] else 'should NOT have opened it'} "
                       f"(opened {m['trigger_rate']:.0%} of the time): {m['query']}" for m in misses)
    tried = "\n".join(f"- train accuracy {h['train']['accuracy']:.0%}: {h['description']}" for h in history)
    user = (f"Skill name: {name}\n\nWhat the skill contains (first part):\n{body[:3500]}\n\n"
            f"Descriptions tried so far:\n{tried}\n\nCurrent description:\n{desc}\n\n"
            f"Requests it got wrong:\n{missed}\n\nWrite a better description that fixes these misses without "
            "breaking what already works. Generalise from the misses; don't list the requests.")
    schema = {"type": "object", "properties": {"description": {"type": "string"}}, "required": ["description"],
              "additionalProperties": False}
    out = model.chat(PROPOSE_SYSTEM, user, schema, 0.7, 700)
    return " ".join(str(out.get("description", desc)).split())[:1024]


def main() -> int:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--skill", type=Path, required=True, help="the skill's folder (with SKILL.md)")
    ap.add_argument("--evals", type=Path, required=True, help='JSON list of {"query", "should_trigger"}')
    ap.add_argument("--url", required=True)
    ap.add_argument("--key-env", default="", help="environment variable holding the server's key, if any")
    ap.add_argument("--model", required=True)
    ap.add_argument("--iterations", type=int, default=5)
    ap.add_argument("--runs", type=int, default=3)
    ap.add_argument("--temperature", type=float, default=0.6)
    ap.add_argument("--distractors", type=int, default=24)
    ap.add_argument("--workers", type=int, default=2)
    ap.add_argument("--seed", type=int, default=7)
    ap.add_argument("--out", type=Path, default=Path("tune-report.json"))
    a = ap.parse_args()

    name, desc, body = frontmatter(a.skill / "SKILL.md")
    evals = json.loads(a.evals.read_text(encoding="utf-8"))
    rng = random.Random(a.seed)
    pos = [e for e in evals if e["should_trigger"]]
    neg = [e for e in evals if not e["should_trigger"]]
    rng.shuffle(pos), rng.shuffle(neg)
    cut_p, cut_n = round(len(pos) * 0.6), round(len(neg) * 0.6)
    train, test = pos[:cut_p] + neg[:cut_n], pos[cut_p:] + neg[cut_n:]
    others = distractors(name, evals, a.distractors, a.seed)
    model = Model(a.url, os.environ.get(a.key_env, "") if a.key_env else "", a.model)
    print(f"{name}: {len(train)} train / {len(test)} test requests, {len(others)} other skills, model {a.model}", flush=True)

    history: list[dict] = []
    for it in range(a.iterations + 1):
        tr = score(model, name, desc, others, train, a.runs, a.temperature, a.workers, a.seed + it)
        te = score(model, name, desc, others, test, a.runs, a.temperature, a.workers, a.seed + it)
        history.append({"iteration": it, "description": desc, "train": tr, "test": te})
        print(f"iteration {it}: train {tr['accuracy']:.0%}  test {te['accuracy']:.0%}  ({len(desc)} chars)", flush=True)
        a.out.write_text(json.dumps({"skill": name, "model": a.model, "history": history}, indent=2), encoding="utf-8")
        misses = [m for m in tr["items"] if not m["passed"]]
        if it == a.iterations or not misses:
            break
        desc = propose(model, name, desc, body, misses, history)

    # Rank by all requests: the test split is small, so one request there must not decide it. Ties keep the earlier.
    n_tr, n_te = len(train), len(test)
    best = max(history, key=lambda h: (h["train"]["accuracy"] * n_tr + h["test"]["accuracy"] * n_te,
                                       h["test"]["accuracy"], -h["iteration"]))
    report = {"skill": name, "model": a.model, "best_iteration": best["iteration"],
              "best_description": best["description"], "best_test": best["test"]["accuracy"],
              "best_train": best["train"]["accuracy"], "history": history}
    a.out.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(f"best: iteration {best['iteration']} (test {best['test']['accuracy']:.0%}, train {best['train']['accuracy']:.0%})")
    print(best["description"])
    return 0


if __name__ == "__main__":
    sys.exit(main())
