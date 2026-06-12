# 流程流转状态(★ 格式模板)

> **本文件是 pm-template 内的格式模板,定义 STATE.md 的 3 段结构(5 phase + 变更日志 + 决策日志)。**
> **target 项目不会直接用本文件**——`/new-project` 首启时读本模板,生成 target 自己的 `docs/STATE.md`,后续由 `update_state.py` 原地读写。
> **pm-template 仓库自身不维护 STATE.md**(无 target 项目,无需)。

锁定状态: [ ] 未开始 / [~] 进行中 / [x] 已锁 / [SKIP] / [UNLOCKED] / [x] LEGACY

## Phase 0 立项

- 状态: [ ]
- artifact: `docs/00_charter.md`
- 追溯证据:
- 签字:

## Phase 1 需求 ★

- 状态: [ ]
- artifact: `docs/01_requirements.md`
- 追溯证据:
- 签字:

## Phase 2 概要设计

- 状态: [ ]
- artifact: `docs/02_high_level_design.md`
- 追溯证据:
- 签字:

## Phase 3 详细设计

- 状态: [ ]
- artifact:
  - `docs/03a_business_process.md`
  - `docs/03b_api_design.md`
  - `docs/03c_data_schema.md`
- 追溯证据:
- 签字:

## Phase 4 实现+验证

- 状态: [ ]
- 追溯证据: `<test/e2e 报告路径>`
- 签字:

## 变更日志(★ /change 入口)

> 状态:[ ] 未开始 / [~] 进行中 / [x] 已锁 / [DEPRECATED] / [ABORTED]
> 本段独立于 5 phase 状态机,由 `/change <type> <name>` 入口维护。
> 详见 `.claude/skills/change.md` 与 `docs/process/TODO.md`。
> 编号 NNNN 由 /change 自动分配(单调递增,废弃号不重用)。

| # | type | 名称 | 状态 | 加于 | 签字 | 关联 |
|---|---|---|---|---|---|---|
| (暂无变更) | | | | | | |

## 决策日志(ADR)

> 状态:proposed / accepted / deprecated / superseded
> 详见 `docs/process/templates/decision.md`。

| # | 标题 | 状态 | 加于 | 签字 |
|---|---|---|---|---|
| (暂无决策) | | | | |