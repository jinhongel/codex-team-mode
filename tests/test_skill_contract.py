from __future__ import annotations

import unittest
from pathlib import Path


ROOT = Path(__file__).parents[1]


class TeamModeSkillContractTests(unittest.TestCase):
    def test_dispatch_contract_is_operational(self) -> None:
        skill = (ROOT / "skills" / "team-mode" / "SKILL.md").read_text(encoding="utf-8")
        for label in ("Outcome", "Sources", "Scope", "Checks", "Stop when", "Return"):
            with self.subTest(label=label):
                self.assertIn(f"`{label}`", skill)
        self.assertIn("required `Outcome`, `Sources`, `Scope`, `Checks`, or `Stop when`", skill)
        self.assertIn("`Benefit`", skill)
        for label in ("Unresolved risk", "Evidence", "Checks already passed", "Do not repeat"):
            with self.subTest(label=label):
                self.assertIn(f"`{label}`", skill)
        self.assertIn("usable partial verdict", skill)
        self.assertIn("children never spawn descendants", skill)
        self.assertIn("request a partial verdict once, then interrupt it", skill)
        self.assertIn("`Explorer`（Luna Medium）", skill)
        self.assertIn("`Executor`（Luna xHigh）", skill)
        self.assertIn("`Reviewer`（Terra High）", skill)
        self.assertIn("Main thread: keep novel architecture", skill)
        self.assertIn("state the handoff", skill)
        self.assertIn("not by file count alone", skill)
        self.assertIn("one risk-focused Reviewer by default", skill)
        self.assertIn("references/interactive-testing.md", skill)

    def test_delegation_requires_clear_net_benefit_without_ritual_announcement(self) -> None:
        skill = (ROOT / "skills" / "team-mode" / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("clear net benefit", skill)
        self.assertIn("Merely having two independent slices is not enough", skill)
        self.assertIn("Decomposition is analysis, not a requirement to delegate", skill)
        self.assertIn("Benefit` is a parent-side routing gate", skill)
        self.assertIn("Do not emit ritual mode announcements", skill)
        self.assertNotIn("👾 已开启小队模式", skill)

    def test_agent_type_dispatch_gate_is_explicit_and_guard_is_optional(self) -> None:
        skill = (ROOT / "skills" / "team-mode" / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("## Dispatch Gate", skill)
        self.assertIn("Every Team Mode `spawn_agent` call must explicitly pass `agent_type`", skill)
        self.assertIn("never use `default` as a working role", skill)
        self.assertIn("optional `default` profile", skill)
        self.assertIn("Team Mode does not require that guard", skill)

    def test_custom_agent_reference_avoids_global_side_effects_and_brittle_workarounds(self) -> None:
        reference = (ROOT / "skills" / "team-mode" / "references" / "custom-agents.md").read_text(
            encoding="utf-8"
        )
        self.assertIn("Team Mode requires these three profiles", reference)
        self.assertIn("`default.toml` is **optional**", reference)
        self.assertIn("can also intercept omitted/default subagent dispatches from other Codex workflows", reference)
        self.assertIn("Do **not** change a global `agents.max_depth` setting solely to install Team Mode", reference)
        self.assertIn("do not change undocumented feature flags from memory", reference)
        self.assertIn("%USERPROFILE%\\.codex\\agents\\", reference)
        self.assertIn("gpt-5.6-terra", reference)
        self.assertIn("gpt-5.6-luna", reference)
        self.assertIn("`Executor`: `gpt-5.6-luna`, `xhigh`", reference)
        self.assertNotIn("hide_spawn_agent_metadata", reference)
        self.assertNotIn("tool_namespace", reference)

    def test_interactive_testing_is_conditional_and_keeps_one_operator(self) -> None:
        reference = (
            ROOT / "skills" / "team-mode" / "references" / "interactive-testing.md"
        ).read_text(encoding="utf-8")
        self.assertIn("代码检查和自动化测试无法提供可信判断", reference)
        self.assertIn("同时只允许一个活动操作者", reference)
        self.assertIn("彼此隔离时，才并行执行", reference)
        self.assertIn("最终体验验收留在主线程", reference)

    def test_public_readmes_document_required_profiles_and_optional_guard(self) -> None:
        for filename in ("README.md", "README.zh-CN.md"):
            with self.subTest(filename=filename):
                readme = (ROOT / filename).read_text(encoding="utf-8")
                self.assertIn("./assets/readme/agent-map.webp", readme)
                self.assertIn("jinhongel/codex-team-mode", readme)
                self.assertIn("default.toml", readme)
        english = (ROOT / "README.md").read_text(encoding="utf-8")
        chinese = (ROOT / "README.zh-CN.md").read_text(encoding="utf-8")
        self.assertIn("Executor · Luna xHigh", english)
        self.assertIn("Executor（执行者）· Luna xHigh", chinese)
        self.assertIn("optional strict dispatch guard", english)
        self.assertIn("可选的严格派发哨兵", chinese)
        self.assertTrue((ROOT / "assets" / "readme" / "agent-map.webp").is_file())
        self.assertFalse((ROOT / "assets" / "readme" / "agent-map.svg").exists())

    def test_skill_metadata_matches_value_based_routing(self) -> None:
        metadata = (ROOT / "skills" / "team-mode" / "agents" / "openai.yaml").read_text(encoding="utf-8")
        self.assertIn("only when they add clear value", metadata)
        self.assertIn("benefit clearly exceeds coordination cost", metadata)


if __name__ == "__main__":
    unittest.main()
