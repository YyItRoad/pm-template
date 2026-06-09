# 标准技术栈规范实施 Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 把 KidBudget 5-phase 流程模板资产 + 标准技术栈规范(`tech_stack.md`)同步到 pm-template 仓库,11 个 commit 完成初始化,GitHub "Use this template" 可用。

**Architecture:** 单仓库扁平结构,`docs/process/` 物理隔离模板资产与项目产物(用户用模板时新建 `docs/00_charter.md` 等)。`tech_stack.md` 是新加的"标准栈规范",在 Phase 0 通过 §2.5 签字 = 锁。

**Tech Stack:** Markdown(纯文档项目,无运行时代码)、Conventional Commits、GitHub Template Repository。

**Spec 来源:** `docs/superpowers/specs/standard-tech-stack-design.md`(已批准)
**资产源:** `KidBudget/docs/process/`(20 个文件)→ `pm-template/docs/process/`

---

## File Structure

### pm-template 终态(11 commit 后)

```
pm-template/
├── LICENSE                           ← 新建(MIT)
├── README.md                         ← 新建(双语,5 phase + tech_stack 入口)
├── .gitignore                        ← 新建(标准 Python + Node ignore)
└── docs/
    ├── process/                      ← 模板资产(从 KidBudget 同步)
    │   ├── README.md                 ← 改:去 KidBudget 特定化
    │   ├── STATE.md                  ← 改:空状态(等用户填)
    │   ├── CHANGELOG.md              ← 改:加 v0.2.0 entry
    │   ├── tech_stack.md             ← 新建(标准栈规范,~500 行)
    │   ├── templates/                ← 复制(5 文件,verbatim)
    │   │   ├── 00_charter.md         ← 改:加 §2.5 技术栈确认
    │   │   ├── 01_requirements.md
    │   │   ├── 02_high_level_design.md   ← 改:加 stack 引用
    │   │   ├── 03_detailed_design.md     ← 改:加 stack 引用(§A/§B/§C)
    │   │   └── (无 04_implementation.md)
    │   ├── dod/                      ← 复制(5 文件,部分改)
    │   │   ├── 00_charter.md         ← 改:加锁 Phase 0 DoD
    │   │   ├── 01_requirements.md
    │   │   ├── 02_high_level_design.md   ← 改:加 L1 偏航 DoD
    │   │   ├── 03_detailed_design.md     ← 改:加 §3.6 §3.7 对齐 DoD
    │   │   └── 04_implementation.md
    │   └── critics/                  ← 复制(7 文件 + .gitkeep,部分改)
    │       ├── 00_charter.md
    │       ├── 01_requirements.md
    │       ├── 02_high_level_design.md   ← 改:加 stack 检查
    │       ├── 03a_business_process.md
    │       ├── 03b_api_design.md
    │       ├── 03c_data_schema.md        ← 改:加数据层检查
    │       ├── 04_implementation.md     ← 改:加代码-选型一致性检查
    │       └── reports/.gitkeep
    └── superpowers/
        ├── specs/
        │   └── standard-tech-stack-design.md  ← 已存在(本 plan 不动)
        └── plans/
            └── standard-tech-stack-implementation.md  ← 本文件
```

### 文件来源对照表

| 终态文件 | 来源 | 处理方式 |
|---|---|---|
| `LICENSE` | 全新 | 写 MIT |
| `README.md`(根) | 全新 | 写双语,5 phase + tech_stack 入口 |
| `.gitignore` | 全新 | 标准 Python + Node |
| `docs/process/README.md` | KidBudget 同名 | 改:KidBudget 特定化 → 通用 |
| `docs/process/STATE.md` | KidBudget 同名 | 改:LEGACY 内容 → 空模板 |
| `docs/process/CHANGELOG.md` | KidBudget 同名 | 改:加 v0.2.0 entry |
| `docs/process/tech_stack.md` | 全新 | 写:按 spec §3 |
| `docs/process/templates/00_charter.md` | KidBudget 同名 | 复制 + 改:加 §2.5 |
| `docs/process/templates/01_requirements.md` | KidBudget 同名 | 复制 verbatim |
| `docs/process/templates/02_high_level_design.md` | KidBudget 同名 | 复制 + 改:加 1 句 stack 引用 |
| `docs/process/templates/03_detailed_design.md` | KidBudget 同名 | 复制 + 改:§A/§B/§C 加引用 |
| `docs/process/dod/00_charter.md` | KidBudget 同名 | 复制 + 改:加锁 DoD |
| `docs/process/dod/01_requirements.md` | KidBudget 同名 | 复制 verbatim |
| `docs/process/dod/02_high_level_design.md` | KidBudget 同名 | 复制 + 改:加 L1 偏航 DoD |
| `docs/process/dod/03_detailed_design.md` | KidBudget 同名 | 复制 + 改:加 §3.6 §3.7 DoD |
| `docs/process/dod/04_implementation.md` | KidBudget 同名 | 复制 verbatim |
| `docs/process/critics/*.md` | KidBudget 同名 | 7 文件:3 改 + 4 verbatim |
| `docs/process/critics/reports/.gitkeep` | KidBudget 同名 | 复制 verbatim |

---

## 命名/格式约定(全局)

- **不**在 spec/plan 名称里带日期(`feedback_spec_no_dates.md` 铁律)
- **不**在正文写"YYYY-MM-DD 已批准"等具体日期
- 模板的 `YYYY-MM-DD` **占位符**保留(用户填写时替换)
- Conventional Commits:`docs:` / `chore:` / `feat:`
- 中文为主,关键术语中英对照

---

## 任务

### Task 1: 仓库根基础文件(LICENSE + README + .gitignore)

**Files:**
- Create: `/Users/yangyang/Desktop/Github/pm-template/LICENSE`
- Create: `/Users/yangyang/Desktop/Github/pm-template/README.md`
- Create: `/Users/yangyang/Desktop/Github/pm-template/.gitignore`

- [ ] **Step 1.1: 写 LICENSE(MIT)**

```bash
cat > LICENSE <<'EOF'
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

- [ ] **Step 1.2: 写根 README.md(双语)**

README 写明:
- 仓库名 + 一句话描述(中英)
- 仓库用途:**5-phase 项目流程模板 + 标准技术栈规范**
- 3 个入口:
  1. `docs/process/README.md` — 流程使用指南
  2. `docs/process/tech_stack.md` — 标准技术栈规范
  3. `docs/superpowers/specs/standard-tech-stack-design.md` — 设计 spec
- "怎么用":GitHub "Use this template" 按钮 → 复制干净起点 → Phase 0 签字 = 锁

模板内容(创建时填):

```markdown
# pm-template / 项目管理模板

> **Standard 5-phase project management process template + tech stack spec**
> 标准 5 阶段项目管理流程模板 + 技术栈规范

## 用途 / Purpose

为 **web 应用(后端业务层 + 后台管理 SPA + 关系数据库)** 型项目提供开箱即用的:
- **5 phase 流程** — 立项 / 需求 / 概要设计 / 详细设计 / 实现,每 phase 三件套(模板 + DoD + critic)
- **标准技术栈** — L1/L2/L3 锁级,Phase 0 签字 = 锁
- **双层验证** — AI critic 自审 + 用户签字

## 3 个入口 / 3 Entry Points

| 用途 | 路径 |
|---|---|
| 流程使用指南 / How to use the process | [`docs/process/README.md`](docs/process/README.md) |
| 标准技术栈规范 / Standard tech stack | [`docs/process/tech_stack.md`](docs/process/tech_stack.md) |
| 设计 spec / Design rationale | [`docs/superpowers/specs/standard-tech-stack-design.md`](docs/superpowers/specs/standard-tech-stack-design.md) |

## 怎么用 / How to Use

1. **复制模板**: GitHub 顶部 → **"Use this template"** → 选 owner/repo → 创建
2. **初始化项目**: 把 `docs/process/templates/0X_*.md` 复制到 `docs/0X_*.md`,按模板填空
3. **签字锁 Phase 0**: 填 `docs/00_charter.md` §2.5,引用 [`docs/process/tech_stack.md`](docs/process/tech_stack.md) 选标准栈
4. **走完 5 phase**: 每 phase 完成 → 跑 critic → 勾 DoD → 签字 → 锁

## 适用 / Not Applicable

| ✅ 适用 | ❌ 不适用 |
|---|---|
| Web 应用(后端 + 管理端 SPA + 关系数据库) | CLI 工具 / 库 / SDK |
| 单体服务 / 中小规模 | 嵌入式 / 移动端原生 |
| 国内私有化部署 | 全球化 / 多区域部署 |

详细规范见 `docs/process/tech_stack.md` §1.3。

## 流程示意 / Process Flow

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

## 许可证 / License

MIT — 详见 [LICENSE](LICENSE)
```

- [ ] **Step 1.3: 写 .gitignore**

```bash
cat > .gitignore <<'EOF'
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
git commit -m "chore: scaffold repo (LICENSE + README + .gitignore)"
```

**预期**: 3 文件 created,1 commit。

---

### Task 2: 复制 docs/process/ 顶层 3 文件(改造版)

**Files:**
- Create: `docs/process/README.md`(从 KidBudget 改造)
- Create: `docs/process/STATE.md`(空模板)
- Create: `docs/process/CHANGELOG.md`(从 KidBudget 改造 + 加 v0.2.0)

- [ ] **Step 2.1: 复制 README.md,改造 KidBudget 特定内容**

```bash
cp /Users/yangyang/Desktop/Github/KidBudget/docs/process/README.md \
   /Users/yangyang/Desktop/Github/pm-template/docs/process/README.md
```

修改 `pm-template/docs/process/README.md`:
- "本目录(`docs/process/`)" → 保留
- "当前使用本流程的具体项目(KidBudget)的 phase 文档在 `docs/00_charter.md`..." → 改为 "新项目用本模板时,phase 文档**也放在** `docs/0X_*.md`(与本目录物理隔离)"
- "完整设计说明见: `docs/superpowers/specs/2026-06-09-standard-process-template-design.md`" → 改为 "完整设计说明见: `docs/superpowers/specs/standard-process-template-design.md`"
- 同步加"技术栈规范"章节入口,链向 `docs/process/tech_stack.md`(内容参考 spec §4.1 形式)

- [ ] **Step 2.2: 写空 STATE.md 模板**

```bash
cat > /Users/yangyang/Desktop/Github/pm-template/docs/process/STATE.md <<'EOF'
# 流程流转状态

> 锁定状态: [ ] 未开始 / [~] 进行中 / [x] 已锁 / [SKIP] / [UNLOCKED] / [x] LEGACY
> 试点项目历史 phase(实施时未走本流程)用 `[x] LEGACY` 标记

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

- [ ] **Step 2.3: 复制 CHANGELOG.md + 加 v0.2.0 entry**

```bash
cp /Users/yangyang/Desktop/Github/KidBudget/docs/process/CHANGELOG.md \
   /Users/yangyang/Desktop/Github/pm-template/docs/process/CHANGELOG.md
```

修改 `pm-template/docs/process/CHANGELOG.md`:
- 顶部 "v0.1.0 (2026-06-09)" → 去掉括号内日期,改为 "v0.1.0"
- "**设计 spec**: `docs/superpowers/specs/2026-06-09-standard-process-template-design.md`" → 改为 "**设计 spec**: `docs/superpowers/specs/standard-process-template-design.md`"
- **追加** v0.2.0 章节(在 v0.1.0 之上):

```markdown
## v0.2.0 — 新增标准技术栈规范

**背景**: 5-phase 流程跑通后,KidBudget 等项目反复出现"技术选型从零开始 / AI 自由发挥选错库"的问题。沉淀一套标准栈规范,Phase 0 签字 = 锁。

**v0.2.0 决定**:
- 新增 `docs/process/tech_stack.md` — 9 层(L1/L2/L3 锁级)+ 后端 4 层架构
- 9 处模板/DoD/critic 资产加 stack 检查/引用
- 引入"轻量级 vs 重量级偏航"分流(L3 子选 vs L1/L2 大改)
- 升级不影响已锁定项目(v0.1 锁定的 KidBudget 等继续生效)

**设计 spec**: `docs/superpowers/specs/standard-tech-stack-design.md`
```

- [ ] **Step 2.4: 验证 + commit**

```bash
cd /Users/yangyang/Desktop/Github/pm-template
ls -la docs/process/{README.md,STATE.md,CHANGELOG.md}
git add docs/process/README.md docs/process/STATE.md docs/process/CHANGELOG.md
git commit -m "docs(process): seed top-level assets (README/STATE/CHANGELOG)"
```

**预期**: 3 文件 created,1 commit。`STATE.md` 全部 `[ ]`,`CHANGELOG.md` 有 v0.1.0 + v0.2.0 两节。

---

### Task 3: 复制 templates/(5 文件,2 改 + 3 verbatim)

**Files:**
- Create: `docs/process/templates/01_requirements.md`(verbatim)
- Create: `docs/process/templates/02_high_level_design.md`(verbatim 本步,改在 Task 7)
- Create: `docs/process/templates/03_detailed_design.md`(verbatim 本步,改在 Task 7)
- Create: `docs/process/templates/00_charter.md`(verbatim 本步,改在 Task 7)
- Create: `docs/process/templates/04_implementation.md`?(无,跳过)

- [ ] **Step 3.1: 复制 5 个模板 verbatim**

```bash
cd /Users/yangyang/Desktop/Github/pm-template
cp /Users/yangyang/Desktop/Github/KidBudget/docs/process/templates/00_charter.md \
   docs/process/templates/00_charter.md
cp /Users/yangyang/Desktop/Github/KidBudget/docs/process/templates/01_requirements.md \
   docs/process/templates/01_requirements.md
cp /Users/yangyang/Desktop/Github/KidBudget/docs/process/templates/02_high_level_design.md \
   docs/process/templates/02_high_level_design.md
cp /Users/yangyang/Desktop/Github/KidBudget/docs/process/templates/03_detailed_design.md \
   docs/process/templates/03_detailed_design.md
```

- [ ] **Step 3.2: 验证 + commit**

```bash
cd /Users/yangyang/Desktop/Github/pm-template
ls -la docs/process/templates/
diff -q /Users/yangyang/Desktop/Github/KidBudget/docs/process/templates/ \
        docs/process/templates/
git add docs/process/templates/
git commit -m "docs(process): copy 4 phase templates verbatim from KidBudget"
```

**预期**: 4 文件 created(没有 04),1 commit。`diff` 无输出(内容一致)。

---

### Task 4: 复制 dod/(5 文件,verbatim,改在 Task 8)

**Files:**
- Create: `docs/process/dod/*.md`(5 文件 verbatim 本步,改在 Task 8)

- [ ] **Step 4.1: 复制 5 个 DoD verbatim**

```bash
cd /Users/yangyang/Desktop/Github/pm-template
mkdir -p docs/process/dod
for f in 00_charter 01_requirements 02_high_level_design 03_detailed_design 04_implementation; do
  cp /Users/yangyang/Desktop/Github/KidBudget/docs/process/dod/${f}.md \
     docs/process/dod/${f}.md
done
```

- [ ] **Step 4.2: 验证 + commit**

```bash
cd /Users/yangyang/Desktop/Github/pm-template
ls docs/process/dod/
diff -r /Users/yangyang/Desktop/Github/KidBudget/docs/process/dod/ \
       docs/process/dod/
git add docs/process/dod/
git commit -m "docs(process): copy 5 DoD checklists verbatim from KidBudget"
```

**预期**: 5 文件 created,1 commit。`diff -r` 无输出。

---

### Task 5: 复制 critics/(7 文件 + .gitkeep,verbatim,改在 Task 9)

**Files:**
- Create: `docs/process/critics/*.md`(7 文件 verbatim 本步,3 改在 Task 9)
- Create: `docs/process/critics/reports/.gitkeep`

- [ ] **Step 5.1: 复制 7 个 critic + .gitkeep**

```bash
cd /Users/yangyang/Desktop/Github/pm-template
mkdir -p docs/process/critics/reports
for f in 00_charter 01_requirements 02_high_level_design 03a_business_process 03b_api_design 03c_data_schema 04_implementation; do
  cp /Users/yangyang/Desktop/Github/KidBudget/docs/process/critics/${f}.md \
     docs/process/critics/${f}.md
done
cp /Users/yangyang/Desktop/Github/KidBudget/docs/process/critics/reports/.gitkeep \
   docs/process/critics/reports/.gitkeep
```

- [ ] **Step 5.2: 验证 + commit**

```bash
cd /Users/yangyang/Desktop/Github/pm-template
ls docs/process/critics/ docs/process/critics/reports/
diff -r /Users/yangyang/Desktop/Github/KidBudget/docs/process/critics/ \
       docs/process/critics/
git add docs/process/critics/
git commit -m "docs(process): copy 7 critic prompts verbatim from KidBudget"
```

**预期**: 7 + 1 文件 created,1 commit。`diff -r` 无输出。

---

### Task 6: 创建 tech_stack.md(spec §3 全部内容)

**Files:**
- Create: `docs/process/tech_stack.md`(新文件,~500 行)

- [ ] **Step 6.1: 写 tech_stack.md**

按 spec `docs/superpowers/specs/standard-tech-stack-design.md` §3(完整 9 节)逐字落地。结构:

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
- §5 偏航 / Unlock 流程(精简版,spec §5)
- §6.2 版本管理(精简版)

**禁止**: 把 spec 中日期、commit 引用等任何带时间锚定的内容带过来。

- [ ] **Step 6.2: 验证 + commit**

```bash
cd /Users/yangyang/Desktop/Github/pm-template
wc -l docs/process/tech_stack.md
# 预期: ~400-500 行
git add docs/process/tech_stack.md
git commit -m "docs(process): add standard tech stack spec (v1.0)"
```

**预期**: 1 文件 created,1 commit。`wc -l` 报 ~400-500。

---

### Task 7: 修改 3 个 templates(加 stack 引用)

**Files:**
- Modify: `docs/process/templates/00_charter.md`(加 §2.5)
- Modify: `docs/process/templates/02_high_level_design.md`(加 1 句 stack 引用)
- Modify: `docs/process/templates/03_detailed_design.md`(§A/§B/§C 各加 1 句)

- [ ] **Step 7.1: 修改 00_charter.md — 在 §2 目标与非目标 之后插 §2.5**

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

(注意:`YYYY-MM-DD` 去掉,按 user feedback "不写具体日期" — 签字栏只留横线)

- [ ] **Step 7.2: 修改 02_high_level_design.md — §1 架构视图段加 stack 引用**

读取 `docs/process/templates/02_high_level_design.md`,找到 §1 架构视图相关位置,加 1 句:

```markdown
> 技术选型遵循 [`docs/process/tech_stack.md`](tech_stack.md) §3.1-§3.8 锁级;偏离项须在 `docs/00_charter.md` §2.5 签字。
```

- [ ] **Step 7.3: 修改 03_detailed_design.md — §A 流程 / §B 接口 / §C DDL 三处开头各加 1 句**

读取 `docs/process/templates/03_detailed_design.md`,找到 §A 业务流程 / §B 接口设计 / §C 数据表 DDL 三节开头位置,各加:

```markdown
> 命名 / 锁层级遵循 [`docs/process/tech_stack.md` §3.6 §3.7](tech_stack.md)。
```

(放在三节标题下的第一行)

- [ ] **Step 7.4: 验证 + commit**

```bash
cd /Users/yangyang/Desktop/Github/pm-template
# 验证 §2.5 存在
grep -A 2 "## 2.5 技术栈确认" docs/process/templates/00_charter.md
# 验证 stack 引用存在
grep "tech_stack.md" docs/process/templates/02_high_level_design.md
grep -c "tech_stack.md" docs/process/templates/03_detailed_design.md
# 预期:第一个 grep 命中 2 行,第二个命中 1 行,第三个报 3(§A/§B/§C 各 1)
git add docs/process/templates/
git commit -m "feat(process): add tech stack confirmation to 3 phase templates"
```

**预期**: 3 文件修改,1 commit。grep 计数对得上。

---

### Task 8: 修改 3 个 DoD(加 stack 检查项)

**Files:**
- Modify: `docs/process/dod/00_charter.md`(加锁 Phase 0 DoD)
- Modify: `docs/process/dod/02_high_level_design.md`(加 L1 偏航 DoD)
- Modify: `docs/process/dod/03_detailed_design.md`(加 §3.6 §3.7 DoD)

- [ ] **Step 8.1: 修改 dod/00_charter.md — 加 Phase 0 锁 DoD**

读取 `docs/process/dod/00_charter.md`,在末尾追加:

```markdown
- [ ] §2.5 技术栈确认签字完整(按标准栈 / 偏离项 + 理由,均需签字)
```

- [ ] **Step 8.2: 修改 dod/02_high_level_design.md — 加 L1 偏航 DoD**

读取 `docs/process/dod/02_high_level_design.md`,在末尾追加:

```markdown
- [ ] 技术选型未引入 `docs/process/tech_stack.md` §3.1-§3.8 L1 锁层之外的栈(若有偏离,Phase 0 §2.5 已签字)
```

- [ ] **Step 8.3: 修改 dod/03_detailed_design.md — 加 §3.6 §3.7 DoD**

读取 `docs/process/dod/03_detailed_design.md`,在末尾追加:

```markdown
- [ ] §A 流程 / §B 接口 / §C DDL 命名、字段类型、接口风格与 `docs/process/tech_stack.md` §3.6 §3.7 对齐
```

- [ ] **Step 8.4: 验证 + commit**

```bash
cd /Users/yangyang/Desktop/Github/pm-template
grep -l "§2.5 技术栈确认" docs/process/dod/00_charter.md
grep -l "L1 锁层" docs/process/dod/02_high_level_design.md
grep -l "§3.6 §3.7" docs/process/dod/03_detailed_design.md
# 三个 grep 都有命中
git add docs/process/dod/
git commit -m "feat(process): add tech stack DoD items to 3 phases"
```

**预期**: 3 文件修改,1 commit。grep 全命中。

---

### Task 9: 修改 3 个 critic(加 stack 检查项)

**Files:**
- Modify: `docs/process/critics/02_high_level_design.md`(加 stack 检查)
- Modify: `docs/process/critics/03c_data_schema.md`(加数据层规范检查)
- Modify: `docs/process/critics/04_implementation.md`(加代码-选型一致性检查)

- [ ] **Step 9.1: 修改 critic 02_high_level_design.md**

读取 `docs/process/critics/02_high_level_design.md`,在检查项列表末尾追加:

```markdown
- 是否引入 `docs/process/tech_stack.md` §3.1-§3.8 L1 锁层之外的技术栈(若偏离,Phase 0 §2.5 已签字)
```

- [ ] **Step 9.2: 修改 critic 03c_data_schema.md**

读取 `docs/process/critics/03c_data_schema.md`,在检查项列表末尾追加:

```markdown
- 表命名 / 字段类型 / 字符集 / 索引命名是否对齐 `docs/process/tech_stack.md` §3.3 数据层规范
```

- [ ] **Step 9.3: 修改 critic 04_implementation.md**

读取 `docs/process/critics/04_implementation.md`,在检查项列表末尾追加:

```markdown
- 实际代码使用的库 / 工具与 Phase 0 §2.5 选型一致;无未在 Phase 0 / Phase 2 锁过的新依赖
```

- [ ] **Step 9.4: 验证 + commit**

```bash
cd /Users/yangyang/Desktop/Github/pm-template
grep -l "L1 锁层" docs/process/critics/02_high_level_design.md
grep -l "§3.3 数据层" docs/process/critics/03c_data_schema.md
grep -l "Phase 0 §2.5" docs/process/critics/04_implementation.md
# 三个 grep 都命中
git add docs/process/critics/
git commit -m "feat(process): add tech stack critic checks to 3 phases"
```

**预期**: 3 文件修改,1 commit。grep 全命中。

---

### Task 10: 更新 process/README.md(加 tech_stack 入口)+ CHANGELOG v0.2.0 校对

**Files:**
- Modify: `docs/process/README.md`(补 tech_stack 章节入口)
- Modify: `docs/process/CHANGELOG.md`(校对 v0.2.0 内容已加)

- [ ] **Step 10.1: 校对 process/CHANGELOG.md v0.2.0 已有(Task 2.3 加的)**

```bash
cd /Users/yangyang/Desktop/Github/pm-template
grep "## v0.2.0" docs/process/CHANGELOG.md
# 预期命中
```

如果未命中,手动追加(见 Task 2.3 内容)。

- [ ] **Step 10.2: 校对 process/README.md 已含 tech_stack 入口(Task 2.1 改的)**

```bash
cd /Users/yangyang/Desktop/Github/pm-template
grep "tech_stack" docs/process/README.md
# 预期命中 ≥ 1 次
```

如未命中,在 README 末尾追加:

```markdown
## 技术栈规范 / Tech Stack Spec

新项目必须引用 [`tech_stack.md`](tech_stack.md),在 `docs/00_charter.md` §2.5 签字 = 锁。详见 [tech_stack.md](tech_stack.md) §1 锁层级说明。
```

- [ ] **Step 10.3: 验证 + commit**

```bash
cd /Users/yangyang/Desktop/Github/pm-template
git add docs/process/README.md docs/process/CHANGELOG.md
git status
# 预期:无变更(除非 Task 2 的改造有遗漏,这时会有 diff)
git diff --cached --stat
# 预期: 0 行 或 < 5 行修正
git commit --allow-empty -m "docs(process): verify tech stack entry points"
```

**预期**: 0 或少量 commit。空 commit 用 `--allow-empty`。

---

### Task 11: 全量验证 + push

- [ ] **Step 11.1: 文件结构验证**

```bash
cd /Users/yangyang/Desktop/Github/pm-template
find docs -type f | sort
```

**预期输出**(24 个文件):

```
docs/process/CHANGELOG.md
docs/process/README.md
docs/process/STATE.md
docs/process/critics/00_charter.md
docs/process/critics/01_requirements.md
docs/process/critics/02_high_level_design.md
docs/process/critics/03a_business_process.md
docs/process/critics/03b_api_design.md
docs/process/critics/03c_data_schema.md
docs/process/critics/04_implementation.md
docs/process/critics/reports/.gitkeep
docs/process/dod/00_charter.md
docs/process/dod/01_requirements.md
docs/process/dod/02_high_level_design.md
docs/process/dod/03_detailed_design.md
docs/process/dod/04_implementation.md
docs/process/templates/00_charter.md
docs/process/templates/01_requirements.md
docs/process/templates/02_high_level_design.md
docs/process/templates/03_detailed_design.md
docs/process/tech_stack.md
docs/superpowers/plans/standard-tech-stack-implementation.md
docs/superpowers/specs/standard-tech-stack-design.md
```

外加 4 顶层:`LICENSE`、`README.md`、`.gitignore`、`.git/`(共 28 个 entries,24 个文档)。

- [ ] **Step 11.2: 内容验证 — stack 引用全部到位**

```bash
cd /Users/yangyang/Desktop/Github/pm-template
# 9 处改动全部到位
echo "=== 1. tech_stack.md 存在 ==="
ls -la docs/process/tech_stack.md

echo "=== 2-4. 3 个 templates 加了引用 ==="
grep -l "## 2.5 技术栈确认" docs/process/templates/00_charter.md
grep -l "tech_stack.md" docs/process/templates/02_high_level_design.md
grep -l "tech_stack.md" docs/process/templates/03_detailed_design.md

echo "=== 5-7. 3 个 DoD 加了检查项 ==="
grep -l "§2.5 技术栈确认" docs/process/dod/00_charter.md
grep -l "L1 锁层" docs/process/dod/02_high_level_design.md
grep -l "§3.6 §3.7" docs/process/dod/03_detailed_design.md

echo "=== 8-10. 3 个 critic 加了检查项 ==="
grep -l "L1 锁层" docs/process/critics/02_high_level_design.md
grep -l "§3.3 数据层" docs/process/critics/03c_data_schema.md
grep -l "Phase 0 §2.5" docs/process/critics/04_implementation.md

echo "=== 11. process/README.md 含入口 ==="
grep -c "tech_stack" docs/process/README.md

echo "=== 12. process/CHANGELOG.md 含 v0.2.0 ==="
grep "## v0.2.0" docs/process/CHANGELOG.md
```

**预期**: 全部 grep 命中。

- [ ] **Step 11.3: 无日期污染验证(feedback_spec_no_dates 铁律)**

```bash
cd /Users/yangyang/Desktop/Github/pm-template
echo "=== 文件名 ==="
find . -type f -not -path "./.git/*" | grep -E "2026|2025|2027" || echo "OK: 无日期文件名"
echo "=== tech_stack.md / process/README.md / 改造文件 ==="
grep -E "2026|2025|2027" docs/process/tech_stack.md docs/process/README.md docs/process/CHANGELOG.md || echo "OK: 无日期"
echo "=== 模板(占位符 YYYY-MM-DD 允许保留) ==="
grep -c "YYYY-MM-DD" docs/process/templates/*.md
# 预期:每个文件 ≥ 0(占位符可保留,本验证不要求)
```

**预期**: 第一/二段输出 "OK: 无日期";第三段报占位符数(无需修)。

- [ ] **Step 11.4: Git log 验证 — 11 个 commit 顺序**

```bash
cd /Users/yangyang/Desktop/Github/pm-template
git log --oneline
```

**预期输出顺序**(从早到晚):

```
chore: scaffold repo (LICENSE + README + .gitignore)
docs(process): seed top-level assets (README/STATE/CHANGELOG)
docs(process): copy 4 phase templates verbatim from KidBudget
docs(process): copy 5 DoD checklists verbatim from KidBudget
docs(process): copy 7 critic prompts verbatim from KidBudget
docs(process): add standard tech stack spec (v1.0)
feat(process): add tech stack confirmation to 3 phase templates
feat(process): add tech stack DoD items to 3 phases
feat(process): add tech stack critic checks to 3 phases
docs(process): verify tech stack entry points
docs(pm-template): add standard tech stack design spec
```

(注意:设计 spec 的 commit 在最底,因为它是 Task 1 之前提交的)

- [ ] **Step 11.5: push 到 GitHub**

```bash
cd /Users/yangyang/Desktop/Github/pm-template
git push -u origin main
```

**预期**: 推送成功,GitHub 仓库 https://github.com/YyItRoad/pm-template 显示全部 11 个 commit + 24 个文档。

- [ ] **Step 11.6: 浏览器手测 — "Use this template" 按钮**

1. 打开 https://github.com/YyItRoad/pm-template
2. 确认右上角绿色 "Use this template" 按钮可见
3. 点击 → "Create a new repository" 页面 → 选 owner + 输 repo 名 → 创建
4. 跳到新仓库 → 验证 `docs/process/tech_stack.md` 渲染正常,`docs/process/README.md` 链接通

**预期**: 全部 4 步通过。

- [ ] **Step 11.7: 最终 commit 记录**

```bash
cd /Users/yangyang/Desktop/Github/pm-template
git log --oneline | head -15
# 截图或记录 commit hash 供未来 reference
```

**收尾 commit hash**: (填入实际值,例如 `804cedd`)

---

## Verification Checklist(签收用)

- [ ] pm-template 仓库含 24 个文档文件(spec + plan + 22 process 资产)
- [ ] `docs/process/tech_stack.md` 存在,~400-500 行,覆盖 9 节(spec §3)
- [ ] 9 处模板/DoD/critic 改动全部到位(Task 11.2 grep 验证)
- [ ] 文件名 + tech_stack.md / process/README.md / process/CHANGELOG.md **无**日期(Task 11.3 验证)
- [ ] 模板 `YYYY-MM-DD` 占位符保留(用户填空时替换)
- [ ] Git log 11 commit 按预期顺序(Task 11.4)
- [ ] GitHub push 成功,仓库可见(Task 11.5)
- [ ] "Use this template" 按钮可点 + 新仓库可创建 + tech_stack.md 渲染正常(Task 11.6)
