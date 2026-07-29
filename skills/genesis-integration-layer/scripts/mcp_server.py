#!/usr/bin/env python3
"""
mcp_genesis_server.py — MCP Server for Skill Genesis Model v3.0
================================================================
Exposes all 7 genesis tools as MCP tools. Works with ANY MCP client:
  - Claude Desktop
  - Cursor
  - Windsurf
  - VS Code with GitHub Copilot
  - Any MCP-compatible agent

Usage:
    python mcp_genesis_server.py
    # Configure in claude_desktop_config.json:
    # {
    #   "mcpServers": {
    #     "skill-genesis": {
    #       "command": "python",
    #       "args": ["path/to/mcp_genesis_server.py"]
    #     }
    #   }
    # }

Protocol: stdio-based MCP transport (fast, no HTTP overhead)
"""

import sys, os, json, asyncio, traceback

# Add genesis model to path
HERMES_SKILLS = os.path.expandvars(r'$LOCALAPPDATA/hermes/skills')
GENESIS_PATH = os.path.join(HERMES_SKILLS, 'mlops', 'skill-genesis-model', 'scripts')
sys.path.insert(0, GENESIS_PATH)

# Import the genesis model
GENESIS_MODULE = os.path.join(GENESIS_PATH, 'skill_genesis.py')

# We need to import it dynamically since it's a CLI script
import importlib.util
spec = importlib.util.spec_from_file_location("genesis", GENESIS_MODULE)
genesis = importlib.util.module_from_spec(spec)
# Execute in a way that doesn't trigger CLI mode
sys.argv = ['mcp_genesis_server.py']
spec.loader.exec_module(genesis)

# Create model instance
model = genesis.SkillGenesis()

# ── MCP Protocol ──────────────────────────────────────────────────────────
# MCP uses JSON-RPC over stdio. Each message is one JSON line.

def send_response(req_id, result):
    """Send a JSON-RPC response."""
    msg = {"jsonrpc": "2.0", "id": req_id, "result": result}
    sys.stdout.write(json.dumps(msg) + "\n")
    sys.stdout.flush()

def send_error(req_id, code, message):
    msg = {"jsonrpc": "2.0", "id": req_id, "error": {"code": code, "message": message}}
    sys.stdout.write(json.dumps(msg) + "\n")
    sys.stdout.flush()

def send_event(method, params):
    msg = {"jsonrpc": "2.0", "method": method, "params": params}
    sys.stdout.write(json.dumps(msg) + "\n")
    sys.stdout.flush()

# ── Initialize ──
send_event("log", {"level": "info", "data": f"Genesis MCP Server initialized. {len(model.analyzer.skills)} skills, 7 tools."})

# ── Tool Definitions ──────────────────────────────────────────────────────
TOOLS = [
    {
        "name": "genesis_audit",
        "description": "Full system health audit of the Skill Genesis Model. Returns schema version, ecosystem coverage, lifetime stats, and health status.",
        "inputSchema": {"type": "object", "properties": {}, "required": []},
    },
    {
        "name": "genesis_discover",
        "description": "Discover skill gaps in one or all ecosystems. Returns list of missing skills with priorities.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "ecosystem": {"type": "string", "description": "Ecosystem name (e.g., 'kubernetes', 'aws') or 'all' for all ecosystems", "default": "all"}
            },
            "required": ["ecosystem"],
        },
    },
    {
        "name": "genesis_create",
        "description": "Batch create skills from discovered gaps. Automatically discovers gaps in an ecosystem and creates skills for them.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "ecosystem": {"type": "string", "description": "Ecosystem to create skills for (e.g., 'kubernetes')"},
                "count": {"type": "integer", "description": "Number of skills to create", "default": 5},
                "dry_run": {"type": "boolean", "description": "Preview without creating", "default": False},
            },
            "required": ["ecosystem"],
        },
    },
    {
        "name": "genesis_score",
        "description": "Score skill quality (0-100). Score a specific skill by name or all skills with optional minimum threshold.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "name": {"type": "string", "description": "Skill name to score (omit for all skills)"},
                "min_score": {"type": "integer", "description": "Minimum score threshold", "default": 0},
                "all": {"type": "boolean", "description": "Score all skills", "default": False},
            },
            "required": [],
        },
    },
    {
        "name": "genesis_related",
        "description": "Find related skills by semantic overlap. Returns skill names ranked by tag + category similarity.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "name": {"type": "string", "description": "Skill name to find related skills for"},
            },
            "required": ["name"],
        },
    },
    {
        "name": "genesis_landscape",
        "description": "Full landscape report with coverage bars and gap counts per ecosystem.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "ecosystem": {"type": "string", "description": "Ecosystem name or 'all'"},
            },
            "required": ["ecosystem"],
        },
    },
    {
        "name": "genesis_trends",
        "description": "Discover skill creation opportunities from technology trends and market momentum.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "domain": {"type": "string", "description": "Domain to filter (e.g., 'mlops', 'networking')"},
                "count": {"type": "integer", "description": "Number of opportunities to return", "default": 10},
            },
            "required": [],
        },
    },
    {
        "name": "genesis_heal",
        "description": "Self-healing: detect and repair corrupt state, missing directories, broken references.",
        "inputSchema": {"type": "object", "properties": {}, "required": []},
    },
    {
        "name": "genesis_bulk_report",
        "description": "Full inventory report: skills per category, total count, distribution.",
        "inputSchema": {"type": "object", "properties": {}, "required": []},
    },
    {
        "name": "genesis_validate",
        "description": "Validate all skills for quality issues (missing sections, no code examples, etc).",
        "inputSchema": {"type": "object", "properties": {}, "required": []},
    },
]


def handle_tool_call(req_id, name, args):
    """Execute a genesis tool and return its result."""
    try:
        if name == "genesis_audit":
            result = model.audit()
            # Convert sets to lists for JSON serialization
            result["model"]["ecosystems"] = list(result["model"]["ecosystems"])
            return send_response(req_id, result)

        elif name == "genesis_discover":
            eco = args.get("ecosystem", "all")
            ecosystems = None if eco == "all" else [eco]
            gaps = model.discover(ecosystems)
            return send_response(req_id, {
                "total_gaps": len(gaps),
                "high_priority": len([g for g in gaps if g["priority"] == "high"]),
                "gaps": gaps[:20],
                "note": "First 20 shown" if len(gaps) > 20 else None,
            })

        elif name == "genesis_create":
            eco = args.get("ecosystem")
            count = args.get("count", 5)
            dry_run = args.get("dry_run", False)
            results = model.discover_and_create(eco, count, dry_run)
            if dry_run:
                return send_response(req_id, {"dry_run": True, "would_create": len(results), "skills": results})
            total_q = sum(r.get("quality", {}).get("score", 0) for r in results)
            avg_q = total_q / max(len(results), 1)
            return send_response(req_id, {
                "created": len(results),
                "avg_quality": round(avg_q, 1),
                "total_skills_ever": model.memory.state["total_skills_created"],
            })

        elif name == "genesis_score":
            score_name = args.get("name")
            min_score = args.get("min_score", 0)
            all_s = args.get("all", False)
            if all_s or not score_name:
                results = model.score(all_skills=True, min_score=min_score)
                avg = sum(r["score"] for r in results) / max(len(results), 1) if results else 0
                return send_response(req_id, {
                    "total": len(results),
                    "average": round(avg, 1),
                    "results": results[:20],
                })
            else:
                q = model.score(name=score_name)
                if q: return send_response(req_id, q)
                else: return send_error(req_id, -32000, f"Skill '{score_name}' not found")

        elif name == "genesis_related":
            skill_name = args.get("name")
            refs = model.related(skill_name)
            return send_response(req_id, {"skill": skill_name, "related": refs})

        elif name == "genesis_landscape":
            eco = args.get("ecosystem", "all")
            report = model.landscape_report(eco if eco != "all" else None)
            return send_response(req_id, {"report": report})

        elif name == "genesis_trends":
            domain = args.get("domain")
            count = args.get("count", 10)
            results = model.discover_trends(domain, count)
            return send_response(req_id, {"total": len(results), "opportunities": results})

        elif name == "genesis_heal":
            result = model.heal()
            return send_response(req_id, result)

        elif name == "genesis_bulk_report":
            report = model.bulk_report()
            return send_response(req_id, {"report": report})

        elif name == "genesis_validate":
            issues = model.bulk_validate()
            return send_response(req_id, {
                "skills_with_issues": len(issues),
                "issues": issues[:20],
            })

        else:
            return send_error(req_id, -32601, f"Tool '{name}' not found")

    except Exception as e:
        traceback.print_exc(file=sys.stderr)
        return send_error(req_id, -32000, str(e))


# ── Main Loop ─────────────────────────────────────────────────────────────
async def main():
    """Listen for JSON-RPC messages on stdin."""
    loop = asyncio.get_event_loop()
    reader = asyncio.StreamReader()
    protocol = asyncio.StreamReaderProtocol(reader)
    await loop.connect_read_pipe(lambda: protocol, sys.stdin)

    # Send initialized notification
    send_event("initialized", {})

    while True:
        try:
            line = await reader.readline()
            if not line:
                break
            msg = json.loads(line.decode().strip())
            msg_id = msg.get("id")
            method = msg.get("method")

            if method == "initialize":
                send_response(msg_id, {
                    "protocolVersion": "2024-11-05",
                    "capabilities": {"tools": {}},
                    "serverInfo": {"name": "skill-genesis-mcp", "version": "3.0.0"},
                })
                send_event("log", {"level": "info", "data": "MCP connection initialized"})

            elif method == "tools/list":
                send_response(msg_id, TOOLS)

            elif method == "tools/call":
                handle_tool_call(msg_id, msg["params"]["name"], msg["params"].get("arguments", {}))

            elif method == "notifications/initialized":
                pass  # No-op

            else:
                send_error(msg_id, -32601, f"Method '{method}' not found")

        except json.JSONDecodeError:
            continue
        except Exception as e:
            traceback.print_exc(file=sys.stderr)
            break


if __name__ == "__main__":
    asyncio.run(main())
