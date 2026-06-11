# 流程模板迭代历史

> 记录本流程模板(`docs/process/`)的迭代变化,**不**记录使用本流程的具体项目。
> 用途: 模板作者根据实际使用反馈调整模板时,在这里记录"为什么改"。

## v0.3.0 — 2026-06-11

**类型**:minor(新增 2 跨切面 skill + 5 项修/重构 + 2 轮审计)
**包含变更**:
- P0 修 3 个让 /change 与 phase 4 实际可跑的 bug(PHASE3_FILE_MAP / sys.path / critic 不支持 change/<type>)
- 5 phase + 5 change DoD 编号统一为全局 `D0-NN` / `CF-NN` 等
- 补 2 skill(`decision` / `release`)+ ADR 配套 critic / DoD
- P2 修 5 项:release 模板示例标 / 03b 列对齐 8 列 / _base 段号说明
- 修剪 + 拼凑:13 skill 描述无模板项目名泄漏(`pm-template` 移除)
- 文档/skill 职责分工原则:skill 瘦执行 + 1 行引用 spec,doc 装详情
- 二轮审计:critic / dod-check 示例改用新 DoD 编号,spec 9 处 "10 skill" 残留 → "13 skill"
- README 同步 13 skills + 3 维护期入口(/change /decision /release)
- Windows 兼容(`update_state.py` 条件 import fcntl,74/74 pytest 在 Windows 跑得动)

**作者**:YyItRoad
**部署**:
- 时间:2026-06-11 11:30
- commit:2e71ce7
- 验证:✓ 74/74 pytest 全过
**回滚方案**:`git revert 2e71ce7..8eed22a` + `git tag -d v0.3.0` + 旧版用 v0.2.0
**关联 ADR**:无(本仓库为模板仓库,STATE.md 保持空)
**关联 5 phase 段**:无

**v0.3.0 决定**:
- skill 数 10 → 13(加 `change` / `decision` / `release`)
- DoD 编号从 `<section>.<idx>` 混乱方案 → 全局唯一 `<phase>-<NN>` 方案
- 引入"skill/doc 职责分工"原则
- 引入"skill 描述无模板项目名"原则

**设计 spec**:
- `docs/superpowers/specs/pm-template-skill-ization-design.md` §2.2(13 skill 职责矩阵)
- `docs/superpowers/specs/pm-template-skill-ization-design.md` §4.6(decision 状态机)
- `docs/superpowers/specs/pm-template-skill-ization-design.md` §4.7(release 规范)

## v0.2.0 — 新增标准技术栈规范

**背景**: 流程跑通后,实际使用中反复出现"技术选型从零开始 / AI 自由发挥选错库"的问题。沉淀一套标准栈规范,Phase 0 签字 = 锁。

**v0.2.0 决定**:
- 新增 `docs/process/tech_stack.md` — 9 层(L1/L2/L3 锁级)+ 后端 4 层架构
- 9 处模板/DoD/critic 资产加 stack 检查/引用
- 引入"轻量级 vs 重量级偏航"分流(L3 子选 vs L1/L2 大改)
- 升级不影响已锁定项目

**设计 spec**: `docs/superpowers/specs/standard-tech-stack-design.md`

## v0.1.0 — 初版落地

**背景**: 5 phase 流程跑通后,把流程模板抽离成独立仓库供未来新项目复用。

**v0.1.0 决定**:
- 5 phase(立项 / 需求 / 概设 / 详设 / 实现)流程
- 每 phase 三件套:模板 + DoD + critic
- 双层验证(AI critic + 人 review)
- 模板 + DoD + critic 资产 ~20 文件
