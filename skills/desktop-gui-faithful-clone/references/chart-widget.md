# ChartWidget Pattern (PyQt6, no QtCharts)

The `PyQt6.QtCharts` module is NOT installed in the fan-controller venv. Replace QtCharts with a custom `ChartWidget` that draws using `QPainter`, `QPen`, and `QBrush`.

## ChartWidget class

```python
class ChartWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.points = []  # list of (x, y)
        self.color = QColor("#38bdf8")
        self.title = ""
        self.y_min = 0
        self.y_max = 100
        self.pen = QPen(self.color, 2)

    def set_title(self, title): self.title = title
    def set_color(self, color): self.color = QColor(color); self.pen = QPen(self.color, 2)
    def set_y_range(self, y_min, y_max): self.y_min = y_min; self.y_max = y_max
    def set_points(self, points): self.points = list(points)
    def add_point(self, x, y): self.points.append((x, y))

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        rect = self.rect()
        painter.fillRect(rect, QColor("#0f172a"))
        if len(self.points) < 2:
            painter.setPen(QColor("#64748b"))
            painter.drawText(rect, Qt.AlignmentFlag.AlignCenter, "No data")
            return
        xs = [p[0] for p in self.points]
        ys = [p[1] for p in self.points]
        x_min, x_max = min(xs), max(xs)
        pad_left, pad_right, pad_top, pad_bottom = 60, 20, 30, 40
        plot_rect = rect.adjusted(pad_left, pad_top, -pad_right, -pad_bottom)
        plot_w, plot_h = plot_rect.width(), plot_rect.height()
        # Grid lines
        for i in range(4):
            y_val = self.y_min + (self.y_max - self.y_min) * i / 3
            y_int = plot_rect.top() + int((y_val - self.y_min) / (self.y_max - self.y_min + 1) * plot_h)
            painter.setPen(QColor("#334155"))
            painter.drawLine(plot_rect.left(), y_int, plot_rect.right(), y_int)
        # Line
        painter.setPen(self.pen)
        for i in range(len(self.points) - 1):
            x1 = plot_rect.left() + int((self.points[i][0] - x_min) / (x_max - x_min + 1) * plot_w)
            y1 = plot_rect.top() + int((self.points[i][1] - self.y_min) / (self.y_max - self.y_min + 1) * plot_h)
            x2 = plot_rect.left() + int((self.points[i+1][0] - x_min) / (x_max - x_min + 1) * plot_w)
            y2 = plot_rect.top() + int((self.points[i+1][1] - self.y_min) / (self.y_max - self.y_min + 1) * plot_h)
            painter.drawLine(x1, y1, x2, y2)
        # Points
        for x, y in self.points:
            px = plot_rect.left() + int((x - x_min) / (x_max - x_min + 1) * plot_w)
            py = plot_rect.top() + int((y - self.y_min) / (self.y_max - self.y_min + 1) * plot_h)
            painter.setPen(self.color)
            painter.setBrush(QColor("#38bdf8"))
            painter.drawEllipse(px - 3, py - 3, 6, 6)
```

## Usage pattern

```python
# In _build_dashboard():
self.temp_chart = ChartWidget(page)
self.temp_chart.set_title("Temperatures")
self.temp_chart.set_color("#38bdf8")
self.temp_chart.set_y_range(0, 100)
self.temp_chart.setAccessibleName("Temperature Chart")
layout.addWidget(self.temp_chart, 3)

# In _on_readings():
self.temp_chart.set_points([(i, r.get("value", 0)) for i, r in enumerate(temps)])
```

## PyQt6 API gotchas

| PyQt6 gotcha | What to do instead |
|---|---|
| `QAction` has no `setStyleSheet()` | `QAction` inherits `QObject`, not `QWidget`. Wrap in a `QWidget`, use `widget.addAction(act)`, add widget to layout. |
| `QAction` cannot be added to a layout directly | Always wrap in `QWidget` first, then add the widget. |
| `setAccessibleName()` does not exist | Use `setObjectName()` for all widget names. |
| `QPainter` drawing is not automatic | Override `paintEvent()` and call it manually when data changes. |
