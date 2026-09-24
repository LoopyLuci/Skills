# Extracting hardcoded strings to Android resources at scale

Retrofitting i18n onto a finished Compose app means hundreds of near-identical edits.
Doing it by hand is slow and error-prone; doing it with a naive regex silently corrupts
copy. This is the approach that worked on a 9-screen app (163 literals → 13).

## 1. Inventory first, with a precise pattern

Only match Compose text *parameters*, and only literals with no interpolation:

```python
PAT = re.compile(r'(Text\(\s*|text\s*=\s*|label\s*=\s*|title\s*=\s*|subtitle\s*=\s*)"([^"\\$]{3,})"')
```

The `[^"\\$]` class is what makes this safe: excluding `$` skips interpolated strings,
which need format arguments and must be handled separately.

Beware false positives. `contentDescription`-adjacent literals like `"activeBorder"`,
`"container"` and `"level"` were **semantics tags and colour keys**, not user copy —
translating them would break tests. Review the inventory before generating anything.

## 2. Generate keys and XML in code, not by hand

```python
def key_for(module, text):
    slug = re.sub(r"[^a-z0-9]+", "_", text.lower()).strip("_")[:40].rstrip("_")
    return f"{module}_{slug}"
```

Module-prefixed keys avoid collisions across feature modules and make the origin obvious.
Derive the module from the path with a regex on `/feature/([^/]+)/src/` — naive
`os.path.dirname` chains give you `kotlin` instead.

**Escaping is mandatory** or `aapt2` fails or mangles output:

```python
t = t.replace("&","&amp;").replace("<","&lt;").replace(">","&gt;")
t = t.replace("'", "\\'")            # apostrophes MUST be escaped
t = re.sub(r"%(?![sd\d])", "%%", t)  # a bare % is read as a format specifier
```

## 3. THE BIG TRAP: multi-line concatenated strings

Compose code wraps long copy like this:

```kotlin
text = "Rules run inside the foreground service. Android may delay " +
    "background triggers while dozing."
```

A regex matching the first literal replaces only that fragment and leaves
`stringResource(R.string.key) + "background triggers while dozing."` — a **broken
sentence in the UI that still compiles**. This produced 7 corrupted strings before it was
caught.

Detect and repair by merging the tail back into the resource, looping until clean because
splits can be 3+ parts:

```python
for _ in range(6):
    found = 0
    for f in files:
        for m in re.finditer(r'stringResource\(R\.string\.(\w+)\)\s*\+\s*\n?\s*"([^"]{2,})"', s):
            # append m.group(2) to the XML entry for m.group(1), drop the concatenation
            found += 1
    if not found: break
```

Always finish with an assertion that zero concatenations remain.

## 4. Imports

`stringResource` is `@Composable`; non-composable call sites (Services, tiles, widgets)
need `context.getString(...)` instead. Add per file:

```python
if "import androidx.compose.ui.res.stringResource" not in s:
    s = s.replace("import androidx.compose.ui.Modifier",
                  "import androidx.compose.ui.Modifier\nimport androidx.compose.ui.res.stringResource", 1)
```

If strings live in a shared module, feature files also need `import <shared>.R`. Verify
imports landed **before** compiling — a missing import fails 100+ sites at once and buries
the real error.

## 5. Counts must be plurals, not concatenation

`"${n} device(s)"` is wrong in English and unfixable in Polish or Arabic:

```xml
<plurals name="count_devices">
    <item quantity="one">%d device</item>
    <item quantity="other">%d devices</item>
</plurals>
```

```kotlin
pluralStringResource(R.plurals.count_devices, n, n)
```

The count is passed **twice** — once to select the form, once as the format argument.

## 6. Prove it, don't assume it

A green build does not prove translatability. Add one partial translation and verify from
the built artifact:

```bash
aapt2 dump resources app.apk | grep -A3 'string/diagnostics_export'
#   () "Export log"
#   (es) "Exportar registro"
```

Then assert it on-device. This test needs no UI, so it runs even behind a keyguard:

```kotlin
val config = Configuration(base.resources.configuration).apply { setLocale(Locale("es")) }
val ctx = base.createConfigurationContext(config)
assertEquals("Exportar registro", ctx.getString(R.string.diagnostics_export))
```

Cover three things: translated keys differ per locale, plurals inflect for 1 vs 3, and
**untranslated keys fall back** to the default rather than crashing or rendering empty. A
partial translation is valid and expected — F-Droid/Weblate translators fill in the rest.

## Result on a real app

| | before | after |
|---|---|---|
| inline literals | 163 | **13** |
| resource lookups | 11 | 168 |
| translatable entries | 44 | 197 |

The 13 remaining are interpolated one-offs and semantics tags, not user-facing copy worth
the churn.
