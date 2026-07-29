---
title: "Building MCP Servers for Media/Streaming Applications"
source: "SovereignStream project — a self-hosted streaming platform with 25+ MCP tools"
date: "2026-07-28"
tags: ["mcp", "media-streaming", "rust", "react", "zustand", "agent-integration"]
---

# Media/Streaming MCP Server Patterns

Real-world patterns from building SovereignStream — a self-hosted music/video
platform with 25+ MCP tools, React frontend, and full agent integration.

## Tool Architecture for Large Toolkits

When an MCP server needs 20+ tools, structure them by category for maintainability:

```rust
// Pattern from sovereign-mcp/src/lib.rs
pub fn register_builtin_tools(registry: &mut McpToolRegistry) {
    // Playback (4 tools)
    register_tools_playback(registry);
    // Search & Discovery (3 tools)
    register_tools_search(registry);
    // Library Management (5 tools)
    register_tools_library(registry);
    // Upload & Ingest (3 tools)
    register_tools_upload(registry);
    // Recommendations (3 tools)
    register_tools_recommendations(registry);
    // Playlists (5 tools)
    register_tools_playlists(registry);
    // Social & Sharing (4 tools)
    register_tools_social(registry);
    // Preferences & Analytics (3 tools)
    register_tools_preferences(registry);
    // Import/Export (2 tools)
    register_tools_import_export(registry);
}
```

The SovereignStream tool set (25+ tools):

| Category | Tools |
|---|---|
| Playback | `play_track`, `pause_playback`, `resume_playback`, `stop_playback`, `skip_to`, `next_track`, `previous_track` |
| Search | `search` (with type/limit/query params), `get_similar_artists`, `get_related_content` |
| Library | `upload_music`, `upload_video`, `add_to_library`, `sync_library` |
| Playlists | `create_playlist`, `add_to_playlist`, `remove_from_playlist`, `reorder_playlist`, `delete_playlist` |
| Recommendations | `get_recommendations`, `generate_smart_playlist`, `set_preferences` |
| Analytics | `get_listening_history`, `get_analytics` |
| Import | `import_playlist` |

## Resource URI Templates for Media

```rust
// Resource URIs (RFC 6576 templates)
// Each maps to a data entity in the media library
ResourceTemplate {
    uri: "sovereign://library/{id}"         // → Library item
    uri: "sovereign://track/{id}"           // → Track metadata + stream URL
    uri: "sovereign://album/{id}"           // → Album with track listing
    uri: "sovereign://artist/{id}"          // → Artist with discography
    uri: "sovereign://playlist/{id}"        // → Playlist with item list
    uri: "sovereign://video/{id}"           // → Video with resolutions
    uri: "sovereign://user/{id}"            // → User profile + preferences
    uri: "sovereign://current"              // → Currently-playing session
    uri: "sovereign://queue"                // → Current playback queue
}
```

## Web Frontend Integration Pattern

The React frontend uses Zustand stores that mirror the MCP tool surface,
allowing the UI and agent to share state naturally:

```typescript
// PlayerStore mirrors the Playback MCP tools
// The same `play(trackId)` action is called by both
//   - The CommandBar (user types "play Bohemian Rhapsody")
//   - The MCP agent (Hermes sends play_track via WebSocket)
//   - The UI (user clicks a track card)

export const usePlayerStore = create()({
  isPlaying: boolean;
  currentTrackId: string | null;
  queue: Track[];
  volume: number;
  repeatMode: 'off' | 'one' | 'all';
  shuffle: boolean;

  // Same signature as MCP tools — allows agent ↔ UI parity
  play: (trackId: string) => void;
  pause: () => void;
  togglePlay: () => void;
  next: () => void;
  // ...
});
```

## Agent Workflow Patterns

These are the most common multi-turn agent interactions with a media platform:

### Pattern 1: "Play something" (single natural language → tool call)
```
User: "Play some jazz for studying"
Agent:
  1. search(query: "jazz", limit: 10) → [results]
  2. get_recommendations(genre: "jazz", mood: "focus") → [recommended tracks]
  3. play_track(trackId: "tk-123", encoding: "flac")
  4. Response: "Playing 'So What' by Miles Davis — a classic jazz study track"
```

### Pattern 2: Create Smart Playlist (multi-turn with context)
```
User: "Make a road trip playlist with rock classics"
Agent:
  1. search(query: "rock classics", type: "track", limit: 20) → [results]
  2. Create playlist → create_playlist(name: "Road Trip Classics", isPublic: false)
  3. Add each track → add_to_playlist(playlistId: "pl-1", trackId: each)
  4. Response: "Created 'Road Trip Classics' with 20 tracks"
```

### Pattern 3: Multi-turn discovery (maintains context across turns)
```
Turn 1 — User: "Play something by Queen"
          Agent: play_track → "Playing Bohemian Rhapsody"

Turn 2 — User: "Add this to my favorites"
          Agent: add_to_playlist(playlistId: "favorites", trackId: current)
          → "Added 'Bohemian Rhapsody' to 'Favorites'"

Turn 3 — User: "What should I listen to next?"
          Agent: get_recommendations(basedOn: "current-track") → [recommendations]
          → "Based on Queen, you might like Led Zeppelin or The Eagles"
```

## Streaming Quality & Format Parameters

When MCP tools involve media streaming, expose quality/encoding as optional tool
parameters so agents can adapt to connection speed:

```json
// Tool parameter schema for play_track
{
  "trackId": {"type": "string", "description": "Track UUID"},
  "quality": {
    "type": "string",
    "enum": ["flac", "wav", "alac", "opus-320", "opus-192", "opus-128", "aac-high", "aac-medium"],
    "default": "flac"
  },
  "spatialAudio": {
    "type": "boolean",
    "default": false,
    "description": "Enable Dolby Atmos / spatial audio rendering"
  }
}
```

## Frontend ↔ MCP Testing Pattern

For testing agent workflows in the browser, provide a dedicated MCP introspection
page that simulates agent commands:

```typescript
// End-to-end agent workflow test (via Playwright)
test('should play music via natural language command from Hermes Agent', async ({ page }) => {
  await page.fill('[data-testid="mcp-command-input"]', 'Play Bohemian Rhapsody');
  await page.click('[data-testid="mcp-execute-btn"]');

  await expect(page.locator('[data-testid="now-playing-title"]')).toContainText('Bohemian Rhapsody');
  await expect(page.locator('[data-testid="player-status"]')).toHaveText('playing');
});
```

## Key Architectural Principles (from SovereignStream)

1. **Agent-native from day one** — tools mirror UI actions exactly; both call the same store
2. **25+ tools organized in 9 categories** — prevents the "one file with everything" problem
3. **Shared state via Zustand** — UI and MCP feed from the same store, no sync layer needed
4. **Natural language → tool via debounced search** — the CommandBar interprets both typed commands and natural language, feeding into the same MCP tool handlers
5. **Thin MCP layer over application logic** — tools don't duplicate business logic; they call the same service layer as the REST API
6. **WebSocket transport for agent integration** — avoids port conflicts with the REST API; keeps agent connections on a separate port (3001 vs 3000)
7. **All state is persistable** — Zustand middleware saves player state, queue, preferences to localStorage so agent context survives page reloads
8. **Every UI interaction has keyboard/agent parity** — Ctrl+K play is same as agent `play_track` is same as clicking a card
