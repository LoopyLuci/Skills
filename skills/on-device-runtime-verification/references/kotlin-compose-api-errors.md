# Kotlin and Compose API-shape errors

Every rule here cost a full Gradle cycle in one session. All are the same class:
the compiler rejects a call because the shape of the API is not what you assumed.
They cluster in Kotlin/Compose because the type system infers through lambdas,
so a wrong guess surfaces as a confusing error far from the guess.

The general move: when a call fails to resolve, read the declaration rather than
guessing the next variant. Guessing produced several consecutive failures from
one wrong assumption.

## Lambdas and function references

- **A lambda bound to a `val` has no label.** `return@work` fails to resolve
  inside `val work: () -> Unit = { ... }`, because the label for a lambda
  expression only exists when the lambda is passed directly as an argument. Use a
  local `fun work() { ... }` instead: it is labelled by its own name and reads
  better anyway.
- **A local function is referenced, not invoked, when passed on.**
  `Thread(work)` compiles as an invocation attempt and fails; `Thread(::work)`
  passes the reference.
- **An inferred lambda parameter type blocks explicit annotation.** `{ s: AppSettings -> ... }`
  inside a `when` branch can fail to infer where the expected type is nullable;
  extracting a named helper with an explicit parameter type is more reliable than
  annotating in place.
- **The elvis operator can bind to the last branch of a `when`** rather than to
  the whole expression. Bind the `when` to a `val` first, then null-check it.

## Compose

- **Wildcard imports matter.** Narrowing `import androidx.compose.runtime.*` to a
  single symbol removes `remember`, `LaunchedEffect`, and `mutableStateOf` and
  produces a cascade of unrelated unresolved-reference errors that look like the
  new code is wrong. When an import is edited, check what else it supplied.
- **An experimental API needs the opt-in at each composable that uses it**, not
  once at the file.
- **A `Modifier` chain with a no-op step is dead code.** `scale(1f, 1f)` next to a
  real `scale(...)` usually means an abandoned idea; a computed value left unused
  nearby is the same tell. Delete both rather than shipping them.

## Framework types are not what they look like

- **A Flow of preferences is not the model.** A datastore's `data` yields
  `Preferences`, not the parsed data class, so reading a field from it fails. Map
  through the same reader the public flow uses.
- **Platform-typed Android properties are nullable to the compiler.** `filesDir`
  is `File?`, so `File(context.filesDir)` does not resolve. Name the type
  explicitly, with a fallback path, rather than wrapping it.
- **The parameter type decides the overload.** A handle-taking loader takes the
  handle; the offset form takes a different type and will not accept it.

## Testing without adding a runtime

- **Inject the directory, not the context.** A class whose only Android dependency
  is "where the files live" takes a `java.io.File` as its primary constructor and
  exposes a context convenience factory. It then tests on a plain JVM with a temp
  folder rule, avoiding a full Android test runtime for logic that never touches
  the framework.
- **A secondary constructor cannot take the platform type the primary does not.**
  Make the simple type primary and offer the platform constructor as a factory.

## Instrumented tests replace impossible simulations

Some behaviour cannot be exercised by broadcasting an intent: a protected system
action is not delivered to a backgrounded app, and a real device reboot that
produces no log proves nothing about the code. Write an instrumented test that
constructs the component and asserts the branch it takes.

- **Drive the branch, not the delivery.** Assert the decision the component makes
  for each input, including the negative case.
- **Wait for the component's own async work** before asserting, or the test races
  the thing it is checking.
- **A framework handle can be absent when invoked directly.** `goAsync()` returns
  null outside a platform-delivered broadcast, and dereferencing it fails on a
  worker thread where no log shows it. Guard it and run inline when missing,
  which is also what makes the component testable at all.