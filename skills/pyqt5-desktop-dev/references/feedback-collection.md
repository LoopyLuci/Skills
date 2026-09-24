# Feedback Collection

## In-App Feedback Dialog

```python
# feedback_dialog.py - In-app feedback collection

class FeedbackDialog(QDialog):
    """Dialog for collecting user feedback."""
    
    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(parent)
        self.setWindowTitle("Send Feedback")
        self.setMinimumSize(500, 400)
        self.collector = feedback_collector
    
    def setup_ui(self):
        # Type selection (Bug Report, Feature Request, General Feedback, Rating)
        # Rating widget (hidden by default, shown when type=Rating)
        # Message input
        # Submit/Cancel buttons
    
    def _on_submit(self):
        feedback_type = self.type_combo.currentText()
        message = self.message_input.toPlainText().strip()
        rating = self.rating_combo.currentIndex() + 1 if feedback_type == "Rating" else None
        
        self.collector.submit_feedback(
            feedback_type=type_map[feedback_type],
            message=message,
            rating=rating,
        )
```

## Feedback Collector

```python
# feedback.py - Feedback collection and analytics

class FeedbackCollector:
    """Collects and manages user feedback."""
    
    def submit_feedback(self, feedback_type: str, message: str, rating: Optional[int] = None, metadata: Optional[dict] = None) -> dict:
        """Submit user feedback."""
        feedback = {
            "id": f"fb-{uuid.uuid4().hex[:8]}",
            "session_id": self.session_id,
            "type": feedback_type,
            "message": message,
            "rating": rating,
            "metadata": metadata or {},
            "system_info": self._get_system_info(),
            "timestamp": datetime.now().isoformat(),
            "app_version": "1.0.0",
        }
        # Save to ~/.webbuilder/feedback/
    
    def submit_bug_report(self, title: str, description: str, steps: str, expected: str, actual: str) -> dict:
        """Submit a bug report."""
    
    def submit_feature_request(self, title: str, description: str) -> dict:
        """Submit a feature request."""
    
    def submit_rating(self, rating: int, comment: str = "") -> dict:
        """Submit a rating (1-5)."""
    
    def submit_nps(self, score: int, reason: str = "") -> dict:
        """Submit NPS score (0-10)."""
    
    def get_feedback_summary(self) -> dict:
        """Get feedback summary statistics."""
        return {
            "total_feedback": len(feedback),
            "by_type": {...},
            "average_rating": sum(ratings) / len(ratings) if ratings else 0,
            "nps_score": self._calculate_nps(nps_scores) if nps_scores else 0,
        }
```

## NPS Calculation

```python
def _calculate_nps(self, scores: list[int]) -> int:
    """Calculate NPS score."""
    promoters = len([s for s in scores if s >= 9])
    detractors = len([s for s in scores if s <= 6])
    total = len(scores)
    return int(((promoters - detractors) / total) * 100) if total > 0 else 0
```

## Feedback Types

| Type | Description | Data Captured |
|------|-------------|---------------|
| Bug Report | Something is broken | Title, description, steps, expected, actual |
| Feature Request | New feature idea | Title, description |
| Rating | User satisfaction | 1-5 stars + comment |
| NPS | Net Promoter Score | 0-10 score + reason |
| General Feedback | Anything else | Free text |

## Storage

```
~/.webbuilder/feedback/
  fb-xxxxxxxx.json  # Individual feedback entries
  session_id        # Anonymous session identifier
```

## Integration

```python
# In WebBuilderWindow.setup_menu():
feedback_action = QAction("Send Feedback...", self)
feedback_action.triggered.connect(self.open_feedback)
help_menu.addAction(feedback_action)

# Handler:
def open_feedback(self):
    from webbuilder.gui.feedback_dialog import FeedbackDialog
    dialog = FeedbackDialog(self)
    dialog.exec_()
```

## Feedback Checklist

- [ ] In-app feedback dialog accessible from Help menu
- [ ] Bug report form with steps/expected/actual
- [ ] Feature request form
- [ ] Star rating (1-5)
- [ ] NPS score (0-10)
- [ ] Anonymous session tracking
- [ ] System info auto-collected
- [ ] Export feedback to JSON
- [ ] NPS calculation
