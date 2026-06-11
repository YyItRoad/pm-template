---
name: critic
description: 单跑 pm-template 的 critic 模板,对指定 phase 产物做自审,产报告存档到 docs/process/critics/reports/。
---

# /critic <phase> — 单跑 critic 自审

## 用途

按 `docs/process/critics/0X_*.md` 模板,对指定 phase 的产物(artifact)做自审,把报告写到 `docs/process/critics/reports/`。

**不写 STATE.md**。只产报告。

## 触发

```
/critic 0         # 跑 Phase 0 charter 自审
/critic 1         # 跑 Phase 1 requirements 自审
/critic 2         # 跑 Phase 2 high-level design 自审
/critic 3a        # 跑 Phase 3a business process 自审
/critic 3b        # 跑 Phase 3b API design 自审
/critic 3c        # 跑 Phase 3c data schema 自审
/critic 4         # 跑 Phase 4 implementation 自审
/critic change/feature    # 跑 feature 变更自审
/critic change/bugfix     # 跑 bugfix 变更自审
/critic change/refactor   # 跑 refactor 变更自审
/critic change/hotfix     # 跑 hotfix 变更自审
/critic change/doc        # 跑 doc 变更自审
/critic change/decision   # 跑 ADR 自审
```

## 执行步骤

### 1. 取 critic 模板

按 phase 编号取 `docs/process/critics/<phase>.md`:

| 输入 | 模板路径 |
|---|---|
| `0` | `docs/process/critics/00_charter.md` |
| `1` | `docs/process/critics/01_requirements.md` |
| `2` | `docs/process/critics/02_high_level_design.md` |
| `3a` | `docs/process/critics/03a_business_process.md` |
| `3b` | `docs/process/critics/03b_api_design.md` |
| `3c` | `docs/process/critics/03c_data_schema.md` |
| `4` | `docs/process/critics/04_implementation.md` |
| `change/feature` | `docs/process/critics/change/feature.md` |
| `change/bugfix` | `docs/process/critics/change/bugfix.md` |
| `change/refactor` | `docs/process/critics/change/refactor.md` |
| `change/hotfix` | `docs/process/critics/change/hotfix.md` |
| `change/doc` | `docs/process/critics/change/doc.md` |
| `change/decision` | `docs/process/critics/change/decision.md` |

缺失时:
- 项目本地无 → 报 `ERR_MISSING_TEMPLATE`
- 尝试从 GitHub raw 拉(URL 模板见 spec §5)
- 离线 → 提示"手动 git submodule add pm-template 补齐"

`change/<type>` 输入不合法(不在 `feature|bugfix|refactor|hotfix|doc` 白名单)→ 报 `ERR_CHANGE_TYPE_INVALID`,提示看 `docs/process/TODO.md` 扩展。

### 2. 确认 artifact 存在

| phase | artifact 路径 |
|---|---|
| 0 | `docs/00_charter.md` |
| 1 | `docs/01_requirements.md` |
| 2 | `docs/02_high_level_design.md` |
| 3a | `docs/03a_business_process.md` |
| 3b | `docs/03b_api_design.md` |
| 3c | `docs/03c_data_schema.md` |
| 4 | `<test/e2e 报告路径>` + 代码 |
| `change/<type>` | `docs/changes/NNNN-<type>-<name>.md`(由 /change 自动分配) |
| `change/decision` | `docs/decisions/NNNN-<title>.md`(由 /decision 自动分配) |

artifact 缺失 → 报错"phase 产物未生成,无法自审"。

### 3. 跑自审(按模板逐条)

读 critic 模板的"你要检查的"段,逐条检查对应 artifact。

**严格按 critic 模板的格式输出**:
- 每条标注 **CRITICAL** / **HIGH** / **MEDIUM** / **LOW**
- CRITICAL 必须列出具体证据(AC 编号 / path / 反向需求条目)
- 不要笼统"看起来 OK"

**例**:
```
## Phase 0 charter 自审报告

### CRITICAL
1. §2.5 技术栈确认段未签字
   - 证据:`docs/00_charter.md` §2.5 末尾无 `[ ] 你本人签字: ___` 勾选
   - 违反:`dod/00_charter.md` DoD-08

### HIGH
(none)

### MEDIUM
1. §3 角色清单列了 5 个角色但只填了 2 个
   - 证据:`docs/00_charter.md` §3 表格有 5 行,3 行内容为空
   - 违反:`dod/00_charter.md` DoD-05

### LOW
(none)
```

### 4. 写报告

**路径**:`docs/process/critics/reports/<phase>_YYYY-MM-DD.md`

变更场景命名不同(避免与 phase 报告冲突):
- 5 phase:`<phase>_YYYY-MM-DD.md`(如 `00_charter_2026-06-10.md`)
- 变更:`change_<type>_YYYY-MM-DD.md`,如:
  - `change_feature_2026-06-10.md`
  - `change_bugfix_2026-06-10.md`
  - `change_refactor_2026-06-10.md`
  - `change_hotfix_2026-06-10.md`
  - `change_doc_2026-06-10.md`
  - `change_decision_2026-06-10.md`

`<YYYY-MM-DD>` 用 `datetime.date.today().isoformat()`(本地时区)。

**前置**:`docs/process/critics/reports/` 目录不存在 → mkdir -p(.gitkeep 已在)。

写完打印:
> ✓ 报告已写:docs/process/critics/reports/00_charter_2026-06-10.md
> CRITICAL: 1 / HIGH: 0 / MEDIUM: 1 / LOW: 0

### 5. 返回信号

**给调用方(`/phase-N-XXX` 或 `/new-project`)**:
- `CRITICAL > 0 或 HIGH > 0` → 提示"报告含 CRITICAL/HIGH,无法锁 phase"
- `MEDIUM > 0` → 提示"可锁但建议修,详报告"
- `全部 LOW 或无问题` → 提示"通过,可锁"

## 自我约束

- critic 是"对产物挑刺",**不修产物**(修产物是 phase skill 的事)
- 不替用户决定"这条算不算 CRITICAL" — 模板怎么说就怎么标
- 报告写完不要立刻 commit(留给用户)

## 不要做的

- 不调用 `update_state()` 写 STATE.md
- 不跑 DoD 自检(那是 `/dod-check` 的事)
- 不改产物文件
