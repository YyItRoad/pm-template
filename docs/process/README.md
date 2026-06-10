# 流程模板使用指南

> 本目录(`docs/process/`)是**可复用的项目流程资产**,不是某个具体项目的 phase 文档。
> 新项目用本模板时,把 `templates/0X_*.md` 复制到 `docs/0X_*.md`,按模板填空。

## 目录结构

```
docs/process/
├── README.md            ← 你正在看
├── STATE.md             ← 当前项目流转状态(由使用本模板的项目填)
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

完整设计说明见: `docs/superpowers/specs/standard-process-template-design.md`

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

看 `docs/process/STATE.md`(由使用本模板的项目维护)。状态符号:
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