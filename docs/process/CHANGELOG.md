# 流程模板迭代历史

> 记录本流程模板(`docs/process/`)的迭代变化,**不**记录使用本流程的具体项目。
> 用途: 模板作者根据实际使用反馈调整模板时,在这里记录"为什么改"。

## v0.1.0 — 初版落地

**背景**: 5 phase 流程跑通后,把流程模板抽离成独立仓库供未来新项目复用。

**v0.1.0 决定**:
- 5 phase(立项 / 需求 / 概设 / 详设 / 实现)流程
- 每 phase 三件套:模板 + DoD + critic
- 双层验证(AI critic + 人 review)
- 模板 + DoD + critic 资产 ~20 文件

## v0.2.0 — 新增标准技术栈规范

**背景**: 流程跑通后,实际使用中反复出现"技术选型从零开始 / AI 自由发挥选错库"的问题。沉淀一套标准栈规范,Phase 0 签字 = 锁。

**v0.2.0 决定**:
- 新增 `docs/process/tech_stack.md` — 9 层(L1/L2/L3 锁级)+ 后端 4 层架构
- 9 处模板/DoD/critic 资产加 stack 检查/引用
- 引入"轻量级 vs 重量级偏航"分流(L3 子选 vs L1/L2 大改)
- 升级不影响已锁定项目

**设计 spec**: `docs/superpowers/specs/standard-tech-stack-design.md`