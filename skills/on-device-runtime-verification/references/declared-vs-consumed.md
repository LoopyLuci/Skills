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

## Ordering bugs the audit tends to expose

Once a value has a real consumer, the next failures are in the wiring around it.
These pass every test that only exercises the happy path:

- **Filter-then-lookup.** Removing an entry from a collection and *then* searching
  that same collection for it guarantees the lookup misses. Read the original
  before filtering.
- **A serializer that drops what the user just edited.** Writing only non-seeded
  entries means an edit to a code-seeded entry is silently discarded on the next
  read. Seeded entries need a written override.
- **A protection flag cleared by its own filter.** Computing the replacement list
  as `all.filterNot { it.id == id } + stored` *before* reading whether that entry
  was protected turns a protected entry into an ordinary, deletable one.

## Audit every client separately

One codebase can carry a desktop and a mobile client whose consumers diverge
completely, so one platform's audit says nothing about the other. Expect the
less-examined client to be worse: the desktop here had 4 of 15 settings inert and
the mobile client 13 of 17.

## Generalise past settings

The same three-way comparison applies to any declared vocabulary - an advertised
command list, a tool registry, a plugin table. Report what is **advertised**,
what is **registered**, and what the loop **handles**. A command accepted and
queued but never handled is accepted-and-dropped.

## The finding is not the deliverable

An audit that ends in a report is half a job. Fix what it found in the same pass,
then report what is fixed and what is not.

The tell is the user asking "what is next?" after a findings list: answering that
with another prioritised list reads as not having listened. Once the question has
been answered in list form, the useful reply is to build the top item and report
the result.

Whatever stays unfixed gets labelled in the UI with the missing capability named
("no animation system in the UI", "TTS is the only audio output") rather than a
generic apology, so a reader can tell whether a setting waits on a permission, a
service, or a feature nobody has built. A control that stores a value nothing
reads is worse than one that admits it.