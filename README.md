<p align="right">
  <strong>English</strong> · <a href="./README.zh-CN.md">简体中文</a>
</p>

<p align="center">
  <img src="./assets/readme/agent-map.webp" width="100%" alt="Team Mode routes evidence gathering, bounded execution, and independent review while the main thread leads and accepts the final result.">
</p>

`team-mode` is a Codex Skill for coordinating three working agents across substantial development, research, analysis, planning, document, data, and content tasks. The main thread keeps unresolved decisions and final acceptance; subagents are used only when context isolation, bounded execution, safe parallelism, verification, or independent judgment has clear net value.

It is a value-based routing guide, not a mandatory pipeline. A task being large or divisible is not, by itself, a reason to spawn more agents.

## The team

- **Explorer · Luna Medium · read-only** — bounded search, tracing, and evidence compression. Medium is intentional: when discovery becomes architecture-defining, high-consequence, or too broad for reliable bounded evidence gathering, return the evidence and uncertainty to the main thread instead of mechanically raising Explorer effort.
- **Executor · Luna Max · workspace-write** — implementation, fixes, and tests after scope, interfaces, data models, state flows, acceptance checks, and safety boundaries are fixed. Max is a deliberately conservative quality margin: reducing implementation omissions and rework matters more than tuning to the theoretical minimum reasoning level.
- **Reviewer · Terra High · read-only** — fresh-context independent review of stable artifacts. High gives more reasoning margin for counterexamples, regressions, requirement coverage, and weak assumptions without making Reviewer a second architect.

A separate **default · Luna Low · read-only** dispatch guard rejects spawns that omit `agent_type`; it does no actual task work.

These defaults do not follow a mechanical “raise every role one level” rule. Use an already-sufficient level for ordinary evidence work, keep more margin where a role mutates artifacts or performs consequential independent judgment, and return decisions beyond a role's boundary to the main thread.

## How routing works

- Team Mode may use no subagents at all. Delegate only when expected benefit clearly exceeds briefing, inspection, waiting, rework, token, and conflict cost.
- Substantial tasks get a brief decomposition pass, but “can be split” does not mean “should be delegated.” Even two independent slices are parallelized only when the gain is real.
- Every child receives a self-contained dispatch packet with `Outcome`, `Benefit`, `Sources`, `Scope`, `Checks`, `Stop when`, and `Return`. `Benefit` must describe a real advantage, not boilerplate.
- Unresolved architecture, product semantics, interfaces, data models, state flows, scope, safety, and final acceptance stay in the main thread.
- New children normally start without inherited parent history; new Reviewers always do. Name every factual source the child needs.
- Parallel writers require disjoint, stable ownership. Keep one writer for each file, shared artifact, interactive session, or mutable-system boundary; stop or complete the old writer and state a handoff before ownership changes.
- After a child error, timeout, or interruption, inspect existing artifacts and trace evidence before retrying. Recover usable work instead of automatically repeating it.
- The main thread inspects real sources, diffs, artifacts, and verification. A child's “completed” status is not final acceptance.

## Independent review

Use Reviewer according to **risk and verification difficulty**, not file count.

Fresh review is usually valuable when shared APIs, state, persistence, concurrency, authorization, security, migration, compatibility, or cross-cutting behavior changed; verification is weak; a plausible false success would be costly; the diff is conceptually dense; implementation or tests exposed meaningful uncertainty; or the user explicitly asks for independent review.

Use **one risk-focused Reviewer by default**. Add another only for a genuinely independent unresolved risk whose expected value exceeds the additional briefing and inspection cost. Crossing a fixed threshold such as “three changed files” does not automatically launch separate code-quality, performance, and reuse reviewers.

## Install

Install this fork's Skill:

```bash
npx skills add jinhongel/codex-team-mode
```

The three working Agent profiles and the `default` dispatch guard are separate from the Skill. Copy the four TOML templates in [`agents/`](./agents) to `~/.codex/agents/` for personal use or `<repository>/.codex/agents/` for one project.

See [Custom Agent Profiles](./skills/team-mode/references/custom-agents.md) for exact filenames, safe installation, runtime validation, permission caveats, and model customization. Open a new Codex task or restart Codex if newly installed profiles do not appear immediately.

## Use

The Skill can trigger automatically for substantial tasks, or you can invoke it directly:

```text
Use $team-mode for this task. Delegate only when the benefit clearly exceeds coordination cost, and keep unresolved decisions and final acceptance in the main thread.
```

You do not need to name every agent yourself. The main thread decides whether to delegate, selects roles, controls concurrency, and remains responsible for the combined result.

## Customize

You can change `model` and `model_reasoning_effort` in `agents/*.toml`, but do not mechanically minimize token use and do not mechanically raise every role just because a higher setting exists. Judge representative tasks by correctness, omissions, rework, verification burden, and usage. Keep Explorer and Reviewer read-only, mutation permissions with Executor, new reviews fresh, and final decisions in the main thread.

## Repository layout

```text
codex-team-mode/
├── agents/                  # Three working profiles plus one dispatch guard
├── assets/readme/           # README visuals
├── skills/team-mode/        # Installable Skill
│   ├── references/          # Setup, evaluation, and testing guidance
│   ├── scripts/usage_by_model.py
│   └── SKILL.md
├── tests/                   # Agent, routing, and usage regression tests
├── LICENSE
└── README.md
```

MIT License
