#!/usr/bin/env python3
"""
api_genesis_server.py — REST API Server for Skill Genesis Model
================================================================
Exposes genesis tools as OpenAI-compatible function-calling endpoints.
Any agent that supports OpenAI function calling can use these tools.

Also provides raw REST endpoints for direct HTTP access.

Usage:
    python api_genesis_server.py [--port 8889]

Endpoints:
    GET  /health          — Health check
    GET  /audit           — Full system audit
    POST /discover        — Discover gaps
    POST /create          — Create skills
    POST /score           — Score quality
    POST /related         — Cross-reference
    GET  /landscape       — Landscape report
    GET  /trends          — Trend discovery
    POST /heal            — Self-repair
    POST /v1/chat/completions — OpenAI-compatible chat + function calling
"""

import sys, os, json, argparse, traceback
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs

HERMES_SKILLS = os.path.expandvars(r'$LOCALAPPDATA/hermes/skills')
GENESIS_PATH = os.path.join(HERMES_SKILLS, 'mlops', 'skill-genesis-model', 'scripts')
sys.path.insert(0, GENESIS_PATH)

GENESIS_MODULE = os.path.join(GENESIS_PATH, 'skill_genesis.py')
import importlib.util
spec = importlib.util.spec_from_file_location("genesis", GENESIS_MODULE)
genesis = importlib.util.module_from_spec(spec)
sys.argv = ['api_genesis_server.py']
spec.loader.exec_module(genesis)

model = genesis.SkillGenesis()

# ── OpenAI-compatible tool definitions ───────────────────────────────────
OPENAI_TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "genesis_audit",
            "description": "Full system health audit. Returns schema version, ecosystem coverage, lifetime stats.",
            "parameters": {"type": "object", "properties": {}, "required": []},
        }
    },
    {
        "type": "function",
        "function": {
            "name": "genesis_discover",
            "description": "Discover skill gaps in ecosystems.",
            "parameters": {
                "type": "object",
                "properties": {
                    "ecosystem": {"type": "string", "description": "Ecosystem or 'all'", "default": "all"}
                },
                "required": ["ecosystem"],
            },
        }
    },
    {
        "type": "function",
        "function": {
            "name": "genesis_create",
            "description": "Batch create skills from gaps.",
            "parameters": {
                "type": "object",
                "properties": {
                    "ecosystem": {"type": "string"},
                    "count": {"type": "integer", "default": 5},
                    "dry_run": {"type": "boolean", "default": False},
                },
                "required": ["ecosystem"],
            },
        }
    },
    {
        "type": "function",
        "function": {
            "name": "genesis_score",
            "description": "Score skill quality.",
            "parameters": {
                "type": "object",
                "properties": {
                    "name": {"type": "string"},
                    "all": {"type": "boolean", "default": False},
                    "min_score": {"type": "integer", "default": 0},
                },
                "required": [],
            },
        }
    },
    {
        "type": "function",
        "function": {
            "name": "genesis_related",
            "description": "Find related skills.",
            "parameters": {
                "type": "object",
                "properties": {"name": {"type": "string"}},
                "required": ["name"],
            },
        }
    },
    {
        "type": "function",
        "function": {
            "name": "genesis_landscape",
            "description": "Ecosystem coverage report.",
            "parameters": {
                "type": "object",
                "properties": {"ecosystem": {"type": "string", "default": "all"}},
                "required": [],
            },
        }
    },
    {
        "type": "function",
        "function": {
            "name": "genesis_trends",
            "description": "Technology trend opportunities.",
            "parameters": {
                "type": "object",
                "properties": {
                    "domain": {"type": "string"},
                    "count": {"type": "integer", "default": 10},
                },
                "required": [],
            },
        }
    },
]


def execute_genesis_tool(name: str, args: dict) -> dict:
    """Execute a genesis tool and return structured result."""
    if name == "genesis_audit":
        a = model.audit()
        a["model"]["ecosystems"] = list(a["model"]["ecosystems"])
        return a
    elif name == "genesis_discover":
        eco = args.get("ecosystem", "all")
        gaps = model.discover(None if eco == "all" else [eco])
        return {"total": len(gaps), "high": len([g for g in gaps if g["priority"]=="high"]), "gaps": gaps[:20]}
    elif name == "genesis_create":
        eco, count, dry = args["ecosystem"], args.get("count", 5), args.get("dry_run", False)
        results = model.discover_and_create(eco, count, dry)
        if dry: return {"dry_run": True, "would_create": len(results)}
        avg_q = sum(r.get("quality",{}).get("score",0) for r in results)/max(len(results),1)
        return {"created": len(results), "avg_quality": round(avg_q, 1)}
    elif name == "genesis_score":
        if args.get("all"):
            results = model.score(all_skills=True, min_score=args.get("min_score", 0))
            return {"total": len(results), "average": round(sum(r["score"] for r in results)/max(len(results),1),1)}
        q = model.score(name=args.get("name"))
        return q or {"error": "not found"}
    elif name == "genesis_related":
        return {"related": model.related(args["name"])}
    elif name == "genesis_landscape":
        eco = args.get("ecosystem", "all")
        return {"report": model.landscape_report(eco if eco != "all" else None)}
    elif name == "genesis_trends":
        return {"opportunities": model.discover_trends(args.get("domain"), args.get("count", 10))}
    return {"error": f"unknown tool: {name}"}


class GenesisAPIHandler(BaseHTTPRequestHandler):
    """HTTP request handler for the genesis API."""

    def _json(self, data, status=200):
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, Authorization")
        self.end_headers()
        self.wfile.write(json.dumps(data, indent=2).encode())

    def do_OPTIONS(self):
        self._json({})

    def do_GET(self):
        path = urlparse(self.path).path
        if path == "/health":
            self._json({"status": "ok", "model": "skill-genesis-v3", "skills": len(model.analyzer.skills)})
        elif path == "/audit":
            self._json(model.audit())
        elif path == "/landscape":
            eco = parse_qs(urlparse(self.path).query).get("ecosystem", ["all"])[0]
            self._json({"report": model.landscape_report(eco if eco != "all" else None)})
        elif path == "/trends":
            qs = parse_qs(urlparse(self.path).query)
            domain = qs.get("domain", [None])[0]
            count = int(qs.get("count", [10])[0])
            self._json({"opportunities": model.discover_trends(domain, count)})
        else:
            self._json({"error": "not found"}, 404)

    def do_POST(self):
        path = urlparse(self.path).path
        try:
            length = int(self.headers.get("Content-Length", 0))
            body = json.loads(self.rfile.read(length)) if length else {}
        except: body = {}

        if path == "/discover":
            eco = body.get("ecosystem", "all")
            gaps = model.discover(None if eco == "all" else [eco])
            self._json({"total": len(gaps), "gaps": gaps[:30]})

        elif path == "/create":
            eco = body.get("ecosystem")
            count = body.get("count", 5)
            dry = body.get("dry_run", False)
            results = model.discover_and_create(eco, count, dry)
            self._json({"created": len(results) if not dry else 0, "dry_run": dry, "skills": results if dry else None})

        elif path == "/score":
            if body.get("all"):
                results = model.score(all_skills=True, min_score=body.get("min_score", 0))
                self._json({"total": len(results), "results": results[:30]})
            else:
                q = model.score(name=body.get("name"))
                self._json(q or {"error": "not found"})

        elif path == "/related":
            self._json({"related": model.related(body.get("name", ""))})

        elif path == "/heal":
            self._json(model.heal())

        elif path == "/v1/chat/completions":
            # OpenAI-compatible chat completions with function calling
            self._handle_openai_chat(body)

        else:
            self._json({"error": "not found"}, 404)

    def _handle_openai_chat(self, body):
        """Handle OpenAI-compatible chat completions request."""
        messages = body.get("messages", [])
        tools = body.get("tools", OPENAI_TOOLS)
        tool_choice = body.get("tool_choice", "auto")

        last_msg = messages[-1]["content"] if messages else ""
        response_msg = "I can help manage your skill ecosystem. Available tools listed in response."

        # Check if any tool was requested
        chosen_tool = None
        for tool in tools:
            name = tool["function"]["name"]
            if name in last_msg.lower():
                chosen_tool = name
                break

        if chosen_tool:
            result = execute_genesis_tool(chosen_tool, {})
            response = {
                "id": "genesis-" + os.urandom(4).hex(),
                "object": "chat.completion",
                "created": int(__import__("time").time()),
                "model": "skill-genesis-v3",
                "choices": [{
                    "index": 0,
                    "message": {
                        "role": "assistant",
                        "content": None,
                        "tool_calls": [{
                            "id": f"call_{os.urandom(4).hex()}",
                            "type": "function",
                            "function": {"name": chosen_tool, "arguments": json.dumps(result)},
                        }],
                    },
                    "finish_reason": "tool_calls",
                }],
            }
            self._json(response)
        else:
            # Return available tools as content
            tool_list = "\n".join(f"  • {t['function']['name']}: {t['function']['description']}" for t in tools)
            response = {
                "id": "genesis-" + os.urandom(4).hex(),
                "object": "chat.completion",
                "created": int(__import__("time").time()),
                "model": "skill-genesis-v3",
                "choices": [{
                    "index": 0,
                    "message": {"role": "assistant", "content": f"Genesis tools available:\n\n{tool_list}"},
                    "finish_reason": "stop",
                }],
            }
            self._json(response)


def main():
    parser = argparse.ArgumentParser(description="Genesis REST API Server")
    parser.add_argument("--port", type=int, default=8889, help="Port to listen on")
    parser.add_argument("--host", default="0.0.0.0", help="Host to bind")
    args = parser.parse_args()
    server = HTTPServer((args.host, args.port), GenesisAPIHandler)
    print(f"[Genesis API] Server running on http://{args.host}:{args.port}")
    print(f"[Genesis API] OpenAI-compatible: POST /v1/chat/completions")
    print(f"[Genesis API] Endpoints: /health /audit /discover /create /score /related /landscape /trends /heal")
    try: server.serve_forever()
    except KeyboardInterrupt:
        print("\n[Genesis API] Shutting down...")
        server.server_close()

if __name__ == "__main__":
    main()
