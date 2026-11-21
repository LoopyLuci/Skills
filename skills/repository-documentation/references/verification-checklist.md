# verification-checklist

Structural checks that a documentation set must pass before delivery. Run in order; each item is reusable across docs sets.

1. **Fence balance.** Every ``` opens and closes (count both, they must match); no unclosed code blocks. Use a balance check with a real parser/language, never ast.parse on .md.
2. **No stub declarations.** No "not implemented", "TODO", or "placeholder" claims that describe the final deliverable as unfinished, unless the doc is explicitly a partial plan.
3. **Cross-reference integrity.** Hyperlinks and file paths referenced in the docs exist. Relative paths resolve from the repo root.
4. **Claim accuracy.** Numbers in the docs (test counts, exit-code semantics, file counts, schema ids) match the actual run. Re-run the project's checks and diff the claims against the output.
5. **Current-state honesty.** The docs state what is not present: submodules not initialized, tests that are mock-only, CI absent, open items in TODO. A doc that describes only the good parts misleads.
6. **Set completeness.** The canonical set is present (unless a documented exception exists), each file names its role, and the docs cross-reference each other.
7. **No incident artifacts.** No dates, ticket IDs, PR numbers, or quoted user text as content. Rules stand without the incident behind them.