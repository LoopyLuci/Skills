# Real-World Architecture: 5 Custom MCP Servers for Daily Life & Work

This reference documents the concrete 5-server build from the originating session at `C:\Projects\AgenticTools\local-mcp-tools\`. Each server is a standalone Python MCP script wired into Hermes Agent as a stdio subprocess.

## 1. Property Intel (`property_intel.py`) — 21 tools

**Domain:** Real Estate  
**Database:** `~/.hermes/mcp-data/property_intel.db`  
**Tables:** properties, leads, comps, showings, open_houses, market_notes, property_expenses

**Key tools:**
- `property_add` / `property_search` / `property_get` / `property_update` / `property_delete` — CRUD watchlist
- `lead_add` / `lead_search` / `lead_update_status` — buyer/seller pipeline (new→contacted→qualified→showing→offer)
- `comp_add` / `comp_search` — comparable sales database
- `cma_generate` — comparative market analysis from nearby comps
- `showing_schedule` / `showing_list` / `showing_update_status` — showing management
- `open_house_create` / `open_house_list` / `open_house_log_visitors` — open house events
- `property_expense_add` — renovation/holding/marketing costs per property
- `market_note_add` / `market_summary` — ZIP-level market intelligence
- `pipeline_report` — full pipeline snapshot

## 2. Content Publisher (`content_publisher.py`) — 20 tools

**Domain:** Social Media & Content Marketing  
**Database:** `~/.hermes/mcp-data/content_publisher.db`  
**Tables:** posts, content_ideas, hashtags, engagement_log, accounts

**Key tools:**
- `post_create` / `post_list` / `post_get` / `post_update_status` — content calendar CRUD
- `idea_generate` / `idea_save_batch` — automated content idea generation
- `hashtag_suggest` / `hashtag_add` / `hashtag_search` — hashtag library
- `engagement_log` / `engagement_report` — performance tracking
- `account_add` / `account_list` — connected social accounts
- `content_grid_plan` — visual content grid for Instagram/etc.

## 3. Marketing Engine (`marketing_engine.py`) — 18 tools

**Domain:** Marketing Automation, SEO, Competitive Intel  
**Database:** `~/.hermes/mcp-data/marketing_engine.db`  
**Tables:** campaigns, campaign_metrics, keywords, keyword_rankings, content_briefs, competitors, competitor_activities, channels

**Key tools:**
- `campaign_create` / `campaign_list` / `campaign_get` / `campaign_log_metrics` / `campaign_update_status` — full campaign lifecycle with ROAS/CTR/CPA analytics
- `keyword_track` / `keyword_log_ranking` / `keyword_report` / `keyword_ranking_history` — SEO tracking
- `brief_create` / `brief_list` / `brief_get` / `brief_update_status` — content briefs
- `competitor_add` / `competitor_list` / `competitor_log_activity` / `competitor_report` — competitive intel
- `marketing_dashboard` — comprehensive rollup

## 4. Life Orchestrator (`life_orchestrator.py`) — 22 tools

**Domain:** Personal Productivity & Daily Life  
**Database:** `~/.hermes/mcp-data/life_orchestrator.db`  
**Tables:** tasks, habits, habit_logs, notes, expenses, goals, journal_entries

**Key tools:**
- `task_add` / `task_list` / `task_complete` / `task_update` / `task_delete` / `task_stats` — task management with priorities, projects, tags, `today`/`overdue`/`this_week` query modes
- `habit_create` / `habit_list` / `habit_log` / `habit_report` — habit tracking with automatic streak calculation
- `note_create` / `note_search` / `note_get` / `note_update` / `note_delete` — full-text searchable notes
- `expense_add` / `expense_summary` — spending tracking by week/month/quarter/year
- `goal_create` / `goal_list` / `goal_update_progress` — goal tracking with progress bars
- `daily_briefing` / `weekly_review` — auto-generated daily and weekly reports

## 5. Data Connector (`data_connector.py`) — 16 tools

**Domain:** Utilities, Web, Files, Notifications  
**Database:** `~/.hermes/mcp-data/data_connector.db`  
**Tables:** cache, bookmarks, notifications, snippets

**Key tools:**
- `web_fetch` / `cache_clear` / `cache_stats` — web content fetching with SQLite cache
- `bookmark_add` / `bookmark_list` — file/URL bookmarking
- `file_search` — glob-based file search with depth limiting
- `notify` / `notification_history` — notification logging
- `currency_convert` — currency conversion with 20+ currencies
- `time_utility` — current time, date math, days-between
- `qr_generate` — QR code generation
- `text_utility` — word count, slugify, URL extraction, truncation
- `snippet_add` / `snippet_get` / `snippet_search` — reusable text snippet storage
- `system_info` — OS/Python/hostname info

## Tool Count Summary

| Server | Tools |
|--------|-------|
| property_intel | 21 |
| content_publisher | 20 |
| marketing_engine | 18 |
| life_orchestrator | 22 |
| data_connector | 16 |
| **Total** | **97** |

## Hermes Config

```yaml
mcp_servers:
  property-intel:
    command: "python"
    args: ["C:/Projects/AgenticTools/local-mcp-tools/src/servers/property_intel.py"]
    timeout: 30
  content-publisher:
    command: "python"
    args: ["C:/Projects/AgenticTools/local-mcp-tools/src/servers/content_publisher.py"]
    timeout: 30
  marketing-engine:
    command: "python"
    args: ["C:/Projects/AgenticTools/local-mcp-tools/src/servers/marketing_engine.py"]
    timeout: 30
  life-orchestrator:
    command: "python"
    args: ["C:/Projects/AgenticTools/local-mcp-tools/src/servers/life_orchestrator.py"]
    timeout: 30
  data-connector:
    command: "python"
    args: ["C:/Projects/AgenticTools/local-mcp-tools/src/servers/data_connector.py"]
    timeout: 30
```