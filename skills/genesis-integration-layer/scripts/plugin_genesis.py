#!/usr/bin/env python3
"""
plugin_genesis.py — Hermes Agent Plugin for Skill Genesis Model
================================================================
Load this as a Hermes plugin to make all genesis tools available as
native Hermes tools (genesis_discover, genesis_create, genesis_score, etc.)

Installation:
    Copy to: %LOCALAPPDATA%/hermes/plugins/genesis-plugin/
    Or load via: skill_manage(action='create', name='genesis-plugin', ...)

The plugin registers itself with Hermes Agent's tool system, making the
genesis model's 7 tools available in every conversation.
"""

import os, sys, json, re

HERMES_SKILLS = os.path.expandvars(r'$LOCALAPPDATA/hermes/skills')

# ── Plugin Metadata ──────────────────────────────────────────────────────
PLUGIN_NAME = "genesis-plugin"
PLUGIN_VERSION = "3.0.0"
PLUGIN_DESCRIPTION = "Skill Genesis Model integration for Hermes Agent"

# Tool schema definitions for Hermes Agent
TOOL_SCHEMAS = {
    "genesis_discover": {
        "description": "Discover skill gaps in any ecosystem. Finds missing skills ranked by priority.",
        "parameters": {
            "type": "object",
            "properties": {
                "ecosystem": {
                    "type": "string",
                    "description": "Ecosystem to analyze (kubernetes, aws, react, python, security) or 'all'",
                    "default": "all",
                }
            },
        },
    },
    "genesis_create": {
        "description": "Batch create skills from discovered gaps in an ecosystem.",
        "parameters": {
            "type": "object",
            "properties": {
                "ecosystem": {"type": "string", "description": "Ecosystem to create skills for"},
                "count": {"type": "integer", "description": "Number of skills to create", "default": 5},
                "dry_run": {"type": "boolean", "description": "Preview without creating", "default": False},
            },
            "required": ["ecosystem"],
        },
    },
    "genesis_score": {
        "description": "Score skill quality (0-100) with grade and improvement suggestions.",
        "parameters": {
            "type": "object",
            "properties": {
                "name": {"type": "string", "description": "Specific skill to score"},
                "all": {"type": "boolean", "description": "Score all skills", "default": False},
                "min_score": {"type": "integer", "description": "Minimum threshold", "default": 0},
            },
        },
    },
    "genesis_related": {
        "description": "Find semantically related skills for cross-referencing.",
        "parameters": {
            "type": "object",
            "properties": {"name": {"type": "string", "description": "Skill name"}},
            "required": ["name"],
        },
    },
    "genesis_landscape": {
        "description": "Full ecosystem landscape report with coverage bars.",
        "parameters": {
            "type": "object",
            "properties": {
                "ecosystem": {"type": "string", "description": "Ecosystem or 'all'", "default": "all"}
            },
        },
    },
    "genesis_trends": {
        "description": "Discover skill opportunities from technology trends.",
        "parameters": {
            "type": "object",
            "properties": {
                "domain": {"type": "string", "description": "Domain filter (mlops, networking, etc)"},
                "count": {"type": "integer", "description": "Number of results", "default": 10},
            },
        },
    },
    "genesis_audit": {
        "description": "Full system health audit of the genesis model.",
        "parameters": {"type": "object", "properties": {}},
    },
    "genesis_heal": {
        "description": "Self-healing: repair state, recreate directories, fix corruption.",
        "parameters": {"type": "object", "properties": {}},
    },
}


class GenesisPlugin:
    """Hermes Agent plugin that loads genesis model as native tools."""

    def __init__(self, hermes_context=None):
        self.name = PLUGIN_NAME
        self.version = PLUGIN_VERSION
        self.context = hermes_context
        self.model = None
        self._initialized = False

    def initialize(self):
        """Lazy-load the genesis model on first use."""
        if self._initialized:
            return
        try:
            genesis_path = os.path.join(
                HERMES_SKILLS, 'mlops', 'skill-genesis-model', 'scripts'
            )
            sys.path.insert(0, genesis_path)
            module_path = os.path.join(genesis_path, 'skill_genesis.py')
            import importlib.util
            spec = importlib.util.spec_from_file_location("genesis", module_path)
            genesis = importlib.util.module_from_spec(spec)
            sys.argv = ['plugin_genesis.py']
            spec.loader.exec_module(genesis)
            self.model = genesis.SkillGenesis()
            self._initialized = True
        except Exception as e:
            print(f"[Genesis Plugin] Failed to load model: {e}")

    def get_tools(self):
        """Return tool definitions for Hermes Agent's tool system."""
        return TOOL_SCHEMAS

    def execute_tool(self, tool_name: str, arguments: dict) -> dict:
        """Execute a genesis tool."""
        self.initialize()
        if not self.model:
            return {"error": "Genesis model not loaded"}

        try:
            if tool_name == "genesis_audit":
                result = self.model.audit()
                result["model"]["ecosystems"] = list(result["model"]["ecosystems"])
                return result
            elif tool_name == "genesis_discover":
                eco = arguments.get("ecosystem", "all")
                gaps = self.model.discover(None if eco == "all" else [eco])
                return {"total": len(gaps), "gaps": gaps[:25]}
            elif tool_name == "genesis_create":
                eco = arguments.get("ecosystem")
                count = arguments.get("count", 5)
                dry = arguments.get("dry_run", False)
                results = self.model.discover_and_create(eco, count, dry)
                if dry: return {"dry_run": True, "would_create": results}
                avg_q = sum(r.get("quality",{}).get("score",0) for r in results)/max(len(results),1)
                return {"created": len(results), "avg_quality": round(avg_q, 1)}
            elif tool_name == "genesis_score":
                if arguments.get("all"):
                    results = self.model.score(all_skills=True, min_score=arguments.get("min_score", 0))
                    return {"total": len(results), "average": round(sum(r["score"] for r in results)/max(len(results),1),1)}
                q = self.model.score(name=arguments.get("name"))
                return q or {"error": "not found"}
            elif tool_name == "genesis_related":
                return {"related": self.model.related(arguments.get("name", ""))}
            elif tool_name == "genesis_landscape":
                eco = arguments.get("ecosystem", "all")
                return {"report": self.model.landscape_report(eco if eco != "all" else None)}
            elif tool_name == "genesis_trends":
                return {"opportunities": self.model.discover_trends(
                    arguments.get("domain"), arguments.get("count", 10))}
            elif tool_name == "genesis_heal":
                return self.model.heal()
            else:
                return {"error": f"Unknown tool: {tool_name}"}
        except Exception as e:
            return {"error": str(e)}


# ── Plugin entry point ───────────────────────────────────────────────────
def create_plugin(hermes_context=None):
    """Plugin factory function for Hermes Agent."""
    return GenesisPlugin(hermes_context)
