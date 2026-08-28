---
name: team-mode
description: Proactively decompose and coordinate substantial development, research, analysis, planning, document, data, and content work with the smallest useful set of custom subagents. Use when delegation, context isolation, bounded execution, safe parallelism, or fresh review has clear value. Keep unresolved decisions and final acceptance in the main thread. Do not use for casual or simple tasks.
---

# Team Mode

Lead the task in the main thread. Use subagents only when their expected speed, context, verification, isolation, or independent-judgment benefit clearly exceeds briefing, inspection, waiting, rework, token, and conflict cost. Do not optimize model effort to the theoretical minimum: prefer enough reasoning margin to reduce rework when the role benefits from it.

Team Mode is a routing guide, not a mandatory pipeline. The main thread owns unresolved decisions and final acceptance; subagents handle focused evidence gathering, bounded implementation, and independent review.

## Dispatch Gate

Every `spawn_agent` call must explicitly pass `agent_type` as exactly one of `Explorer`, `Executor`, or `Reviewer`.

- Never omit `agent_type` and never pass `default`. The `default` profile is a fail-closed dispatch guard, not a working Agent.
- Never use `task_name` to select a profile; it only labels the child thread.
- If the intended custom profile is unavailable, keep the work in the main thread or repair the profiles. Do not silently use a generic child.
- If a child returns the dispatch-guard message or its trace shows `default` / `subagent/unknown`, reject its output and respawn only after selecting the intended custom profile explicitly.

Read [references/custom-agents.md](references/custom-agents.md) only when installing, repairing, or verifying the three working profiles and the `default` guard. The controlled onboarding self-test described there is the only time Team Mode deliberately omits `agent_type`.

## One-Time Onboarding

Do not inspect Agent files, load onboarding instructions, or repeat setup explanations during normal Team Mode routing. Treat the active `spawn_agent.agent_type` choices and descriptions as runtime readiness evidence. When all three working profiles are available and `default` is described as the dispatch guard, skip onboarding without mentioning it.

Only read [references/custom-agents.md](references/custom-agents.md) and start onboarding when a required profile or guard is unavailable, or when the user explicitly asks to install, repair, verify, move, disable, or customize them. Get authorization before writing personal or project configuration.

## Required Rules

- When this Skill activates, immediately send one brief commentary update in the user's language, prefixed with `👾`. For Chinese, say `👾 已开启小队模式。`; translate naturally for other languages. Announce it once per task, not before every subagent call.
- Activating Team Mode does not require spawning any subagent. Keep work in the main thread whenever delegation does not provide a clear net benefit.
- For substantial tasks, perform a brief decomposition pass. Decomposition is analysis, not a requirement to delegate.
- Dispatch independent slices in parallel only when the combined wall-clock, context, isolation, or verification gain clearly exceeds briefing, inspection, waiting, rework, token, and conflict cost. Merely having two independent slices is not enough.
- After unresolved architecture, product, editorial, safety, scope, interface, data-model, state-flow, and acceptance decisions are fixed, identify bounded, independently verifiable implementation slices. Delegate useful slices to `Executor`; keep unresolved or weakly verifiable decisions in the main thread.
- Before each spawn, identify one material benefit: useful parallelism, context isolation, bounded execution, evidence gathering, or independent judgment. If that benefit is marginal or speculative, keep the slice in the main thread.
- Keep all routing and fan-out in the main thread. Under standard Team Mode, children never spawn descendants; they return evidence, artifacts, or blockers to the parent.
- Use `fork_turns="none"` by default for new subagents and always for a new `Reviewer`. Reuse an existing child only when continuity of the same bounded workstream is more valuable than fresh context.
- Keep unresolved user intent, product, editorial, architecture, interface, data-model, state-flow, safety, scope, and acceptance decisions, plus final acceptance, in the main thread.
- Assign one current writer to every file, shared artifact, interactive session, or mutable-system boundary. Parallel writers require disjoint, stable ownership. When ownership changes, stop or complete the previous writer and state the handoff before the new writer starts.
- Inspect the actual artifacts, sources, diffs, and verification output before accepting delegated work. A child reporting completion is not acceptance evidence by itself.
- If a child errors, times out, or is interrupted, inspect shared artifacts and trace evidence before retrying. Recover usable work instead of automatically repeating it. Retry a transient failure at most once unless new evidence justifies another attempt.
- Treat the parent task's live permission mode as the effective child permission. Do not infer read-only isolation from TOML alone; verify runtime permissions when isolation matters.

When the user asks to evaluate Team Mode itself, compare models or reasoning effort, or measure whether delegation was worthwhile, read [references/evaluation.md](references/evaluation.md) before designing the trial.

## Dispatch Contract

Before every spawn, make the brief self-contained with these labeled fields:

- `Outcome`: the independently finishable result the child must return.
- `Benefit`: the material advantage over keeping this slice in the main thread.
- `Sources`: every path, URL, dataset, or raw artifact required for factual work.
- `Scope`: allowed reads or writes, ownership, exclusions, and external-action authority.
- `Checks`: acceptance criteria and validation the child owns.
- `Stop when`: the bounded completion, blocker, or evidence threshold that ends the turn.
- `Return`: the concise report or artifact format expected by the parent.

Do not spawn while `Outcome`, required `Sources`, `Scope`, `Checks`, or `Stop when` is missing. `Benefit` must be real rather than boilerplate; if the parent cannot name a meaningful benefit, keep the slice in the main thread. Keep a slice in the main thread when it is not independently finishable.

For a `Reviewer`, also name one concrete `Unresolved risk`, the exact `Evidence` to inspect, `Checks already passed`, and `Do not repeat`. Do not tell the Reviewer the prior debate, author, suspected findings, or desired verdict. Require a usable partial verdict if the stop condition arrives before exhaustive review.

## Route The Work

- `Explorer`（Luna Medium）: use for non-trivial read-only discovery that benefits from isolated context. Give it exact sources and a bounded evidence question. Medium is intentional because most Explorer work is search, tracing, and evidence compression rather than final design judgment.
- `Executor`（Luna Max）: use for localized or substantial bounded execution only after the main thread fixes unresolved architecture, product, safety, scope, interfaces, data models, state flows, and acceptance criteria. Max is intentionally conservative: implementation quality and low rework take priority over minimizing reasoning usage.
- `Reviewer`（Terra High）: use fresh read-only context when independent review has clear value. High gives extra reasoning margin for counterexamples, regression risk, requirement coverage, and weak assumptions without turning the Reviewer into a second main architect.
- Main thread: keep novel architecture, ambiguous requirements, high-consequence security or rollback judgment, weak or subjective verification, broad cross-system decisions, and any task whose correct outcome cannot be bounded reliably for a child.

If an Explorer or Reviewer discovers that the assigned question has become architecture-defining, high-consequence, or too broad for a reliable bounded verdict, return evidence and uncertainty to the parent instead of silently expanding authority. Do not create a proliferation of stronger role variants solely to cover every complexity level; escalate the judgment to the main thread.

## Independent Review

Use `Reviewer` according to risk and verification difficulty, not by file count alone.

A fresh review is usually valuable when one or more of these applies:

- shared APIs, state, persistence, concurrency, authorization, security, migration, compatibility, or other cross-cutting behavior changed;
- the change is difficult to verify deterministically or a plausible false success would be costly;
- the diff is conceptually dense enough that the main thread could reasonably miss regressions, unsupported assumptions, dead code, or missed reuse;
- implementation or tests exposed meaningful uncertainty;
- the user explicitly asks for independent review, cleanup, simplification, or high confidence.

Use one risk-focused Reviewer by default. Add another fresh Reviewer only when there is a genuinely independent unresolved risk or review lens whose expected value exceeds the additional briefing and inspection cost. Do not launch separate code-quality, performance, and reuse reviewers merely because a change crossed a file-count threshold.

When code quality, performance, or reuse is the actual unresolved risk, assign that lens explicitly. Reviewers report severity-ordered findings with paths, evidence, and the smallest behavior-preserving repair direction. They do not edit, format, commit, or repeat checks that already passed. The main thread validates findings, applies or delegates accepted repairs, and reruns relevant checks.

## Coordinate The Work

- Start with the smallest useful team. Parallelize genuinely independent exploration, analysis, tests, implementation, or review only when the net benefit is clear; do not duplicate work merely to keep Agents occupied.
- For coding tasks, test split points such as independent modules, implementation versus tests, code versus documentation, separate platform targets, and separate verification surfaces, but keep work serial when ownership or coordination cost makes that safer or simpler.
- Before execution, state plainly what the result should be, what may be touched, what must remain unchanged, and how completion will be checked. Revise these requirements if new evidence conflicts with them.
- Verify in proportion to risk. Use independent review for complex, consequential, or difficult-to-check results rather than for every task.
- Reuse passed checks as evidence. Do not ask another Agent to repeat broad validation unless the integrity or relevance of those checks is itself the unresolved risk.

When a task depends on live UI, browser, device, or other interactive state that code inspection and automated checks cannot prove reliably, read [references/interactive-testing.md](references/interactive-testing.md). Do not load it for tasks that can be verified from code.

## Context And Reuse

- Give each new subagent a compact, self-contained brief containing only the objective, relevant sources or paths, scope, authority, exclusions, intended result, required checks, and return format. Never copy credentials into it.
- With `fork_turns="none"`, assume the child knows nothing from the parent conversation. Name every source artifact required for factual claims; if a source is missing, either provide its path, narrow the child to collecting that evidence, or keep the source-dependent slice in the main thread.
- Reuse an existing Explorer or Executor when new work belongs to the same bounded workstream and its prior context remains useful. Send only the new objective and changed constraints.
- Start fresh when prior context is stale or noisy, the role or authority changes, or independent judgment matters.
- Reuse a Reviewer only to clarify its existing report. Use a fresh Reviewer for a new review or for checking revised work.
- Do not give an Explorer an expected conclusion. Do not tell a Reviewer the prior debate, author, suspected findings, or desired verdict.

## Handle Findings

- Validate findings against the underlying sources, artifact, and intended outcome before acting.
- Let the main thread apply accepted repairs directly or delegate them according to scope, context, cost, and risk.
- When risk calls for independent review after consequential repairs, use a fresh Reviewer with only the updated artifact and neutral requirements.
- If a Reviewer crosses its `Stop when` condition without a usable return, request a partial verdict once, then interrupt it. Inspect the trace and existing evidence; do not automatically start another Reviewer.

## Inspect Local Usage

When the user asks for model or subagent consumption, run `python3 scripts/usage_by_model.py`. For the active task use `--task-id current --by-agent --by-session`; for broader history use `--days N` or `--all`, with `--json` when structured output helps. Report processed tokens plus uncached input, cached input, output, reasoning output, and estimated credits. Treat this as diagnostic evidence, not a mandate to tune every role to the lowest possible effort. Prefer changing a profile only when repeated task-scoped evidence shows the current setting is wasteful or insufficient.

## Guardrails

- Preserve unrelated user work and obey applicable project, domain, and tool instructions.
- Delegation does not expand authority. Do not commit, publish, deploy, send messages, change external state, or handle sensitive data beyond the user's request.
- For current or factual research, prefer primary sources, record relevant dates, cite evidence, and distinguish fact from inference.
- Keep private-data exploration narrow and return only the minimum evidence needed.
- Resolve conflicting claims against the strongest available evidence and return one coherent result to the user.
