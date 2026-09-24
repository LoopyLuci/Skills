# Model Architectures — Full Specifications

## ColorHarmonyModel

**Purpose:** Generate WCAG-compliant color palettes from brand color + context.

**Architecture:**
```
Input(33) → Dense(48, relu) → Dense(96, relu) → Dropout(0.15) → Dense(48, relu) → Dense(15, sigmoid)
```

**Input encoding (33 dims):**
- brand_colors: 3 dims (R, G, B normalized 0-1)
- mood: 10 dims one-hot (professional, playful, elegant, bold, calm, energetic, warm, cool, minimal, vibrant)
- industry: 20 dims one-hot (tech, health, finance, education, retail, food, travel, art, sports, music, news, government, nonprofit, realestate, automotive, fashion, beauty, gaming, legal, other)

**Output (15 dims):**
- 5 colors × 3 RGB = 15 values (0-1, multiply by 255 for hex)
- Order: primary, secondary, accent, background, text

**Training:**
- Data: `DataGenerator.generate_color_data(n)`
- Loss: MSE
- Epochs: 20-30
- Batch: 32
- LR: 0.001

---

## LayoutGenerationModel

**Purpose:** Predict optimal section positions, spacing, and alignment.

**Architecture:**
```
Input(33) → Dense(64, relu) → Dropout(0.2) → Dense(128, relu) → BatchNorm(128) → Dense(64, relu) → Dense(130, linear)
```

**Input encoding (33 dims):**
- section_types: 20 dims one-hot (Navbar, Hero, Features, CTA, Pricing, Stats, Testimonials, FAQ, Footer, etc.)
- content_length: 10 dims (normalized section content lengths)
- device_type: 3 dims one-hot (desktop, tablet, mobile)

**Output (130 dims):**
- positions: 100 dims (10 sections × 10 grid positions)
- spacing: 20 dims (padding/margin values)
- alignment: 10 dims (left/center/right)

---

## TypographyPairingModel

**Purpose:** Select optimal heading + body font pairing.

**Architecture:**
```
Input(45) → Dense(64, relu) → Dense(128, relu) → Dropout(0.2) → Dense(64, relu) → Dense(100, softmax)
```

**Input encoding (45 dims):**
- personality: 15 dims (brand personality traits)
- content_type: 10 dims (blog, landing, portfolio, ecommerce, etc.)
- language: 20 dims (language script categories)

**Output (100 dims):**
- heading_font: 50 dims softmax over font list
- body_font: 50 dims softmax over font list

**Font list (20 fonts):**
Inter, Roboto, Open Sans, Lato, Montserrat, Poppins, Playfair Display, Merriweather, Nunito, Raleway, PT Serif, Source Sans Pro, Oswald, Ubuntu, Rubik, Work Sans, Fira Code, Space Grotesk, DM Sans, Plus Jakarta Sans

---

## PageSpeedModel

**Purpose:** Predict page load time and Lighthouse score.

**Architecture:**
```
Input(5) → Dense(32, relu) → Dense(64, relu) → Dropout(0.2) → Dense(32, relu) → Dense(2, sigmoid)
```

**Input encoding (5 dims):**
- dom_size: 1 dim (normalized 0-1, divide by 1000)
- script_size: 1 dim (normalized 0-1, divide by 1000000)
- image_count: 1 dim (normalized 0-1, divide by 50)
- css_rules: 1 dim (normalized 0-1, divide by 1000)
- third_party: 1 dim (normalized 0-1, divide by 10)

**Output (2 dims):**
- load_time_ms: sigmoid × 10000
- lighthouse_score: sigmoid × 100

**Grade mapping:**
- A: ≥90, B: ≥80, C: ≥70, D: ≥60, F: <60

---

## AccessibilityComplianceModel

**Purpose:** Detect WCAG 2.1 violations.

**Architecture:**
```
Input(280) → Dense(128, relu) → Dropout(0.2) → Dense(64, relu) → Dense(30, sigmoid)
```

**Input encoding (280 dims):**
- 10 real features (contrast_ratio, alt_text_coverage, aria_usage, semantic_html_score, keyboard_navigable, focus_indicators, form_labels, heading_hierarchy, link_text_quality, color_independence)
- 270 zeros (padding for future features)

**Output (30 dims):**
- 30 violation type probabilities

**Violation types (30):**
missing_alt, low_color_contrast, missing_labels, no_keyboard_access, missing_focus, poor_heading, link_text, color_only, missing_lang, autoplay_media, small_touch_target, no_captcha_alt, time_limit, no_skip_link, inconsistent_nav, missing_title, duplicate_ids, table_headers, frame_titles, blinking_content, pdf_accessible, svg_labels, animation_pause, text_resize, error_identification, error_suggestion, error_prevention, name_role_value, language_parts, consistent_nav

**WCAG level mapping:**
- AAA: compliance ≥ 0.9
- AA: compliance ≥ 0.7
- A: compliance < 0.7

---

## CodeCompletionModel

**Purpose:** Predict next token in HTML/CSS/JS code.

**Architecture:**
```
Input(50 tokens) → Embedding(vocab_size, 128) → LSTM(128, 256) → Dense(256, vocab_size, softmax)
```

**Input encoding:**
- 50 token IDs (hashed from code context)
- Embedding: 1000 × 128 matrix

**Output:**
- Probability distribution over 1000 token vocabulary

**Training:**
- Data: `generate_code_corpus(n)` from code_corpus.py
- Templates: 10 HTML + 10 CSS + 10 JS templates
- Tokens hashed to IDs via `hash(t) % vocab_size`
- Loss: crossentropy
- Epochs: 10

---

## UserIntentPredictionModel

**Purpose:** Predict user's next action based on current state.

**Architecture:**
```
Input(324) → Dense(128, relu) → Dropout(0.2) → Dense(64, relu) → Dense(50, softmax)
```

**Input encoding (324 dims):**
- current_state: 100 dims (canvas state, selected section, etc.)
- history: 200 dims (last 20 actions × 10 dims each)
- time_of_day: 4 dims one-hot (morning, afternoon, evening, night)
- project_type: 20 dims one-hot

**Output (50 dims):**
- 50 possible actions (add_section, delete_section, move_up, move_down, change_text, change_color, change_font, add_image, add_button, preview, export, save, undo, redo, add_page, delete_page, switch_theme, open_settings, run_ai, format_code, comment_code, find_replace, add_form, add_table, add_video, add_map, add_social, add_nav, add_footer, add_header, add_hero, add_features, add_pricing, add_testimonials, add_faq, add_cta, add_gallery, add_team, add_stats, add_timeline, add_accordion, add_tabs, add_modal, add_tooltip, add_badge, add_alert, add_divider, add_spacer, add_code)

---

## Training Pitfalls (Lessons Learned)

1. **Gradient explosion with synthetic data**: Always clip gradients to [-1.0, 1.0] before SGD update. Without clipping, NaN weights appear within 5-10 epochs.

2. **Crossentropy loss returns negative values**: Cast to float: `float(-np.mean(np.sum(target * np.log(pred + 1e-8), axis=-1)))`. Don't be alarmed by negative loss.

3. **Feature dimensions must match exactly**: Input layer dim must match feature vector size. Use `np.concatenate` carefully and verify shapes.

4. **Code Completion requires real templates**: Random data produces garbage. Use `generate_code_corpus()` with actual HTML/CSS/JS templates.

5. **Accessibility model output is 30 dims, not 33**: WCAG level is derived from compliance score (1 - mean(output)), not from separate output neurons.

6. **BatchNorm before final layer**: Layout model uses BatchNorm(128) before final Dense — helps stabilize training.

7. **Persistence required**: Call `save_model(name, layers)` AFTER training. Weights are lost on exit otherwise.

## GUI Integration Pattern

```python
# In WebBuilderWindow method
def _generate_color_palette(self):
    from webbuilder.ml_engine.models import MLModelFactory
    factory = MLModelFactory()
    model = factory.get('color_harmony')
    palette = model.generate('#3b82f6', 'professional', 'tech')
    # Show in QMessageBox or apply to project
```

**Factory pattern:** `MLModelFactory.get(name)` returns cached instance. Call `MLModelFactory.load_all()` at startup to load trained weights.