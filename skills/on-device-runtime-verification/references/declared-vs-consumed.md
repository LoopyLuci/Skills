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
- **Accessor-only reads.** A consumer that reaches the field through a derived
  method is invisible to a literal name search, so a live setting reports as
  dead. Match the field name *or* a method derived from it.
- **A duplicate registration.** Two handlers for one command name means the
  second silently replaced the first, losing whatever the first returned. The
  tell is a count that disagrees between the declared list and the registered
  set - chase that discrepancy rather than rounding it off.
- **Assert your parser against ground truth** before trusting output: count what
  it found and check one name you already know is there.

## Inert usually means a feature is missing, not a wire

Before offering to wire a gap, establish what kind of work it is. A setting whose
capability has no implementation at all - no boot receiver, no notification
channel, no sound engine - cannot be connected to anything. Those need building,
and they are the items worth surfacing as scope rather than quietly skipping.

Take the labels off only after the behaviour exists: the label is a claim about
the code, so it follows the code, never precedes it.

## Check the extent of a gap before scoping it

The costliest pattern here is calling a gap one feature when one step of reading
the code would have said otherwise. Two mistakes from one session, both mine:

- Reported the mobile client was missing a provider the desktop had. It had it on
  both; the desktop was the one omitting it from its selectable list. The proposed
  work would have built what already existed.
- Called a set of settings "behind" and scoped them as wiring. Reading the code
  showed the capability was absent entirely, so each was a feature to build, not
  a line to connect.

The distinction is the deliverable, so state it explicitly: "the control cannot
select a provider the engine supports" is wiring; "there is no boot receiver at
all" is a feature. Reporting either as "settings that do not work" hides which
one you are asking to build.

The same applies to the audit's own reach: an inert surface on one client says
nothing about the other, and a count of zero from a scanner that never looked at a
directory is a finding about the scanner, not the app.

## A manifest declaration is not a request

A permission listed in the manifest proves nothing. On modern Android the grant
is a runtime decision made by the user in a dialog the app must actually raise,
so a declared permission that is never requested is a control that reads as on
and delivers nothing - the same defect as an unwired setting, one layer further
down and invisible to a scanner that only reads code.

- Audit for `checkSelfPermission` and `rememberLauncherForActivityResult` /
  `requestPermissions`, not just for the manifest line. The manifest is where a
  feature is *planned*; the launcher is where it is *asked for*.
- Request at the moment the feature is relevant - when the user turns the setting
  on, not on first launch. A cold prompt for an app the user has not yet
  understood is declined far more often, and a permanently-declined permission
  cannot be re-asked.
- When the user declines, set the setting back off. Leaving it reading as
  enabled is the one outcome that guarantees the control is lying.
- Where the platform does not gate the capability at all, the blocked branch is
  unreachable on the available hardware. Say so and cover the *decision* with an
  instrumented test rather than claiming the blocked state was observed.

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

## A lookup that misses silently is the worst case

Most defects in this class announce themselves: a control is visibly dead, a test
fails, a log is empty. The expensive ones do not. A lookup that misses and returns
a **default** produces no error, no failing test, and a passing audit - because a
fallback is indistinguishable from success when read by eye.

The signature is a set of records that are supposed to differ but render
identically. When a feature works in principle yet the data never changes what
appears, suspect identity mismatch before suspecting the rendering:

- **Generated identities.** A catalogue whose entries get a random id at
  construction, while the rest of the app references stable names, matches
  nothing. Every lookup silently takes its default branch, so every record looks
  the same no matter what the data says. This hid behind a correct-looking
  feature: the drawing code was fine, the colours were defined, and none of it
  was ever selected.
- **Defaults that hide the miss.** Require the identifier rather than defaulting
  it, so an entry cannot be anonymous, and make the catalogue's ids match the
  naming the rest of the app already uses.
- **Assert the lookup directly.** A unit test that resolves two entries by id and
  asserts they differ in species, colour, or any distinguishing attribute catches
  this with no device at all.

Prove the fix by observing two records that *should* look different actually
looking different in a capture. If both still render the same, the lookup is
still missing - and the fix was in the data layer, not the view.

## A handler registered twice silently shadows the first

Two registrations for one command name is not an error the runtime reports: the
second replaces the first and whatever the first returned is gone. Only the count
disagreement between the declared list and the registered set exposes it, so make
the scanner report duplicates explicitly - harmless at runtime, fatal as drift.

The sibling of filter-then-lookup: a duplicate left in the declared list is inert
config that reads as supported.

## Hollow capability: working plumbing over nothing

An engine can pass every structural check while having nothing to operate on. A
sound engine with working volume, working category routing and two independent
mute switches, and zero audio files, satisfies a consumer audit completely and
ships a slider that moves a number controlling nothing.

- After a consumer audit returns zero, ask what the consumers *act on*. Working
  plumbing over an empty substrate is the same defect one layer down.
- Give the empty substrate a check of its own, and check content rather than
  existence: for generated audio, assert duration band, audible RMS, no clipped
  samples, no long silence, peak low enough not to startle. "The file is present"
  passes for a file of zeroes.
- Generating assets rather than committing binaries of unknown provenance is
  reproducible and reviewable; commit the generator and the output together.

A control can be honestly wired and still hollow. Say which one you fixed.

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

Treat the second asking as a correction, not a prompt for a better list. A
rephrased question is the user saying the previous answer did not land; answering
it a third way is worse than answering it the first way, because it establishes
that the answer is being produced without reference to whether it worked. After
the second time there is only one correct shape: state the single highest-value
item in a sentence, then do it and report what changed. No ranking, no options,
no question at the end.

Two failure shapes to avoid specifically. Offering alternatives and waiting -
"do you want more features or the remaining rough edges polished?" - is the same
stall in a more conversational dress, and it hands back a decision the user has
already made by asking again. And re-ranking from scratch on each asking treats a
repetition as new information when it is the opposite: it is evidence that the
previous ranking was not acted on.

When the autonomous work is genuinely exhausted, say so plainly and name what is
blocked on the user - credentials, a signing key, a decision about scope. "I have
nothing left that does not need your input, and here is exactly what that input
is" is a real answer that ends the loop. Repeating a list as filler after the work
runs out is the thing the repetition is complaining about.

Keep going without waiting for a "go" once the pattern is established. Each cycle
should read as one item chosen, built, and verified, with the reply leading on
what changed rather than on what might be next. The loop only breaks when the
report says the same thing twice, so make each report carry something that could
not have been said before - a number that moved, a defect class found, a thing
that was hollow. If a cycle produces no such thing, the choice of item was wrong,
not the format of the reply.

## Gate only what nothing else covers

A CI gate that fires for a finding the UI already discloses is noise, and noise
trains people to ignore the gate. Fail on what no other report catches: a
command advertised but unable to run, a declared list that disagrees with the
code. Report the rest and exit zero.

Whatever stays unfixed gets labelled in the UI with the missing capability named
("no animation system in the UI", "TTS is the only audio output") rather than a
generic apology, so a reader can tell whether a setting waits on a permission, a
service, or a feature nobody has built. A control that stores a value nothing
reads is worse than one that admits it.