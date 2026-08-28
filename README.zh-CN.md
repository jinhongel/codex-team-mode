<p align="right">
  <a href="./README.md">English</a> · <strong>简体中文</strong>
</p>

<p align="center">
  <img src="./assets/readme/agent-map.webp" width="100%" alt="小队模式把探索、边界执行和独立复审交给不同角色，主线程负责带队、决策与最终验收。">
</p>

`team-mode`（小队模式）是一个负责协调三个工作 Agent 的 Codex Skill，适用于有一定规模的开发、调研、分析、规划、文档、数据和内容任务。主线程保留尚未解决的决策并负责最终验收；子 Agent 只承担能够明确获得上下文隔离、执行、并行、验证或独立判断收益的工作。

它是按任务净收益调度的指南，不要求每次走固定流程，也不会因为任务“大”或“可以拆”就自动要求多开 Agent。

## 三个角色

- **Explorer（探索者）· Luna Medium · 只读**：负责有边界的搜索、追踪和证据压缩。Medium 是有意保留的默认值；如果调查演变成架构级、高后果或难以收口的判断，就把证据和不确定性交回主线程，而不是机械提高 Explorer 档位。
- **Executor（执行者）· Luna Max · 可写**：在范围、接口、数据模型、状态流程、验收标准和安全边界已经明确后完成实现、修复和测试。Max 是偏保守的质量余量，优先减少实现遗漏和返工，而不是把推理强度压到理论最低。
- **Reviewer（复审者）· Terra High · 只读**：使用全新上下文独立检查稳定产物。High 为反例、回归、需求覆盖和错误假设保留额外判断余量，但 Reviewer 不取代主线程做架构决策。

另有一个 **default · Luna Low · 只读** 的派发哨兵，只负责拒绝漏传 `agent_type` 的派发，不承担实际工作。

这套模型配置不是“所有角色统一上调一级”。原则是：普通证据型工作用已经足够的档位；会直接产生修改或承担重要独立判断的角色，可以保留更宽裕的推理余量；超出角色边界的关键判断回到主线程。

## 怎么调度

- Team Mode 可以一个子 Agent 都不启动。只有当预期收益明确高于 brief、检查、等待、返工、token 和冲突成本时才委派。
- 大任务先做拆分分析，但“能拆”不等于“应该派”。即使存在两个独立切片，也只有在并行或上下文收益确实明显时才并行。
- 每个子 Agent 收到包含 `Outcome`、`Benefit`、`Sources`、`Scope`、`Checks`、`Stop when` 和 `Return` 的自包含任务包。`Benefit` 必须是真实收益，不允许为了满足格式而编一个理由。
- 架构、产品语义、接口、数据模型、状态流程、范围、安全边界和最终验收仍由主线程负责。
- 新子 Agent 默认不继承父线程历史；尤其 Reviewer 必须使用 fresh context。任务包必须明确需要读取的文件、URL、数据或其他事实来源。
- 并行写入只允许责任区稳定且互不重叠的任务。同一文件、共享产物、交互会话或可变系统边界同一时间只保留一个写入者；换人时先停止/完成旧 writer，再明确 handoff。
- 子 Agent 报错、超时或中断后，先检查它已经留下的代码、产物和 trace；已有结果可恢复时不重复执行。
- 主线程必须检查真实来源、diff、产物和验证结果；子 Agent 自己说“完成”不等于任务通过验收。

## 独立复审

Reviewer 按**风险和验证难度**触发，而不是按“改了几个文件”机械触发。

通常在以下情况值得使用 fresh Reviewer：共享 API、状态、持久化、并发、权限、安全、迁移、兼容或跨模块行为发生变化；结果难以确定性验证；错误成功的代价较高；diff 概念密度较高；实现或测试已经暴露出真实不确定性；或者用户明确要求独立审查。

默认先使用 **一个针对具体风险的 Reviewer**。只有存在第二个真正独立的未解决风险，且额外审查的收益明确高于协调成本时，才增加 Reviewer。不会因为修改跨过“三个文件”等固定阈值就自动启动代码质量、性能、复用三个 Reviewer。

## 安装

安装这个 fork 的 Skill：

```bash
npx skills add jinhongel/codex-team-mode
```

三个工作 Agent 配置和 `default` 派发哨兵与 Skill 分开安装。个人使用时，把 [`agents/`](./agents) 里的四个 TOML 模板复制到 `~/.codex/agents/`；只给单个项目使用时，复制到 `<repository>/.codex/agents/`。

准确文件名、安全安装、运行时验证、权限限制和模型调整说明见[自定义 Agent 配置说明](./skills/team-mode/references/custom-agents.md)。安装后没有立即显示新 Agent 时，新建 Codex 任务或重启 Codex。

## 使用

任务达到一定规模时 Skill 可以自动触发，也可以明确调用：

```text
使用 $team-mode 完成这个任务。只有在收益明确高于协调成本时才委派；尚未解决的决策和最终验收留在主线程。
```

用户不用逐个指定 Agent。主线程负责判断是否委派、选择角色、控制并发和最终验收。

## 自定义

可以修改 `agents/*.toml` 中的 `model` 和 `model_reasoning_effort`，但不要机械追求最低 token，也不要因为存在更高档就统一升级。优先根据真实任务中的正确性、遗漏、返工、验证成本和使用量判断。Explorer 和 Reviewer 保持只读；修改权限只交给 Executor；新的复审保持 fresh context；最终决策留在主线程。

## 仓库结构

```text
codex-team-mode/
├── agents/                  # 三个工作 Profile 与一个派发哨兵
├── assets/readme/           # README 视觉素材
├── skills/team-mode/        # 可安装 Skill
│   ├── references/          # 配置、评估与测试说明
│   ├── scripts/usage_by_model.py
│   └── SKILL.md
├── tests/                   # Agent、路由与用量回归测试
├── LICENSE
└── README.md
```

MIT License
