---
name: phase-2-design
description: 拉 docs/process/templates/02_high_level_design.md 模板(段标 [必填]/[可选] 标记),引导用户写架构/数据/接口清单,跑 DoD + critic,sign-off 后调 update_state 锁 [x] Phase 2。
---

# /phase-2-design — 概要设计

## 用途

把 Phase 1 需求拆成可实现的概要设计:`docs/02_high_level_design.md`(架构 / 数据形态 / 接口清单 / 部署形态)。

**写 STATE.md**:Phase 2 → `[x]`(需 DoD 全过 + critic 无 CRITICAL/HIGH + 用户明示锁)

## 触发

```
/phase-2-design
```

前置:
- Phase 1 ∈ `[x]`
- Phase 2 状态 ∈ `{[ ], [~], [UNLOCKED]}`

## 执行步骤

### 1. 启动检查

**a) 上游检查**:
```bash
python3 -c "...; print(f'Phase 1: {get_current_status(st[1])}')"
```

Phase 1 不是 `[x]` → 报 `ERR_PHASE_LOCKED_BY_UPSTREAM`。

**b) 本 phase 状态 + 版本对齐**:同 Phase 1。

### 2. 标记 in-progress(可选)

```bash
python3 .claude/scripts/update_state.py --phase 2 --status "[~]"
```

### 3. 拉模板 + 引导填空

读 `docs/process/templates/02_high_level_design.md`,核心段(每段已标 `[必填]` / `[可选]`):

| 段 | 必填项 |
|---|---|
| §1 架构视图 [必填] | 文字 / ASCII 图描述系统由哪些模块组成,模块间怎么连 |
| §2 数据模型(逻辑层) [必填] | 列出"实体"(不写字段),如 User / Budget / Income / Expense / Apply |
| §3 接口清单 [必填] | 列出"接口方向"(不写 path / method),每行必追溯 S-XX |
| §4 非功能需求落点 [必填] | 性能 / 安全 / 可观测 / 可维护(4 项都填,无内容写"N/A") |
| §5 反向设计 [必填] | ≥3 条,标"不引入 X(常见诱因 Y)" |
| §6 决策记录 [必填] | ≥1 条 |
| §7 末尾自查:孤儿检查 [必填] | 机械 grep,必跑 |
| §8 critic + 签字 [必填] | — |
| §9 未来扩展 [可选] | 留 thought experiment;**两种合法状态**:整段不写 / 写了填内容。**挂标题空内容 = `ERR_OPTIONAL_SECTION_FILLED_BUT_BLANK`** |

**关键提示**:
- §2 接口清单列"接口方向",**不写 path / method** — 那是 Phase 3b 的事
- §2 数据形态列"实体",**不写字段** — 那是 Phase 3c 的事
- §4 关键决策:偏离 tech_stack 必须在 Phase 0 §2.5 写过理由,Phase 2 不能再加偏离项
- §6 决策记录:实现 / 部署时改了 Phase 2 的决定,反过来补这一段(spec §3.3 "回写")

### 4. 写产物

写到 `docs/02_high_level_design.md`。

### 5. 跑 DoD

```bash
/dod-check 2
```

### 6. 跑 critic

```bash
/critic 2
```

**Phase 2 critic 重点**(详 `docs/process/critics/02_high_level_design.md`):
- 实体是否覆盖 Phase 1 所有故事
- 接口方向是否能映射到 Phase 1 故事的 AC
- 部署形态是否与 tech_stack §2.4 一致(无擅自偏离)
- §6 决策记录是否每条"理由 + 备选 + 决定"

### 7. Sign-off

### 8. 锁

```bash
python3 .claude/scripts/update_state.py \
  --phase 2 \
  --status "[x]" \
  --signed-by "<name>" \
  --signed-at "<YYYY-MM-DD>" \
  --critic-report-path "docs/process/critics/reports/02_high_level_design_<YYYY-MM-DD>.md" \
  --dod-count "<M>/<M>" \
  --template-sha "<pm-template root HEAD SHA>"
```

### 9. 提示下一步

> Phase 2 已锁(签字:<name> <YYYY-MM-DD>)。
> 下一步:运行 `/phase-3-detail` 写详细设计(3a 业务流程 / 3b 接口 / 3c 数据表)。

## 错误处理

| 错误 | 行为 |
|---|---|
| `ERR_PHASE_1_INCOMPLETE` | phase 1 挖掘证据不全(改动 5 硬 grep),**回 phase 1 unlock 补** |
| `ERR_OPTIONAL_SECTION_FILLED_BUT_BLANK` | §9 未来扩展挂了标题但内容是占位符,提示"删标题 / 写内容"二选一 |
| Phase 1 未锁 | 报 `ERR_PHASE_LOCKED_BY_UPSTREAM` |
| Phase 2 是 `[x]` | 报"已锁,需先 unlock" |
| 实体漏覆盖 Phase 1 故事 | critic CRITICAL,提示"§2 数据形态缺 <实体> 用于 <故事>" |
| 接口方向无对应 AC | critic HIGH |
| 部署偏离 tech_stack | critic CRITICAL(需先 unlock Phase 0 改 §2.5) |

## 不要做的

- **不绕过 §9 [可选] 的二选一** —— 挂标题空内容 = ERR_OPTIONAL_SECTION_FILLED_BUT_BLANK
- 不写 path / method(那是 3b)
- 不写字段(那是 3c)
- 不在 Phase 2 加 tech_stack 偏离项(必须先回 Phase 0)
