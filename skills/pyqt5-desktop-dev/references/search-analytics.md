# Search & Analytics

## Full-Text Search

```python
# search.py - Full-text search across projects

class SearchIndex:
    """Full-text search index for projects."""
    
    def add_document(self, doc_id: str, content: dict[str, str]) -> None:
        """Add a document to the index."""
        # Tokenize and index with TF scoring
    
    def remove_document(self, doc_id: str) -> None:
        """Remove a document from the index."""
    
    def search(self, query: str, limit: int = 20) -> list[dict]:
        """Search for documents matching the query."""
        # Return sorted results by score
    
    def _tokenize(self, text: str) -> list[str]:
        """Tokenize text into search terms."""
        # Lowercase, split on word boundaries, remove stop words

class ProjectSearch:
    """Search across all projects."""
    
    def _build_index(self) -> None:
        """Build search index from all projects."""
    
    def _index_project(self, project: Project) -> None:
        """Index a single project."""
        content = {
            "title": project.name,
            "description": "",
            "type": "project",
            "sections": " ".join(s.type for s in project.pages[0].sections),
        }
        self.index.add_document(project.id, content)
```

## Analytics Tracking

```python
# analytics.py - Usage tracking and dashboard data

class AnalyticsTracker:
    """Tracks usage analytics."""
    
    def track(self, event_type: str, data: dict = None, session_id: str = "", user_id: str = "") -> None:
        """Track an event."""
        event = AnalyticsEvent(
            id=f"evt-{uuid.uuid4().hex[:8]}",
            event_type=event_type,
            data=data or {},
            timestamp=datetime.now().isoformat(),
            session_id=session_id,
            user_id=user_id,
        )
        self.events.append(event)
        self._save_events()
    
    def get_stats(self) -> dict:
        """Get analytics statistics."""
        return {
            "total_events": len(self.events),
            "events_last_24h": len(events_24h),
            "events_last_7d": len(events_7d),
            "events_last_30d": len(events_30d),
            "event_counts": dict(event_counts),
            "most_common_events": sorted(event_counts.items(), key=lambda x: x[1], reverse=True)[:10],
        }
```

## Search Scoring

```python
# Simple TF (Term Frequency) scoring
for term in terms:
    if term not in self.index:
        self.index[term] = {}
    self.index[term][doc_id] = self.index[term].get(doc_id, 0) + 1

# Query scoring
for term in query_terms:
    if term in self.index:
        for doc_id, score in self.index[term].items():
            scores[doc_id] += score
```

## Stop Words

```python
stop_words = {"a", "an", "the", "and", "or", "but", "in", "on", "at", "to", "for", "of", "is", "it", "this", "that"}
```

## Search & Analytics Checklist

- [ ] Full-text search across projects
- [ ] TF scoring for relevance
- [ ] Stop word removal
- [ ] Event tracking
- [ ] Session management
- [ ] Usage statistics (24h, 7d, 30d)
- [ ] Most common events
- [ ] Export analytics data
