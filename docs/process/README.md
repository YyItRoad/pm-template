# 流程模板使用指南

> 本目录(`docs/process/`)是**可复用的项目流程资产**,不是某个具体项目的 phase 文档。
> 新项目用本模板时,把 `templates/0X_*.md` 复制到 `docs/0X_*.md`,按模板填空。

## 目录结构

```
docs/process/
├── README.md            ← 你正在看
├── STATE.md             ← STATE.md **格式模板**(只读,定义 5 phase + 变更日志 + 决策日志 段结构);target 项目的 runtime 状态在 `docs/STATE.md`,由 `/new-project` 生成
├── CHANGELOG.md         ← 流程模板迭代历史
├── tech_stack.md        ← 标准技术栈规范
├── templates/           ← artifact 模板(给 AI 填空,不自由发挥)
│   ├── 00_charter.md
│   ├── 01_requirements.md
│   ├── 02_high_level_design.md
│   └── 03_detailed_design.md
├── dod/                 ← DoD checklist(每 phase 一份,全部勾上才能锁)
│   ├── 00_charter.md
│   ├── 01_requirements.md
│   ├── 02_high_level_design.md
│   ├── 03_detailed_design.md
│   └── 04_implementation.md
└── critics/             ← critic prompt(给 AI 跑自审,只报不修)
    ├── 00_charter.md
    ├── 01_requirements.md
    ├── 02_high_level_design.md
    ├── 03a_business_process.md
    ├── 03b_api_design.md
    ├── 03c_data_schema.md
    ├── 04_implementation.md
    └── reports/         ← critic 自审报告存档(强制)
```

## 5 Phase 流程

| Phase | 产物 | 模板 | DoD | Critic |
|---|---|---|---|---|
| 0 立项 | `docs/00_charter.md` | `templates/00_charter.md` | `dod/00_charter.md` | `critics/00_charter.md` |
| 1 需求 ★ | `docs/01_requirements.md` | `templates/01_requirements.md` | `dod/01_requirements.md` | `critics/01_requirements.md` |
| 2 概要设计 | `docs/02_high_level_design.md` | `templates/02_high_level_design.md` | `dod/02_high_level_design.md` | `critics/02_high_level_design.md` |
| 3 详细设计 | `docs/03a_business_process.md` 等 3 文件 | `templates/03_detailed_design.md` | `dod/03_detailed_design.md` | `critics/03a/b/c_*.md` |
| 4 实现+验证 | 代码 + tests | (无) | `dod/04_implementation.md` | `critics/04_implementation.md` |

## 技术栈规范

新项目**必须**引用 [`tech_stack.md`](tech_stack.md),在 `docs/00_charter.md` §2.5 签字 = 锁。

详见 [tech_stack.md](tech_stack.md) §1 锁层级说明。

## 怎么用(5 步)

1. **复制模板**: 把 `templates/0X_*.md` 复制到 `docs/0X_*.md`
2. **让 AI 填空**: 告诉 AI "请按 `docs/process/templates/0X_*.md` 填空,主题是 <项目>"
3. **跑 critic 自审**: 把 `critics/0X_*.md` 完整内容复制 + 加 "<artifact_path> 跑自审"
4. **报告存档**: critic 报告**必须**存到 `critics/reports/0X_<phase>_<YYYY-MM-DD>.md`
5. **签字锁**: 勾完 DoD 全部 + 在 artifact 末尾 §N+1 签字 + 更新 `STATE.md` 状态

## 流转状态

看 target 项目的 `docs/STATE.md`(由 `/new-project` 从 `docs/process/STATE.md` 模板生成,后续 `update_state.py` 原地读写)。状态符号:
- `[ ]` 未开始
- `[~]` 进行中
- `[x]` 已锁(走完流程,签字确认)
- `[SKIP]` 跳过(必须写理由)
- `[UNLOCKED]` 解锁中(已锁的 phase 改了,下游待重审)
- `[x] LEGACY` 历史包袱(试点项目专用)

## 双层验证

1. **AI critic 自审** — 跑 `critics/0X_*.md` 模板的 prompt,产出报告
2. **你本人 review** — 看报告,CRITICAL/HIGH 改完,再勾 DoD 末两条(critic + 签字)

只有两层都过,phase 才能锁。

---

## 设计原则(Why pm-template 是这样)

> 答 5 个最常被问的"为什么"。精简版,设计取舍的完整讨论在 git history。

### 1. 为什么 5 phase?不 3 不 7

- 立项(Why) → 需求(What) → 概设(How-逻辑) → 详设(How-物理) → 实现(Code)
- 每 phase 一个状态,粗→细。phase 之间有"签字门"挡漂移
- 3 phase 粗(质量难控),7 phase 细(状态机爆炸 — 5 phase × 5 状态 = 25 个状态已接近认知上限)

### 2. 为什么 L1/L2/L3 锁级?不扁平

- L1 🔒 锁死:每次新项目重选会浪费时间(语言 / 框架 / 库)
- L2 🟡 推荐:大概率沿用,偏离要文档化理由(数据库 / ORM)
- L3 ⬜ 自由:按需选(具体小库)
- 偏离成本 ↑ 时锁级 ↑。锁得越死,越要 Phase 0 签字 + unlock 流程保护

### 3. 为什么 4 层后端(API/Service/Model/Schema)?

- 防两个 AI 最常踩的坑:"胖 API 层"(业务写在 route)和"漏 service"(API 直接查 DB)
- 4 层 + 单一职责是**机械约束**,让 AI 不能自由发挥
- 详见 [`tech_stack.md`](tech_stack.md) §5

### 4. 为什么 13 skill?不"手写流程"

- 文档是死的,LLM 不照着读 → 流程等于没流程
- 13 skill 把"5 phase 流程 + 状态机 + DoD + critic"封装成 Claude Code 可识别的入口
- 1 入口(new-project)+ 5 phase + 4 辅助(state/critic/dod-check/unlock)+ 4 维护期(change/decision/release/audit)= 14(注:14 是 v0.4.0 后)
- 状态机 6 状态(`[ ]`/`[~]`/`[x]`/`[UNLOCKED]`/`[SKIP]`/`[x] LEGACY`)覆盖完整生命周期

### 5. 为什么 5 类门(状态机 / 签字 / DoD / critic / 硬 grep)?

- 单层检查(critic 主观打分)易被 LLM 绕开
- 5 类门 = 5 个**独立**机制,任一被绕还有 4 个兜底
- 硬 grep 尤其关键 — LLM 不能"凭记忆"骗过 `grep` 命令
- 例:Phase 2 启动时硬 grep `01_requirements.md` 的 4 个 anchor(挖掘证据),缺一就 `ERR_PHASE_1_INCOMPLETE`