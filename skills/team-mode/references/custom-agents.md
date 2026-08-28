# Custom Agent Profiles

Read this reference only when installing, repairing, verifying, or customizing Team Mode profiles. Normal task routing does not require it.

## Runtime Readiness

Treat the active Codex runtime as the source of truth. Profile files on disk do not prove that the current task can route to them.

Before declaring Team Mode ready:

1. Confirm that `spawn_agent` exposes `agent_type` and that `Explorer`, `Executor`, and `Reviewer` are selectable.
2. After a new task or restart, run a small bounded profile probe when runtime verification is needed.
3. Verify actual trace metadata such as agent role, model, effort, and effective sandbox rather than relying on the child Agent's self-report.

If `agent_type` is missing or a selected profile inherits the wrong model, do not silently use a generic child and do not change undocumented feature flags from memory. Update/restart Codex, open a fresh task, and check the current official Codex subagent documentation before changing runtime configuration. A workaround that was valid for an older Codex release may be wrong for the current one.

`task_name` labels a child thread; it does not select a profile. Team Mode always passes one of the three working profile names explicitly through `agent_type`.

## Required Working Profiles

The Skill and custom Agent profiles are separate configuration surfaces. Installing the Skill alone does not install the working profiles.

Team Mode requires these three profiles:

- `Explorer`: `gpt-5.6-luna`, `medium`, `read-only`.
- `Executor`: `gpt-5.6-luna`, `xhigh`, `workspace-write`.
- `Reviewer`: `gpt-5.6-terra`, `high`, `read-only`.

The defaults deliberately do not follow a mechanical “one level higher everywhere” rule. Explorer stays at Medium because most of its work is bounded search, tracing, and evidence compression. Executor uses Luna xHigh to keep substantial reasoning margin for mutable implementation while reserving Max for genuinely hardest quality-first workloads. Reviewer uses Terra High to give fresh independent review more room for counterexamples, regressions, requirement coverage, and weak assumptions.

These are role defaults, not claims that one effort level is universally optimal. Do not upgrade or downgrade merely because a higher or lower setting exists. Change a profile when repeated representative tasks show that the current setting is materially insufficient or unnecessarily wasteful.

Use the canonical templates in this fork's [`agents`](https://github.com/jinhongel/codex-team-mode/tree/main/agents) directory.

## Optional Strict Dispatch Guard

`default.toml` is **optional**. It is not a fourth working profile and Team Mode does not depend on it for normal routing.

When installed, the guard uses `gpt-5.6-luna` at `low` effort and refuses any subagent dispatch that omits `agent_type` or explicitly selects `default`.

The guard is useful when you want fail-closed routing, but it has a wider side effect: a personal `default.toml` can also intercept omitted/default subagent dispatches from other Codex workflows or Skills in the same scope. Do not install it globally merely because Team Mode is installed. Prefer a project-scoped guard when strict routing is useful only for one repository.

## Choose The Scope

Personal profiles apply across Codex tasks for that user. Project profiles apply only to the repository where they are installed.

Typical personal paths:

- Windows: `%USERPROFILE%\.codex\agents\`
- macOS/Linux: `~/.codex/agents/`

Project scope:

- `<repository>/.codex/agents/`

Required filenames:

- `Explorer.toml`
- `Executor.toml`
- `Reviewer.toml`

Optional strict guard:

- `default.toml`

Codex identifies a custom Agent by its `name` field. Keep the names unchanged unless the Skill routing names are changed at the same time.

## Keep Fan-Out Shallow Without Global Side Effects

Standard Team Mode keeps all routing in the main thread and its working profiles explicitly prohibit spawning descendants. That behavioral boundary is sufficient for normal use.

Do **not** change a global `agents.max_depth` setting solely to install Team Mode. A global depth limit can affect unrelated Codex workflows and other Skills. If you want a hard runtime nesting limit in addition to the profile instructions, configure it only after checking the current Codex documentation and understanding the scope of the setting; prefer project scope when available.

Choose any thread/concurrency limit according to runtime capacity and task value. Available slots are not a reason to fill them.

## Install Or Repair

1. Confirm authorization before writing personal or project Codex configuration.
2. Inspect the destination directory first and preserve unrelated profiles.
3. If a same-named profile already exists, compare it with the template before replacing user changes.
4. Copy the three required TOML templates to the selected Agent directory.
5. Install `default.toml` only when strict fail-closed routing is explicitly desired and its scope is understood.
6. Parse the TOML files with Python `tomllib` or another TOML parser and verify `name`, `description`, `developer_instructions`, model, effort, and sandbox mode.
7. Open a new Codex task or restart Codex if newly installed profiles are not visible.

## Disable Or Restore The Optional Guard

To disable only the guard, move `default.toml` outside the active `agents` directory rather than deleting it. The three working profiles remain installed.

Example disabled locations:

- Windows personal scope: `%USERPROFILE%\.codex\agents-disabled\default.toml`
- macOS/Linux personal scope: `~/.codex/agents-disabled/default.toml`
- Project scope: `<repository>/.codex/agents-disabled/default.toml`

Restart Codex or open a new task after moving the file. Restore strict dispatch by moving it back into the active `agents` directory.

## Verify Availability

Installed profiles and running subagents are different things. An Agent/thread activity list normally shows instances that have already been spawned, not every idle installed profile.

For the three required profiles:

1. Open a new task after installation or repair.
2. Confirm `spawn_agent` exposes the intended `agent_type` choices.
3. Spawn a small bounded `Explorer` probe with fresh context and no writes.
4. Verify from runtime trace data that:
   - the role is `Explorer`;
   - the model matches the profile;
   - the effort matches the profile;
   - the effective sandbox is appropriate.

The parent task's live permission mode may override a child profile's TOML sandbox setting. If read-only isolation matters, verify the effective runtime sandbox; the TOML field alone is not an operating-system security guarantee.

If the optional `default` guard is installed, you may perform a controlled onboarding self-test by deliberately omitting `agent_type` in a no-tool probe. It should refuse the task and return the guard message. Do not omit `agent_type` during normal Team Mode routing.

## Customize Models Safely

Model availability and preferences may differ between Codex environments. Preserve these boundaries when customizing:

- Keep `Explorer` and `Reviewer` read-only.
- Keep mutation permissions limited to `Executor`.
- Keep standard Team Mode fan-out in the main thread.
- Keep new independent reviews fresh and neutral.
- Keep unresolved user intent, product, editorial, architecture, interface, data-model, state-flow, safety, scope, and acceptance decisions in the main thread.
- Prefer enough reasoning margin to avoid costly rework, but do not mechanically raise every role by one level.
- Reserve Max for cases where representative evidence shows xHigh is not enough or the user explicitly wants a hardest-case quality-first run.
- If a configured model is unavailable, verify current model availability before substituting another one.
