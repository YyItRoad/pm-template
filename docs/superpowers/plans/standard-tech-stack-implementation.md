# 标准技术栈规范实施 Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 把 KidBudget 的 5-phase 流程模板资产(20 文件)+ 设计 spec 完整迁移到 pm-template 仓库,加 `tech_stack.md` 与 9 处模板/DoD/critic 改动,pm-template 仓库**零** KidBudget 残留,GitHub "Use this template" 可用。

**Architecture:** **MOVE 而非 COPY** — 用 `cp` + 双仓库 `git rm`/`git add` 模式实现跨仓库"移动"。KidBudget 仓库最终**无** `docs/process/` 目录;pm-template 仓库**无** KidBudget 任何内容。KidBudget 阶段文档中残留的 `docs/process/` 引用全部改指 pm-template GitHub URL。

**Tech Stack:** Markdown(纯文档项目)、Conventional Commits、GitHub Template Repository。

**Spec 来源:** `docs/superpowers/specs/standard-tech-stack-design.md`(已批准,本仓库)

---

## 命名/格式约定(全局)

- **不**在 spec/plan 名称里带日期(`feedback_spec_no_dates.md` 铁律)
- **不**在正文写"YYYY-MM-DD 已批准"等具体日期
- 模板的 `YYYY-MM-DD` **占位符**保留(用户填写时替换)
- Conventional Commits:`docs:` / `chore:` / `feat:`
- 中文为主,关键术语中英对照
- **pm-template 中任何文件零 KidBudget 内容**(项目名、commit hash、日期、具体路径都禁出现)

---

## File Structure(终态)

### pm-template 终态(11 commit 后)

```
pm-template/
├── LICENSE                           ← 新建(MIT,pm-template 自己)
├── README.md                         ← 新建(描述 pm-template 自己)
├── .gitignore                        ← 新建(pm-template 自己需要的忽略)
└── docs/
    ├── process/                      ← 从 KidBudget MOVE 过来(20 文件)
    │   ├── README.md                 ← MOVE + 完全改写(去 KidBudget 特定化)
    │   ├── STATE.md                  ← MOVE + 完全改写(空模板)
    │   ├── CHANGELOG.md              ← MOVE + 完全改写(无 KidBudget 试点引用)
    │   ├── tech_stack.md             ← 新建(标准栈规范,~400-500 行)
    │   ├── templates/                ← MOVE(5 文件,3 文件后续改)
    │   │   ├── 00_charter.md         ← 改:加 §2.5
    │   │   ├── 01_requirements.md
    │   │   ├── 02_high_level_design.md   ← 改:加 stack 引用
    │   │   ├── 03_detailed_design.md     ← 改:§A/§B/§C 加引用
    │   │   └── (无 04)
    │   ├── dod/                      ← MOVE(5 文件,3 文件后续改)
    │   │   ├── 00_charter.md         ← 改:加锁 DoD
    │   │   ├── 01_requirements.md
    │   │   ├── 02_high_level_design.md   ← 改:加 L1 偏航 DoD
    │   │   ├── 03_detailed_design.md     ← 改:加 §3.6 §3.7 DoD
    │   │   └── 04_implementation.md
    │   └── critics/                  ← MOVE(7 文件 + .gitkeep,3 文件后续改)
    │       ├── 00_charter.md
    │       ├── 01_requirements.md
    │       ├── 02_high_level_design.md   ← 改:加 stack 检查
    │       ├── 03a_business_process.md
    │       ├── 03b_api_design.md
    │       ├── 03c_data_schema.md        ← 改:加数据层检查
    │       ├── 04_implementation.md     ← 改:加一致性检查
    │       └── reports/.gitkeep
    └── superpowers/
        ├── specs/
        │   ├── standard-tech-stack-design.md  ← 已有(本 plan 不动)
        │   └── standard-process-template-design.md  ← 从 KidBudget MOVE
        └── plans/
            └── standard-tech-stack-implementation.md  ← 本文件
```

### KidBudget 终态(MOVE 完成后)

```
KidBudget/
├── docs/
│   ├── 00_charter.md ~ 03c_data_schema.md   ← 7 个 phase 文档,内部 docs/process/ 引用全部改 pm-template URL
│   ├── superpowers/
│   │   ├── specs/  ← standard-process-template-design.md 已被 move,无 KidBudget 设计 spec 残留
│   │   ├── plans/  ← (不动)
│   │   └── ...
│   ├── 功能说明.md  ← 内部引用检查
│   └── ...
├── (无 docs/process/)  ← 整个目录被 move 走
├── README.md  ← 内部 docs/process/ 引用改 pm-template URL
└── ...
```

---

## 任务

### Task 1: pm-template 仓库根基础文件

**Files:**
- Create: `/Users/yangyang/Desktop/Github/pm-template/LICENSE`
- Create: `/Users/yangyang/Desktop/Github/pm-template/README.md`
- Create: `/Users/yangyang/Desktop/Github/pm-template/.gitignore`

- [ ] **Step 1.1: 写 LICENSE(MIT,pm-template 自己)**

```bash
cat > /Users/yangyang/Desktop/Github/pm-template/LICENSE <<'EOF'
MIT License

Copyright (c) YyItRoad

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
EOF
```

- [ ] **Step 1.2: 写根 README.md(描述 pm-template 自己,不是项目通用模板)**

模板内容:

```markdown
# pm-template

> **Standard 5-phase project management process template + tech stack spec**
> 标准 5 阶段项目管理流程模板 + 技术栈规范

## 这是什么 / What is this

pm-template 是一个**可复用资产仓库**,为 **web 应用(后端业务层 + 后台管理 SPA + 关系数据库)** 型项目提供:

- **5 phase 流程** — 立项 / 需求 / 概要设计 / 详细设计 / 实现,每 phase 三件套(模板 + DoD + critic)
- **标准技术栈** — L1/L2/L3 锁级,Phase 0 签字 = 锁
- **双层验证** — AI critic 自审 + 用户签字

**不是**给单个项目用的脚手架。**是**给所有同类型项目共享的"流程 + 选型"标准。

## 3 个入口

| 用途 | 路径 |
|---|---|
| 流程使用指南 | [`docs/process/README.md`](docs/process/README.md) |
| 标准技术栈规范 | [`docs/process/tech_stack.md`](docs/process/tech_stack.md) |
| 设计 spec | [`docs/superpowers/specs/standard-process-template-design.md`](docs/superpowers/specs/standard-process-template-design.md) / [`standard-tech-stack-design.md`](docs/superpowers/specs/standard-tech-stack-design.md) |

## 怎么用

1. **新项目**: GitHub 顶部 → **"Use this template"** → 选 owner/repo → 创建
2. **初始化**: 把 `docs/process/templates/0X_*.md` 复制到新项目的 `docs/0X_*.md`,按模板填空
3. **Phase 0 签字**: 填 `docs/00_charter.md` §2.5,引用 [`docs/process/tech_stack.md`](docs/process/tech_stack.md) 选标准栈
4. **走完 5 phase**: 每 phase 完成 → 跑 critic → 勾 DoD → 签字 → 锁

## 适用

| ✅ 适用 | ❌ 不适用 |
|---|---|
| Web 应用(后端 + 管理端 SPA + 关系数据库) | CLI / 库 / SDK |
| 单体服务 / 中小规模 | 嵌入式 / 移动端原生 |
| 国内私有化部署 | 全球化 / 多区域部署 |

## 流程示意

```
Phase 0 立项        [x] ──┐
                          │
Phase 1 需求 ★      [x] ──┤
                          │
Phase 2 概要设计    [x] ──┤   每 phase: 模板填空 → critic 自审
                          │              → 勾 DoD → 签字 → 锁
Phase 3 详细设计    [x] ──┤
                          │
Phase 4 实现+验证   [x] ──┘
```

## 许可证

MIT — 详见 [LICENSE](LICENSE)
```

- [ ] **Step 1.3: 写 .gitignore(pm-template 自己需要的)**

pm-template 是纯文档仓库,但**也**是 GitHub Template Repository 起点,新项目 clone 后 gitignore 是干净起点,所以给一份常见语言的占位:

```bash
cat > /Users/yangyang/Desktop/Github/pm-template/.gitignore <<'EOF'
# 模板仓库的 .gitignore 占位
# 实际项目("Use this template" 后)按需扩展

# Python
__pycache__/
*.py[cod]
*.egg-info/
.venv/
venv/
.env

# Node
node_modules/
dist/
dist-app/
.vite/

# IDE
.vscode/
.idea/
*.swp

# OS
.DS_Store
Thumbs.db

# Logs
*.log
EOF
```

- [ ] **Step 1.4: 验证 + commit**

```bash
cd /Users/yangyang/Desktop/Github/pm-template
ls -la LICENSE README.md .gitignore
git add LICENSE README.md .gitignore
git -c user.name="YyItRoad" -c user.email="yyitroad@users.noreply.github.com" \
    commit -m "chore: scaffold repo (LICENSE + README + .gitignore)"
```

**预期**: 3 文件 created,1 commit。

---

### Task 2: MOVE 16 个模板/DoD/critic 文件(KidBudget → pm-template)

**Files:**
- Create in pm-template: `docs/process/templates/{00_charter,01_requirements,02_high_level_design,03_detailed_design}.md`(4 文件)
- Create in pm-template: `docs/process/dod/{00_charter,01_requirements,02_high_level_design,03_detailed_design,04_implementation}.md`(5 文件)
- Create in pm-template: `docs/process/critics/{00_charter,01_requirements,02_high_level_design,03a_business_process,03b_api_design,03c_data_schema,04_implementation}.md` + `reports/.gitkeep`(7 + 1 文件)
- Delete in KidBudget: 整个 `docs/process/{templates,dod,critics}/` 目录(后续 Task 10 一起做)

- [ ] **Step 2.1: 从 KidBudget 复制 16 文件到 pm-template**

```bash
cd /Users/yangyang/Desktop/Github/pm-template
mkdir -p docs/process/templates docs/process/dod docs/process/critics/reports

# templates/ (4 文件,无 04)
for f in 00_charter 01_requirements 02_high_level_design 03_detailed_design; do
  cp /Users/yangyang/Desktop/Github/KidBudget/docs/process/templates/${f}.md \
     docs/process/templates/${f}.md
done

# dod/ (5 文件)
for f in 00_charter 01_requirements 02_high_level_design 03_detailed_design 04_implementation; do
  cp /Users/yangyang/Desktop/Github/KidBudget/docs/process/dod/${f}.md \
     docs/process/dod/${f}.md
done

# critics/ (7 文件 + .gitkeep)
for f in 00_charter 01_requirements 02_high_level_design 03a_business_process 03b_api_design 03c_data_schema 04_implementation; do
  cp /Users/yangyang/Desktop/Github/KidBudget/docs/process/critics/${f}.md \
     docs/process/critics/${f}.md
done
cp /Users/yangyang/Desktop/Github/KidBudget/docs/process/critics/reports/.gitkeep \
   docs/process/critics/reports/.gitkeep
```

- [ ] **Step 2.2: 验证内容完整性(零内容改动)**

```bash
cd /Users/yangyang/Desktop/Github/pm-template
# 这些文件在 KidBudget 是纯模板,pm-template 拿过来应逐字节一致
diff -r /Users/yangyang/Desktop/Github/KidBudget/docs/process/templates/ \
        docs/process/templates/
diff -r /Users/yangyang/Desktop/Github/KidBudget/docs/process/dod/ \
        docs/process/dod/
diff -r /Users/yangyang/Desktop/Github/KidBudget/docs/process/critics/ \
        docs/process/critics/
# 预期:无任何 diff 输出
```

- [ ] **Step 2.3: 验证零 KidBudget 内容**

```bash
cd /Users/yangyang/Desktop/Github/pm-template
grep -r "KidBudget" docs/process/templates/ docs/process/dod/ docs/process/critics/ 2>&1
# 预期:无输出
```

- [ ] **Step 2.4: commit 到 pm-template**

```bash
cd /Users/yangyang/Desktop/Github/pm-template
git add docs/process/templates/ docs/process/dod/ docs/process/critics/
git -c user.name="YyItRoad" -c user.email="yyitroad@users.noreply.github.com" \
    commit -m "docs(process): move 16 template/dod/critic files from KidBudget"
```

**预期**: 16 文件 created,1 commit。`diff` 无输出,`grep KidBudget` 无输出。

---

### Task 3: 在 pm-template 新建 3 个 meta 文件(README/STATE/CHANGELOG,无 KidBudget 内容)

**Files:**
- Create in pm-template: `docs/process/README.md`(完全重写,描述 pm-template 自己的 docs/process/)
- Create in pm-template: `docs/process/STATE.md`(空模板,全部 [ ])
- Create in pm-template: `docs/process/CHANGELOG.md`(纯 v0.1.0 + v0.2.0,无 KidBudget 引用)

> **不**从 KidBudget 复制这 3 个文件,因为它们含 KidBudget 特定内容(LEGACY phase 状态 / KidBudget 试点描述)。在 pm-template 全新写。

- [ ] **Step 3.1: 写 docs/process/README.md(pm-template 自己的)**

内容(直接覆盖,pm-template 视角):

```markdown
# 流程模板使用指南

> 本目录(`docs/process/`)是**可复用的项目流程资产**,不是某个具体项目的 phase 文档。
> 新项目用本模板时,把 `templates/0X_*.md` 复制到 `docs/0X_*.md`,按模板填空。

## 目录结构

\`\`\`
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
\`\`\`

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
```

- [ ] **Step 3.2: 写 docs/process/STATE.md(空模板)**

```bash
cat > /Users/yangyang/Desktop/Github/pm-template/docs/process/STATE.md <<'EOF'
# 流程流转状态

> 锁定状态: [ ] 未开始 / [~] 进行中 / [x] 已锁 / [SKIP] / [UNLOCKED] / [x] LEGACY
> 本文件由使用本模板的项目维护,pm-template 仓库自身不使用。

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
EOF
```

- [ ] **Step 3.3: 写 docs/process/CHANGELOG.md(无 KidBudget 引用)**

```markdown
# 流程模板迭代历史

> 记录本流程模板(`docs/process/`)的迭代变化,**不**记录使用本流程的具体项目。
> 用途: 模板作者根据实际使用反馈调整模板时,在这里记录"为什么改"。

## v0.1.0 — 初版落地

**背景**: 试点项目验证 5 phase 流程能跑通后,把流程模板抽离成独立仓库供未来新项目复用。

**v0.1.0 决定**:
- 5 phase(立项 / 需求 / 概设 / 详设 / 实现)流程
- 每 phase 三件套:模板 + DoD + critic
- 双层验证(AI critic + 人 review)
- 模板 + DoD + critic 资产 ~20 文件

## v0.2.0 — 新增标准技术栈规范

**背景**: 流程跑通后,试点项目反复出现"技术选型从零开始 / AI 自由发挥选错库"的问题。沉淀一套标准栈规范,Phase 0 签字 = 锁。

**v0.2.0 决定**:
- 新增 `docs/process/tech_stack.md` — 9 层(L1/L2/L3 锁级)+ 后端 4 层架构
- 9 处模板/DoD/critic 资产加 stack 检查/引用
- 引入"轻量级 vs 重量级偏航"分流(L3 子选 vs L1/L2 大改)
- 升级不影响已锁定项目

**设计 spec**: `docs/superpowers/specs/standard-tech-stack-design.md`
```

- [ ] **Step 3.4: 验证零 KidBudget 内容 + commit**

```bash
cd /Users/yangyang/Desktop/Github/pm-template
grep -E "KidBudget|yyitroad" docs/process/README.md docs/process/STATE.md docs/process/CHANGELOG.md
# 预期:无输出
git add docs/process/README.md docs/process/STATE.md docs/process/CHANGELOG.md
git -c user.name="YyItRoad" -c user.email="yyitroad@users.noreply.github.com" \
    commit -m "docs(process): add pm-template-specific README/STATE/CHANGELOG"
```

**预期**: 3 文件 created,1 commit。`grep KidBudget/yyitroad` 无输出。

---

### Task 4: MOVE 设计 spec(KidBudget → pm-template)

**Files:**
- Move in KidBudget: `docs/superpowers/specs/standard-process-template-design.md` → 删除
- Create in pm-template: `docs/superpowers/specs/standard-process-template-design.md`

- [ ] **Step 4.1: 复制 + 验证**

```bash
cp /Users/yangyang/Desktop/Github/KidBudget/docs/superpowers/specs/standard-process-template-design.md \
   /Users/yangyang/Desktop/Github/pm-template/docs/superpowers/specs/standard-process-template-design.md

# 注: KidBudget 里的 spec 文件名也是 2026-06-09 前缀的旧名
# 先看一下源文件实际名字
ls /Users/yangyang/Desktop/Github/KidBudget/docs/superpowers/specs/
```

**如果源文件是 2026-06-09 前缀的旧名**(基于之前对话):先重命名为无日期版(应用 user feedback "无日期" 铁律):

```bash
# 在 KidBudget 仓库内重命名
cd /Users/yangyang/Desktop/Github/KidBudget
git mv docs/superpowers/specs/2026-06-09-standard-process-template-design.md \
       docs/superpowers/specs/standard-process-template-design.md

# 再复制到 pm-template(用新名)
cp docs/superpowers/specs/standard-process-template-design.md \
   /Users/yangyang/Desktop/Github/pm-template/docs/superpowers/specs/standard-process-template-design.md
```

- [ ] **Step 4.2: 验证零 KidBudget 内容 + commit**

```bash
cd /Users/yangyang/Desktop/Github/pm-template
grep -E "KidBudget|yyitroad|2026-06-09" \
   docs/superpowers/specs/standard-process-template-design.md
# 预期:无输出(或仅允许的占位符)
wc -l docs/superpowers/specs/standard-process-template-design.md
# 预期:~600 行(原 spec 大小)
git add docs/superpowers/specs/standard-process-template-design.md
git -c user.name="YyItRoad" -c user.email="yyitroad@users.noreply.github.com" \
    commit -m "docs(specs): move process template design spec from KidBudget"
```

- [ ] **Step 4.3: 在 KidBudget 提交删除**

```bash
cd /Users/yangyang/Desktop/Github/KidBudget
git status
# 预期:1 文件 renamed(从旧名到无日期名)或 1 文件 deleted
git add -A  # 把所有变更 stage
git -c user.name="YyItRoad" -c user.email="yyitroad@users.noreply.github.com" \
    commit -m "docs(specs): move process template design spec to pm-template"
```

**预期**: pm-template 1 commit + KidBudget 1 commit。

---

### Task 5: 创建 tech_stack.md

**Files:**
- Create: `/Users/yangyang/Desktop/Github/pm-template/docs/process/tech_stack.md`

- [ ] **Step 5.1: 写 tech_stack.md(按 spec §3 完整 9 节)**

按 spec `docs/superpowers/specs/standard-tech-stack-design.md` §3(完整 9 节)逐节落地。结构:

- 顶部:`**版本: v1.0**(初版)` + 简介
- §1 锁层级总览(2.1 锁级 / 2.2 存放位置)
- §3.1 后端栈
- §3.2 前端栈(Vue 3 管理端 SPA)
- §3.3 数据层
- §3.4 部署 / DevOps
- §3.5 测试策略
- §3.6 命名 / 接口 / 错误码约定
- §3.7 反向约束(Don'ts)
- §3.8 开发 / 运行环境
- §3.9 后端分层架构 + 职责/约束(4 层 + 异常体系 + Don'ts)
- §5 偏航 / Unlock 流程(精简版)
- §6.2 版本管理(精简版)

**必带**:🔒🟡⬜ 三级锁级 emoji(贯穿全文)
**禁止**:
- 任何 KidBudget 字样
- 具体日期(2026-06-09 等)
- spec 自身的 commit 引用、迭代历史

- [ ] **Step 5.2: 验证 + commit**

```bash
cd /Users/yangyang/Desktop/Github/pm-template
grep -E "KidBudget|2026-06-09|yyitroad" docs/process/tech_stack.md
# 预期:无输出
wc -l docs/process/tech_stack.md
# 预期:~400-500 行
grep -c "🔒" docs/process/tech_stack.md
# 预期:≥ 20(L1 锁级项数)
git add docs/process/tech_stack.md
git -c user.name="YyItRoad" -c user.email="yyitroad@users.noreply.github.com" \
    commit -m "docs(process): add standard tech stack spec (v1.0)"
```

**预期**: 1 文件 created,1 commit。`grep` 无残留,🔒 emoji ≥ 20。

---

### Task 6: 修改 3 个 templates(加 stack 引用)

**Files:**
- Modify: `docs/process/templates/00_charter.md`(加 §2.5)
- Modify: `docs/process/templates/02_high_level_design.md`(加 1 句)
- Modify: `docs/process/templates/03_detailed_design.md`(§A/§B/§C 各加 1 句)

- [ ] **Step 6.1: 修改 00_charter.md — 在 §2 目标与非目标 之后插 §2.5**

读取 `docs/process/templates/00_charter.md`,找到 "## 2. 目标与非目标" 段结束位置(在 "## 3. 角色清单" 之前),插入:

```markdown
## 2.5 技术栈确认

> 标准栈见 [`docs/process/tech_stack.md`](tech_stack.md)。
> 本节一旦签字,Phase 2/3/4 不再能改;偏航必须显式 unlock Phase 0 + 走 critic。

- **本项目栈选择**:
  - [ ] 按标准栈执行(L1 + L2 全锁,L3 自选)
  - [ ] 偏离标准栈,具体偏离项:
    - 偏离项 1: ___ (理由: ___)
    - 偏离项 2: ___ (理由: ___)

- [ ] 你本人签字: _______ — 锁生效
```

(签字栏不留 YYYY-MM-DD 占位符 — 改为"签字日期"在签字人名字后,具体值由用户填)

- [ ] **Step 6.2: 修改 02_high_level_design.md — 加 stack 引用**

读取 `docs/process/templates/02_high_level_design.md`,在文件顶部(标题后第一段)插入:

```markdown
> 技术选型遵循 [`docs/process/tech_stack.md`](tech_stack.md) §3.1-§3.8 锁级;偏离项须在 `docs/00_charter.md` §2.5 签字。
```

- [ ] **Step 6.3: 修改 03_detailed_design.md — §A/§B/§C 各加 1 句**

读取 `docs/process/templates/03_detailed_design.md`,找到 §A 业务流程 / §B 接口设计 / §C 数据表 DDL 三节,各在节标题下第一行加:

```markdown
> 命名 / 锁层级遵循 [`docs/process/tech_stack.md` §3.6 §3.7](tech_stack.md)。
```

- [ ] **Step 6.4: 验证 + commit**

```bash
cd /Users/yangyang/Desktop/Github/pm-template
grep "## 2.5 技术栈确认" docs/process/templates/00_charter.md
grep -c "tech_stack.md" docs/process/templates/02_high_level_design.md
grep -c "tech_stack.md" docs/process/templates/03_detailed_design.md
# 预期:1 命中 / 1 命中 / 3 命中(§A/§B/§C)
grep -E "KidBudget|2026-06-09|yyitroad" docs/process/templates/00_charter.md docs/process/templates/02_high_level_design.md docs/process/templates/03_detailed_design.md
# 预期:无输出
git add docs/process/templates/
git -c user.name="YyItRoad" -c user.email="yyitroad@users.noreply.github.com" \
    commit -m "feat(process): add tech stack confirmation to 3 phase templates"
```

**预期**: 3 文件修改,1 commit。grep 计数对得上,无 KidBudget 残留。

---

### Task 7: 修改 3 个 DoD(加 stack 检查项)

**Files:**
- Modify: `docs/process/dod/00_charter.md`
- Modify: `docs/process/dod/02_high_level_design.md`
- Modify: `docs/process/dod/03_detailed_design.md`

- [ ] **Step 7.1: 修改 dod/00_charter.md — 加 Phase 0 锁 DoD**

读取 `docs/process/dod/00_charter.md`,在末尾追加:

```markdown
- [ ] §2.5 技术栈确认签字完整(按标准栈 / 偏离项 + 理由,均需签字)
```

- [ ] **Step 7.2: 修改 dod/02_high_level_design.md — 加 L1 偏航 DoD**

读取 `docs/process/dod/02_high_level_design.md`,在末尾追加:

```markdown
- [ ] 技术选型未引入 `docs/process/tech_stack.md` §3.1-§3.8 L1 锁层之外的栈(若有偏离,Phase 0 §2.5 已签字)
```

- [ ] **Step 7.3: 修改 dod/03_detailed_design.md — 加 §3.6 §3.7 DoD**

读取 `docs/process/dod/03_detailed_design.md`,在末尾追加:

```markdown
- [ ] §A 流程 / §B 接口 / §C DDL 命名、字段类型、接口风格与 `docs/process/tech_stack.md` §3.6 §3.7 对齐
```

- [ ] **Step 7.4: 验证 + commit**

```bash
cd /Users/yangyang/Desktop/Github/pm-template
grep -l "§2.5 技术栈确认" docs/process/dod/00_charter.md
grep -l "L1 锁层" docs/process/dod/02_high_level_design.md
grep -l "§3.6 §3.7" docs/process/dod/03_detailed_design.md
# 三个 grep 都命中
grep -E "KidBudget|2026-06-09|yyitroad" docs/process/dod/00_charter.md docs/process/dod/02_high_level_design.md docs/process/dod/03_detailed_design.md
# 预期:无输出
git add docs/process/dod/
git -c user.name="YyItRoad" -c user.email="yyitroad@users.noreply.github.com" \
    commit -m "feat(process): add tech stack DoD items to 3 phases"
```

---

### Task 8: 修改 3 个 critic(加 stack 检查项)

**Files:**
- Modify: `docs/process/critics/02_high_level_design.md`
- Modify: `docs/process/critics/03c_data_schema.md`
- Modify: `docs/process/critics/04_implementation.md`

- [ ] **Step 8.1-8.3: 追加检查项(每个文件末尾)**

`docs/process/critics/02_high_level_design.md` 追加:
```markdown
- 是否引入 `docs/process/tech_stack.md` §3.1-§3.8 L1 锁层之外的技术栈(若偏离,Phase 0 §2.5 已签字)
```

`docs/process/critics/03c_data_schema.md` 追加:
```markdown
- 表命名 / 字段类型 / 字符集 / 索引命名是否对齐 `docs/process/tech_stack.md` §3.3 数据层规范
```

`docs/process/critics/04_implementation.md` 追加:
```markdown
- 实际代码使用的库 / 工具与 Phase 0 §2.5 选型一致;无未在 Phase 0 / Phase 2 锁过的新依赖
```

- [ ] **Step 8.4: 验证 + commit**

```bash
cd /Users/yangyang/Desktop/Github/pm-template
grep -l "L1 锁层" docs/process/critics/02_high_level_design.md
grep -l "§3.3 数据层" docs/process/critics/03c_data_schema.md
grep -l "Phase 0 §2.5" docs/process/critics/04_implementation.md
grep -E "KidBudget|2026-06-09|yyitroad" docs/process/critics/02_high_level_design.md docs/process/critics/03c_data_schema.md docs/process/critics/04_implementation.md
# 三个 grep 命中,第四个无输出
git add docs/process/critics/
git -c user.name="YyItRoad" -c user.email="yyitroad@users.noreply.github.com" \
    commit -m "feat(process): add tech stack critic checks to 3 phases"
```

---

### Task 9: KidBudget 侧引用清理(7 文件)

**Files in KidBudget:**
- Modify: `README.md`
- Modify: `docs/00_charter.md`
- Modify: `docs/01_requirements.md`
- Modify: `docs/02_high_level_design.md`
- Modify: `docs/03a_business_process.md`
- Modify: `docs/03b_api_design.md`
- Modify: `docs/03c_data_schema.md`

**目标**: 把所有 `docs/process/...` 内部引用改为 `https://github.com/YyItRoad/pm-template/tree/main/docs/process/<...>` 形式(让 KidBudget 还能引用模板,但从外部 URL 拉取)。

- [ ] **Step 9.1: 替换 README.md 中"流程状态"段(1 处)**

原文(`README.md:196`):
```markdown
> **流程状态**: 本项目作为 [docs/process/](docs/process/README.md) 5 phase 流程的**试点**,所有 phase 标 [x] LEGACY(实施在 2026-06-09 前完成,未走 critic 自审)。试点后从下次大改动起严格走完整流程。详见 [`docs/process/STATE.md`](docs/process/STATE.md)。
```

改为:
```markdown
> **流程状态**: 本项目作为 5 phase 流程的**试点**,所有 phase 标 [x] LEGACY(实施在流程沉淀前完成,未走 critic 自审)。试点后从下次大改动起严格走完整流程。流程模板见 [pm-template/docs/process/](https://github.com/YyItRoad/pm-template/tree/main/docs/process/README.md)。
```

- [ ] **Step 9.2-9.7: 替换 6 个 phase 文档(每文件 2-3 处)**

`docs/00_charter.md` 改 4 处:
- `process/templates/00_charter.md` → `https://github.com/YyItRoad/pm-template/tree/main/docs/process/templates/00_charter.md`
- `process/STATE.md` → `https://github.com/YyItRoad/pm-template/tree/main/docs/process/STATE.md`
- `process/README.md` → `https://github.com/YyItRoad/pm-template/tree/main/docs/process/README.md`
- `docs/process/STATE.md` 引用 → 同上

`docs/01_requirements.md` 改 2 处:`process/STATE.md` × 2
`docs/02_high_level_design.md` 改 3 处:`process/templates/02_high_level_design.md` + `process/STATE.md` × 2
`docs/03a_business_process.md` 改 3 处:`process/templates/03_detailed_design.md § A` + `process/STATE.md` × 2
`docs/03b_api_design.md` 改 3 处:同上 § B
`docs/03c_data_schema.md` 改 3 处:同上 § C

**统一替换模式**(可在每个文件内做):
- `](process/` → `](https://github.com/YyItRoad/pm-template/tree/main/docs/process/`
- `](docs/process/` → `](https://github.com/YyItRoad/pm-template/tree/main/docs/process/`
- `[docs/process/](docs/process/README.md)` → `[docs/process/](https://github.com/YyItRoad/pm-template/tree/main/docs/process/README.md)`

(具体每个文件的修改点用 Read + Edit 工具逐处改)

- [ ] **Step 9.8: 验证 KidBudget 内无残留 `docs/process/` 内部引用**

```bash
cd /Users/yangyang/Desktop/Github/KidBudget
# docs/process/ 目录已被 move(若还没 move,先 Task 10)
grep -rn "docs/process/" README.md docs/00_charter.md docs/01_requirements.md docs/02_high_level_design.md docs/03a_business_process.md docs/03b_api_design.md docs/03c_data_schema.md 2>&1
# 预期:无输出(全部已改为 https:// 形式)
```

- [ ] **Step 9.9: commit KidBudget 7 文件改动**

```bash
cd /Users/yangyang/Desktop/Github/KidBudget
git add README.md docs/00_charter.md docs/01_requirements.md docs/02_high_level_design.md docs/03a_business_process.md docs/03b_api_design.md docs/03c_data_schema.md
git -c user.name="YyItRoad" -c user.email="yyitroad@users.noreply.github.com" \
    commit -m "docs: point process/ refs to pm-template GitHub URL"
```

**预期**: KidBudget 1 commit,7 文件 modified。

---

### Task 10: KidBudget 侧 docs/process/ 删除 + 功能说明.md 同步

**Files in KidBudget:**
- Delete: 整个 `docs/process/` 目录(已被 move 走,现在显式 commit 删除)
- Modify: `docs/功能说明.md`(可能含 docs/process/ 引用)

- [ ] **Step 10.1: 验证 KidBudget 其它文件无 docs/process/ 引用**

```bash
cd /Users/yangyang/Desktop/Github/KidBudget
grep -rn "docs/process/" --include="*.md" --include="*.py" --include="*.sh" --include="*.yml" \
   --exclude-dir=docs/process --exclude-dir=.git --exclude-dir=node_modules --exclude-dir=__pycache__ 2>&1
# 预期:无输出(Task 9 已清理 phase 文档;此步检查其它文件)
```

如发现 `docs/功能说明.md` 等其它文件有引用,同 Task 9.2 模式替换为 pm-template URL。

- [ ] **Step 10.2: 删除 docs/process/ + commit**

```bash
cd /Users/yangyang/Desktop/Github/KidBudget
git rm -r docs/process/
git -c user.name="YyItRoad" -c user.email="yyitroad@users.noreply.github.com" \
    commit -m "docs: remove docs/process/ (moved to pm-template repo)"
```

**预期**: KidBudget 1 commit,docs/process/ 整个目录删除。

---

### Task 11: 全量验证 + push

- [ ] **Step 11.1: pm-template 文件结构验证**

```bash
cd /Users/yangyang/Desktop/Github/pm-template
find . -type f -not -path "./.git/*" | sort
```

**预期 27 个文件**:
- 4 顶层(LICENSE / README.md / .gitignore / docs/)
- 3 docs/process/ 顶层
- 4 docs/process/templates/
- 5 docs/process/dod/
- 8 docs/process/critics/(7 + .gitkeep)
- 1 docs/process/tech_stack.md
- 2 docs/superpowers/specs/(tech-stack + process-template)
- 1 docs/superpowers/plans/

- [ ] **Step 11.2: 全仓库零 KidBudget 内容验证**

```bash
cd /Users/yangyang/Desktop/Github/pm-template
grep -rn "KidBudget\|yyitroad\|2026-06-09" \
   --exclude-dir=.git --exclude-dir=node_modules 2>&1
# 预期:无输出(任何文件)
```

**如命中**:立即修复对应文件,再跑一次验证。

- [ ] **Step 11.3: 9 处改动全部到位**

```bash
cd /Users/yangyang/Desktop/Github/pm-template

# 1. tech_stack.md 存在
test -f docs/process/tech_stack.md && echo "✓ tech_stack.md"

# 2-4. 3 templates
grep -q "## 2.5 技术栈确认" docs/process/templates/00_charter.md && echo "✓ 00_charter §2.5"
grep -q "tech_stack.md" docs/process/templates/02_high_level_design.md && echo "✓ 02 stack ref"
grep -q "tech_stack.md" docs/process/templates/03_detailed_design.md && echo "✓ 03 stack ref"

# 5-7. 3 DoD
grep -q "§2.5 技术栈确认" docs/process/dod/00_charter.md && echo "✓ dod 00 lock"
grep -q "L1 锁层" docs/process/dod/02_high_level_design.md && echo "✓ dod 02 L1"
grep -q "§3.6 §3.7" docs/process/dod/03_detailed_design.md && echo "✓ dod 03 align"

# 8-10. 3 critic
grep -q "L1 锁层" docs/process/critics/02_high_level_design.md && echo "✓ critic 02 L1"
grep -q "§3.3 数据层" docs/process/critics/03c_data_schema.md && echo "✓ critic 03c data"
grep -q "Phase 0 §2.5" docs/process/critics/04_implementation.md && echo "✓ critic 04 impl"

# 11-12. process/README.md + CHANGELOG.md
grep -q "tech_stack" docs/process/README.md && echo "✓ process/README tech_stack entry"
grep -q "v0.2.0" docs/process/CHANGELOG.md && echo "✓ process/CHANGELOG v0.2.0"
```

**预期**: 12 行 ✓。

- [ ] **Step 11.4: KidBudget 侧无残留 docs/process/ 引用**

```bash
cd /Users/yangyang/Desktop/Github/KidBudget
test ! -d docs/process/ && echo "✓ docs/process/ 目录已删除"
grep -rn "docs/process/" --include="*.md" --include="*.py" --include="*.sh" --include="*.yml" \
   --exclude-dir=.git --exclude-dir=node_modules --exclude-dir=__pycache__ 2>&1 | head
# 预期:无输出
```

- [ ] **Step 11.5: Git log 验证(双仓库)**

```bash
echo "=== pm-template commits ==="
cd /Users/yangyang/Desktop/Github/pm-template
git log --oneline

echo "=== KidBudget commits ==="
cd /Users/yangyang/Desktop/Github/KidBudget
git log --oneline | head -5
```

**pm-template 预期 11 commit**:
```
chore: scaffold repo (LICENSE + README + .gitignore)
docs(process): move 16 template/dod/critic files from KidBudget
docs(process): add pm-template-specific README/STATE/CHANGELOG
docs(specs): move process template design spec from KidBudget
docs(process): add standard tech stack spec (v1.0)
feat(process): add tech stack confirmation to 3 phase templates
feat(process): add tech stack DoD items to 3 phases
feat(process): add tech stack critic checks to 3 phases
docs(pm-template): add standard tech stack design spec        ← 已存在的
docs(pm-template): add tech stack implementation plan           ← 已存在的
```

**KidBudget 预期新增 3 commit**:
```
docs: point process/ refs to pm-template GitHub URL
docs: remove docs/process/ (moved to pm-template repo)
docs(specs): move process template design spec to pm-template
```

- [ ] **Step 11.6: push pm-template 到 GitHub**

```bash
cd /Users/yangyang/Desktop/Github/pm-template
git push -u origin main
```

**预期**: 推送成功,GitHub 仓库 https://github.com/YyItRoad/pm-template 显示 11 commit + 24 文档。

- [ ] **Step 11.7: push KidBudget 到 GitHub**

```bash
cd /Users/yangyang/Desktop/Github/KidBudget
git push -u origin main
```

- [ ] **Step 11.8: 浏览器手测 — "Use this template"**

1. 打开 https://github.com/YyItRoad/pm-template
2. 确认右上角绿色 "Use this template" 按钮可见
3. 点击 → "Create a new repository" 页面 → 选 owner + 输 repo 名 → 创建
4. 跳到新仓库 → 验证 `docs/process/tech_stack.md` 渲染正常,`docs/process/README.md` 链接通

**预期**: 4 步通过。

---

## Verification Checklist(签收用)

### pm-template
- [ ] 27 文件全部到位(Task 11.1)
- [ ] **全仓库零 KidBudget / yyitroad / 2026-06-09 引用**(Task 11.2)
- [ ] 12 处改动(tech_stack.md + 3 templates + 3 DoD + 3 critic + process README/CHANGELOG)全部到位(Task 11.3)
- [ ] Git log 11 commit 按预期顺序(Task 11.5)
- [ ] push 成功 + "Use this template" 按钮可点(Task 11.6/11.8)

### KidBudget
- [ ] `docs/process/` 目录被删除(Task 11.4)
- [ ] 7 phase 文档 + README 引用全部改 pm-template URL(Task 9)
- [ ] 其它文件无残留 docs/process/ 引用(Task 10.1)
- [ ] Git log 新增 3 commit(Task 11.5)
- [ ] push 成功(Task 11.7)
