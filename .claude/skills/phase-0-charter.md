---
name: phase-0-charter
description: 拉 docs/process/templates/00_charter.md 模板,引导用户填 §1-§6(项目章程),跑 DoD + critic,sign-off 后调 update_state 锁 [x] Phase 0。
---

# /phase-0-charter — 立项

## 用途

引导用户填项目章程 `docs/00_charter.md`,回答"为什么做 / 给谁用 / 边界在哪 / 不能做什么 / 锁哪条技术栈"。

**写 STATE.md**:Phase 0 → `[x]`(需 DoD 全过 + critic 无 CRITICAL/HIGH + 用户明示锁)

## 触发

```
/phase-0-charter
```

前置:Phase 0 状态 ∈ `{[ ], [~], [UNLOCKED]}`(不能是 `[x]` 或 `[x] LEGACY`)。

## 执行步骤

### 1. 启动检查(同 spec §6.3)

**a) 找 STATE.md**:
```bash
python3 -c "import sys; sys.path.insert(0, 'scripts'); from update_state import find_state_file, parse_state, get_current_status; sp = find_state_file(); st = parse_state(sp); print(f'Phase 0: {get_current_status(st[0])}')"
```

- 抛 `StateFileCorruptError` → 报"STATE.md 缺失或损坏,先跑 `/new-project <topic>` 初始化"
- Phase 0 状态是 `[x]` → 报"`Phase 0 已锁,需先 /state --audit --unlock(谨慎) 解锁`"
- Phase 0 状态是 `[x] LEGACY` → 报"`Phase 0 是历史包袱,不可改`"

**b) 版本对齐**:对比 `STATE.md` 记录的 Phase 0 `template_sha` vs pm-template git HEAD。

```bash
# 取 pm-template SHA(子项目用 vendor/pm-template,pm-template 自仓库用 .)
git -C . rev-parse HEAD 2>/dev/null || git -C vendor/pm-template rev-parse HEAD
```

如果 `template_sha` 已记录且与当前 SHA 不一致:
- 提示:`⚠️ pm-template 已升级(<old> → <new>),建议先 /state --audit 决定是否 unlock 重跑`

**c) 上游检查**:Phase 0 是第一 phase,无上游。

### 2. 标记 in-progress(可选)

如果 Phase 0 当前是 `[ ]`:
```bash
python3 .claude/scripts/update_state.py --phase 0 --status "[~]"
```

不阻塞主流程,只是把 STATE.md 留个"进行中"痕迹,防止 `Ctrl+C` 后看不出在干啥。

### 3. 拉模板

读 `docs/process/templates/00_charter.md`,看每个 `##` 段(§1-§6)需要填什么。

**关键段(锁前必填)**:
- §1 基础信息(项目名 / 一句话 / 适用场景 ≥ 3 条)
- §2.1 核心目标 ≥ 3 条(可"是/否"判定)
- §2.2 明确不做的事 ≥ 3 条(防范围蔓延)
- **§2.5 技术栈确认**(必须勾"按标准栈"或"偏离具体项",且签字行必填)
- §3 角色清单 ≥ 1 行
- §4 核心约束 / 禁忌 ≥ 3 条
- §5 / §6(项目自填)

### 4. 引导填空

按模板顺序逐段问用户。**不要一次全问**,一段填完确认再下一段。

**关键提示**:
- §2.5 锁技术栈,后续 phase 不可改;偏离要写理由
- §2.2 "明确不做的事"是给 critic 抓范围蔓延用的,不能空话(详 spec §3 + critics/00_charter.md)
- §4 禁忌要写"违反会导致什么",不能光说"不能做 X"

### 5. 写产物

写到 `docs/00_charter.md`(相对项目根)。

如果项目已用 `Use this template` 从 pm-template 复制,`docs/process/templates/00_charter.md` 是模板,`docs/00_charter.md` 是产物,**别写错位置**。

### 6. 跑 DoD

```bash
/dod-check 0
```

通过率 < 100% → 列出缺哪几条,**停下来等用户补**。不绕过 DoD 强锁。

### 7. 跑 critic

```bash
/critic 0
```

CRITICAL > 0 或 HIGH > 0 → 报告路径给用户,**停下来等用户改**。

MEDIUM > 0 → 提示"建议修但非阻塞,继续请明示"。

### 8. Sign-off 提示(spec §3.2 + §12)

```
> Phase 0 待锁。
> 产物: docs/00_charter.md (<N> 行)
> critic 报告: docs/process/critics/reports/00_charter_<YYYY-MM-DD>.md
>   CRITICAL: 0 / HIGH: 0 / MEDIUM: 0 / LOW: 0
> DoD 勾选: 12/12 ✓
>
> 请确认锁:
>   [y] 锁(签字: <name> <YYYY-MM-DD>)
>   [n] 不锁(返回修改)
>   [c] 只看 critic 报告
```

**用户输入 `y`** → 继续输入:
- `name?`(非空,≤50 字符)
- `date?`(回车默认今天)

**用户输入 `n`** → 问"需修改什么?",回到 §4 重填。

**用户输入 `c`** → 完整展示 critic 报告内容。

### 9. 锁

```bash
python3 .claude/scripts/update_state.py \
  --phase 0 \
  --status "[x]" \
  --signed-by "<name>" \
  --signed-at "<YYYY-MM-DD>" \
  --critic-report-path "docs/process/critics/reports/00_charter_<YYYY-MM-DD>.md" \
  --dod-count "12/12" \
  --template-sha "<pm-template 当前 HEAD SHA>"
```

输出 `✓ update_state(phase=0, status='[x]') 成功` + diff。

### 10. 提示下一步

> Phase 0 已锁(签字:<name> <YYYY-MM-DD>)。
> 下一步:运行 `/phase-1-requirements` 写需求。

## 错误处理

| 错误 | 行为 |
|---|---|
| `ERR_INVALID_TRANSITION` | 当前状态不可进入(已锁 / LEGACY),提示解锁路径 |
| `ERR_MISSING_TEMPLATE` | 模板缺失,提示 git submodule 或 GitHub raw 拉 |
| `ERR_VERSION_MISMATCH` | pm-template 已升,建议先 --audit 再决定 |
| critic 报 CRITICAL/HIGH | 拒绝锁,等用户改产物 |
| DoD 缺项 | 拒绝锁,等用户补 |

## 不要做的

- 不替用户填 §2.5 签字(技术栈 = 项目生死,必须用户明示)
- 不绕过 critic 强锁
- 不写 docs/process/templates/(那是只读模板)
