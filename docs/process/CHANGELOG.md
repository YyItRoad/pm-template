# 流程模板迭代历史

> 记录本流程模板(`docs/process/`)的迭代变化,**不**记录使用本流程的具体项目。
> 用途: 模板作者根据实际使用反馈调整模板时,在这里记录"为什么改"。

## v0.4.0 — 2026-06-12

**类型**:minor(交付清单 MANIFEST.json + audit skill + 清理 spec/tests)+ 配套 7 处引用修复
**包含变更**:
- 加 [`MANIFEST.json`](../../MANIFEST.json) — 区分 ship / skip,对齐 npm `package.json files` 行业约定;目标项目"Use this template" 后用本清单决定保留 / 删什么
- 加 `.claude/skills/audit.md` + `.claude/scripts/audit.py` — `/audit` skill 包装 phase-4 critic 5 项机械检查(AC 覆盖 / 范围蔓延 / 反向需求 / 接口一致 / 单测),tests/ 缺失时 1 + 5 自动 N/A
- 删 `docs/superpowers/` — 4 个 pm-template 自己的设计 spec + plan(standard-process-template / standard-tech-stack / pm-template-skill-ization + tech-stack-implementation plan,共 2651 行)
- 删 `tests/` — 2 个 pm-template 自己的 pytest(test_skill_redesign_smoke + test_update_state,1365 行);目标项目用不到,改在 target 项目里自测
- 删 `docs/process/TESTING_BOUNDARY.md` — 整文件描述已删的 28 个测试用例,失去意义
- 7 处引用清理:README.md 4 入口表 / tech_stack.md frontmatter / .claude/skills/README.md / .claude/scripts/update_state.py / CHANGELOG v0.2/0.3 历史条目(加注)→ 全部从指向已删 spec 改为"git history"或"本文件"
- 修 README.md "13 skills" 数字不一致(全统一为 14)
- 修 MANIFEST.json `docs/process/audit/reports/` 矛盾(空占位不应在 skip)

**作者**:YyItRoad
**部署**:
- 时间:2026-06-12 16:40
- commit:b2ea092 + 85d4f4c
- 验证:✓ audit.py 加载 + tests/ 缺失时 N/A fallback 工作
**回滚方案**:`git revert b2ea092..85d4f4c`
**关联 ADR**:无
**关联 5 phase 段**:无

**v0.4.0 决定**:
- 引入 ship / skip 清单(MANIFEST.json),把"Use this template"流程标准化
- 清理 pm-template 自己的 meta(specs + tests + 边界文档),让仓库作为模板更"轻"
- audit skill 收口 phase-4 critic(不再让 LLM 自由发挥跑审查)
- "13 → 14 skill"(加 audit)

**设计原则变更**:
- **specs 不再随仓库 ship**:pm-template 演化用的设计 spec 改为 git history 唯一来源,目标项目不继承
- **target project self-test**:pm-template 不再"自带测试套件",目标项目引入后自写测试

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

**设计 spec** *(历史 spec,v0.4.0 起已从仓库清理,完整内容见 git history `b2ea092` 之前)*:
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

**设计 spec** *(历史 spec,v0.4.0 起已从仓库清理)*: `docs/superpowers/specs/standard-tech-stack-design.md`

## v0.1.0 — 初版落地

**背景**: 5 phase 流程跑通后,把流程模板抽离成独立仓库供未来新项目复用。

**v0.1.0 决定**:
- 5 phase(立项 / 需求 / 概设 / 详设 / 实现)流程
- 每 phase 三件套:模板 + DoD + critic
- 双层验证(AI critic + 人 review)
- 模板 + DoD + critic 资产 ~20 文件
