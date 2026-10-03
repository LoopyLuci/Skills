# Declared versus consumed

The defect class this harness exists to catch: a surface is declared, rendered,
and apparently working, and nothing reads the value.

## The rule

A rendered control, a save method, or a passing test proves nothing if nothing
reads the value. Classify every surface into three states, never two:

- **Live** - read and honoured.
- **Read-only mirror** - the app writes it at startup to reflect real state, so
  it shows the truth but changing it does nothing.
- **Inert** - nothing reads it.

The middle state is the one people miss, and labelling it "not wired up" is
simply incorrect.

## Audit procedure

1. Derive the classification mechanically - a scanner that finds readers and
   writers per name beats a hand-maintained list.
2. Check the derived lists against each other for overlap.
3. Gate the scan in CI so drift fails cheaply.
4. Print the full classified list, not just a verdict. A clean result from a
   broken parser is worse than a failure.

## Your scanner is itself a defect

The first version of a scanner reports everything healthy. Expect these:

- **Plumbing counted as a consumer.** A repository, viewmodel, and settings
  screen that move a value between UI and storage are storage, not behaviour.
  Counting them hides the entire class you were sent to find. Exclude them.
- **Reading the forwarder instead of the dispatch table.** Control receivers and
  route handlers typically parse and delegate; the command list and handlers
  live in a separate registration object. Reading the forwarder yields "zero
  commands" and looks like a result.
- **Assert your parser against ground truth** before trusting output: count what
  it found and check one name you already know is there.

## Writers must reach durable storage

A writer landing in an in-memory map is a writer that does not exist: the value
reads back, reports success, and dies at restart.

- Ask of every write path whether it reaches the store the app restarts from.
- **An ack of `success` or `queued` is a claim, not evidence.** A handler that
  records a request and returns `queued` without calling the service is the same
  defect.

## Reached is not the same as honoured

Two breaks sit downstream of a value reaching a call site, invisible to a scanner
that stops there:

- **A built-in default that shadows user configuration.** Resolution order
  decides whether the setting is consulted at all; a hardcoded default first
  makes the setting decorative. Audit the precedence chain.
- **A display function that disagrees with the request path.** Reporting and
  sending must resolve identically, or the UI shows an endpoint the app never
  calls. Extract one resolver, use it in both.
- **Wire shapes differ between providers.** A field name correct for an
  OpenAI-compatible endpoint may be ignored by another runtime, which expects it
  nested or renamed. Check the target's actual contract.