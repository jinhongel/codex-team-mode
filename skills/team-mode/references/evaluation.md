# Evaluate Team Mode

Read this reference only when the user asks to assess Team Mode's routing, Agent profiles, models, reasoning effort, cost, or practical value.

## Establish The Trial

1. Record the root task ID, repository or artifact baseline, acceptance checks, and installed role-to-model mapping.
2. Verify actual child runtime metadata from local traces: `agent_role`, `model`, `effort`, and effective sandbox. Configuration files alone do not prove runtime selection or isolation.
3. Treat a custom profile's TOML effort as the intended setting unless runtime trace proves an override. Passing `reasoning_effort` to one spawn does not by itself establish a controlled A/B trial; use isolated sessions or separately configured profiles when comparing effort levels.
4. Choose the smallest useful delegation. Keep a comparable slice in the main thread when the goal includes comparing delegation with direct work.
5. Give different Agents independent slices or one stable writer boundary. Do not create duplicate work solely to produce a benchmark.

## Measure What Happened

Resolve `scripts/usage_by_model.py` relative to the installed Team Mode Skill directory and run it with the environment's Python executable. For the active task use `--task-id current --by-agent --by-session --json`.

Use per-session time, terminal status, depth, and effective sandbox as trace evidence; continue to judge artifact quality and rework manually. Record:

- artifact correctness and requirement coverage;
- source completeness for fresh-context children;
- whether the child brief was self-contained and bounded;
- main-thread context avoided;
- briefing, waiting, inspection, and rework cost;
- time to a usable return;
- wall-clock effect from useful parallelism;
- uncached input, cached input, output, reasoning output, and estimated credits by session;
- permission or runtime differences from the configured profiles;
- transient failures, partial shared artifacts, retries, and duplicated review.

Do not treat token minimization as the objective. The preferred setting is the one that gives reliable quality with a reasonable safety margin and acceptable rework, not necessarily the lowest effort that can sometimes pass. Token and credit data are diagnostic inputs, especially useful for identifying obviously wasteful routing or repeated failed work.

Credit estimates are not billing truth. The script uses a static official rate-card snapshot; included-plan allowances, account-specific metering, promotions, Fast mode, and later rate changes can differ. Verify the current official rate card when the number matters, and treat Codex `/usage` as authoritative for account limits and actual metering.

A child's opinion that its spawn was useful is not primary evidence; judge the returned artifact, the inspection needed, and task-scoped usage. Likewise, a child recommending another Reviewer does not establish review value. If the main thread cannot state a neutral unresolved risk, exact evidence, passed checks, excluded revalidation, and a bounded stop condition, count the extra Reviewer as avoidable routing rather than mandatory assurance.

Treat `terminal_status=completed` only as evidence that the local trace contains `task_complete`; it does not prove correctness or a useful final report. Inspect interrupted or incomplete sessions before retrying, and record any usage that produced no usable return.

Compare `effective_sandbox` with the configured profile. When a parent live override produces broader permissions for an Explorer or Reviewer, their read-only boundary is instructional rather than OS-enforced; do not count that route as security isolation.

Attribute missing facts before blaming the model. When a fresh-context child correctly reports that required evidence was not provided, count the omission as briefing cost; do not treat invented completion as the preferred behavior.

When a child fails, inspect the shared target before counting the attempt as lost or retrying. Record recoverable artifacts separately from the missing final report.

## Interpret The Roles

- `Explorer` defaults to Luna Medium. Keep it there when bounded search, tracing, and evidence compression are reliable. Do not mechanically raise it for ordinary discovery. If the task becomes architecture-defining, high-consequence, or too broad for bounded evidence gathering, return the judgment to the main thread rather than turning Explorer into a substitute architect.
- `Executor` defaults to Luna Max. This is intentionally conservative for mutable implementation: low rework and implementation completeness are prioritized over tuning to the minimum sufficient effort. Consider lowering it only when repeated representative tasks show High preserves the same quality and verification profile with materially less waste.
- `Reviewer` defaults to Terra High. This gives independent review additional reasoning margin for counterexamples, regressions, requirement coverage, and weak assumptions. Consider Medium only when repeated review tasks show equivalent finding quality and coverage.
- The optional `default` guard uses Luna Low because it performs no work beyond refusing invalid dispatch. Raising its effort does not provide a meaningful quality margin.

Use one Reviewer for a concrete unresolved risk by default. Add another only for a genuinely independent risk with clear expected value. Do not infer the need for multiple Reviewers from file count alone.

Evaluate an Executor inside the real controlled workflow, including the candidate, main-thread inspection, and bounded repair. Strong main-thread acceptance can close observable implementation gaps cheaply. It cannot reliably compensate for a plausible but product-weaker architecture that passes shallow checks, so keep novel architecture, weak or subjective verification, and high-consequence rollback or security judgment in the main thread.

Prefer changing routing thresholds, brief quality, or task boundaries before changing models. Change a profile when repeated task-scoped evidence shows the current setting is materially insufficient or unnecessarily wasteful—not merely because a lower or higher reasoning level exists.

## Report The Result

For each spawn, record role, runtime model and effort, purpose, outcome quality, rework, task-scoped usage, and keep/change verdict. Separate confirmed findings from one-off impressions and note that local logs omit unavailable or ephemeral sessions.
