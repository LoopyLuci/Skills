---
name: google-ads-api-mcp-setup
description: Use when installing and configuring the Google Ads MCP Server for AI assistants.
tags: [google-ads, mcp, api, python, pipx, ai-tools]
related_skills: [google-cloud-recipe-auth, gemini-api]
---

# Google Ads API MCP Server Installation

This skill provides a structured guide to install, configure, and integrate the official [Google Ads Model Context Protocol (MCP) Server](https://github.com/googleads/google-ads-mcp). It enables AI assistants (Claude Desktop, Cursor, Antigravity) to query Google Ads campaigns and retrieve reporting metrics via natural language.

## Prerequisites

- **Python 3.12+** and **pipx** installed
- **Google Ads API Credentials**: Developer Token, OAuth2 Client ID/Secret, Refresh Token, Customer IDs
- Outbound HTTPS access to `googleads.googleapis.com` and PyPI

## Installation Steps

1. **Verify prerequisites**: Check Python 3.12+ (`python3 --version`) and pipx (`pipx --version`)
2. **Install the server**: `pipx install google-ads-mcp`
3. **Verify installation**: `google-ads-mcp --help`
4. **Configure environment variables**: Set `GOOGLE_ADS_DEVELOPER_TOKEN`, `GOOGLE_ADS_CLIENT_ID`, `GOOGLE_ADS_CLIENT_SECRET`, `GOOGLE_ADS_REFRESH_TOKEN`
5. **Integrate with AI client**: Add MCP server config to Claude Desktop / Cursor settings

## Auth Environment Variables

| Variable | Description |
|----------|-------------|
| `GOOGLE_ADS_DEVELOPER_TOKEN` | Your Google Ads Developer Token |
| `GOOGLE_ADS_CLIENT_ID` | OAuth2 Client ID (`*.apps.googleusercontent.com`) |
| `GOOGLE_ADS_CLIENT_SECRET` | OAuth2 Client Secret |
| `GOOGLE_ADS_REFRESH_TOKEN` | OAuth2 Refresh Token |
| `GOOGLE_ADS_LOGIN_CUSTOMER_ID` | Manager Account ID (MCC) for hierarchies |

## Code Example: MCP Client Config

```json
{
  "mcpServers": {
    "google-ads": {
      "command": "pipx",
      "args": ["run", "google-ads-mcp"],
      "env": {
        "GOOGLE_ADS_DEVELOPER_TOKEN": "YOUR_TOKEN",
        "GOOGLE_ADS_CLIENT_ID": "YOUR_CLIENT_ID",
        "GOOGLE_ADS_CLIENT_SECRET": "YOUR_CLIENT_SECRET",
        "GOOGLE_ADS_REFRESH_TOKEN": "YOUR_REFRESH_TOKEN"
      }
    }
  }
}
```

## Common Pitfalls

- **PATH issues**: `pipx` binaries go to `~/.local/bin`; if `google-ads-mcp` isn't found, use absolute path or restart shell
- **Customer ID format**: Must be digits only (no hyphens), e.g., `1234567890`
- **Client restart required**: MCP servers load on app startup — restart the AI tool after config changes
- **IDE isolation**: External IDEs may not inherit shell RC files — set env vars in the MCP JSON config

## Verification Checklist

- [ ] Python 3.12+ confirmed: `python3 --version`
- [ ] pipx installed: `pipx --version`
- [ ] Server installed: `google-ads-mcp --help`
- [ ] Environment variables exported correctly
- [ ] AI client configured with MCP block
- [ ] Test query works: "List campaigns from account 1234567890"
