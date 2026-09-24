# Native AI Systems for Desktop App Builders

This reference covers the native AI/ML systems built into WebBuilder that operate without any external APIs or dependencies.

## Architecture

All AI systems are built from scratch using only NumPy — zero external ML framework dependencies (no TensorFlow, PyTorch, JAX, etc.). This means:

- **No API keys required** — everything runs locally
- **No internet connection needed** — fully offline-capable
- **Deterministic** — same input always produces same output (with fixed seed)
- **Trainable in-app** — users can train models from the GUI
- **Visual monitoring** — real-time loss curves, weight distributions, activation maps

## Neural Network Framework (`neural/`)

### Components
- **Layers**: Dense, Conv2D, MaxPool2D, Flatten, Dropout, BatchNorm, LayerNorm, ResidualBlock
- **Activations**: ReLU, LeakyReLU, Sigmoid, Tanh, Softmax, GELU, SiLU, Mish
- **Losses**: MSE, CrossEntropy, BCE, Huber
- **Optimizers**: SGD (with momentum), Adam, AdamW, RMSprop
- **Model & Trainer**: Full forward/backward propagation, mini-batch training

### Usage Pattern
```python
from neural import Dense, ReLU, Adam, Model, CrossEntropyLoss

layers = [
    Dense(64, 32),
    ReLU(),
    Dense(32, 16),
    ReLU(),
    Dense(16, 10),
    Softmax()
]

model = Model(layers, CrossEntropyLoss(), Adam(lr=0.001))
trainer = Trainer(model, batch_size=32, epochs=100)
trainer.fit(x_train, y_train, x_val, y_val)
```

### Training Dashboard GUI
```python
# Real-time loss curve
def update_loss_curve(self):
    pixmap = QPixmap(800, 200)
    painter = QPainter(pixmap)
    # Draw axes, then loss curve from self.training_losses
    for i in range(1, len(self.training_losses)):
        painter.drawLine(x1, y1, x2, y2)
    self.loss_canvas.setPixmap(pixmap)

# Weight distribution scatter plot
# Activation map heatmap
```

## Diffusion Model (`generators/image/`)

### Components
- **VAE**: Encoder → latent distribution → Decoder with reparameterization trick
- **DDPM**: Forward diffusion, reverse denoising, U-Net architecture
- **Noise Scheduler**: Manages noise schedule for diffusion process
- **Procedural Generator**: Gradients, patterns, icons (no neural net needed)

### Usage Pattern
```python
from generators.image import VAE, DiffusionModel, ProceduralImageGenerator

# VAE for compression/generation
vae = VAE(latent_dim=128, image_size=64)
z = vae.encode(images)
reconstructed = vae.decode(z)

# Diffusion for image generation
diffusion = DiffusionModel(num_timesteps=1000, image_size=64)
generated = diffusion.generate(num_images=4, num_steps=50)

# Procedural for icons/patterns
gen = ProceduralImageGenerator()
icon = gen.generate_icon(64, 'star', [255, 215, 0])
pattern = gen.generate_pattern(256, 256, 'checkerboard')
```

### Procedural Generation GUI
```python
def update_generator(self):
    gen_type = self.gen_type.currentText()
    scale = self.scale_slider.value()
    octaves = self.octaves_slider.value()
    seed = int(self.seed_input.text())
    
    pixmap = QPixmap(600, 400)
    painter = QPainter(pixmap)
    
    if gen_type == 'Perlin Noise':
        for y in range(0, 400, 4):
            for x in range(0, 600, 4):
                n = self.perlin_noise(x / scale, y / scale, octaves, seed)
                c = int((n + 1) * 127.5)
                painter.fillRect(x, y, 4, 4, QColor(c, c, c))
    
    self.gen_preview.setPixmap(pixmap)
```

## Layout Generation (`generators/layout/`)

### Components
- **Grid System**: CSS Grid-like functionality
- **Constraint Solver**: Backtracking with forward checking
- **Genetic Engine**: Tournament selection, elitism, adaptive convergence
- **Fitness Function**: Multi-objective scoring based on 8 design principles
- **Mutation/Crossover**: 5 mutation operators + 4 crossover operators

### Usage Pattern
```python
from generators.layout import GridSystem, ConstraintSolver, GeneticEngine

grid = GridSystem(columns=12, rows=8, gutter=16)
solver = ConstraintSolver(grid)
engine = GeneticEngine(population_size=100, generations=50)

layout = engine.optimize(sections, constraints)
```

## Color & Typography AI (`ai/`)

### Components
- **ColorAI**: HSL-based palette generation, WCAG contrast scoring
- **TypographyAI**: Font pairing + modular scale generation
- **CopyGenerator**: Markov chain + template-based copywriting
- **NativeAIBuilder**: Complete project generation from a single prompt

### Usage Pattern
```python
from ai import NativeAIBuilder

builder = NativeAIBuilder()

# Generate complete project from description
project = builder.generate_project(
    project_type='saas',
    company_name='TaskFlow',
    audience='teams',
    style='modern'
)

# Generate specific assets
palette = builder.color_ai.generate_palette('#3b82f6', 'complementary')
typography = builder.typography_ai.generate_system(base_size=16, scale_name='major_third')
copy = builder.copy_generator.generate_hero('TaskFlow', 'teams')
```

## Plugin Architecture (`plugins/`)

### Components
- **PluginLoader**: Loads plugins from directories or files
- **PluginRegistry**: Manages plugin lifecycle
- **PluginAPI**: Interface for plugins to interact with core
- **Hook System**: Event-driven extension points
- **PluginOrchestrator**: High-level API combining all components

### Extension Points
- `component:register` — Register custom components
- `generator:register` — Register custom generators
- `exporter:register` — Register custom exporters
- `tool:register` — Register custom tools

## Integration Pattern for Desktop Apps

```python
class WebBuilderApp(QMainWindow):
    def __init__(self):
        # Initialize AI systems
        self.ai_builder = NativeAIBuilder()
        self.vae = VAE(latent_dim=128)
        self.diffusion = DiffusionModel(num_timesteps=100)
        self.color_ai = ColorAI()
        self.typography_ai = TypographyAI()
        
    def generate_full_project(self):
        """One-click project generation."""
        description = self.get_description_from_user()
        project = self.ai_builder.generate_project(
            project_type=self.detect_type(description),
            company_name=self.extract_name(description),
            audience=self.detect_audience(description)
        )
        self.load_project(project)
    
    def generate_image(self, width, height, image_type):
        """Generate image using diffusion or procedural."""
        if image_type == 'photo':
            return self.diffusion.generate(1, 50)[0]
        else:
            return self.procedural.generate_gradient(width, height, colors)
```

## Key Design Principles

1. **Deterministic by Default**: All random operations accept a seed parameter
2. **Lazy Loading**: Heavy models (VAE, Diffusion) are loaded only when needed
3. **Progressive Enhancement**: Start with procedural, upgrade to neural when needed
4. **Visual Feedback**: Every AI operation has a visual representation in the GUI
5. **Trainable In-App**: Users can train models from the Training tab with real-time monitoring

## Performance Considerations

- Neural networks are CPU-only (NumPy) — expect ~10-100x slower than GPU
- For production use, consider exporting to ONNX or TensorFlow Lite
- Procedural generation is always fast (<16ms for 60fps)
- Cache generated assets to avoid regeneration
