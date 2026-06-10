---
name: phase-2-design
description: 拉 docs/process/templates/02_high_level_design.md 模板,引导用户写架构/数据/接口清单,跑 DoD + critic,sign-off 后调 update_state 锁 [x] Phase 2。
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

读 `docs/process/templates/02_high_level_design.md`,核心段:

| 段 | 必填项 |
|---|---|
| §1 设计总览 | 一段话讲清"按什么思路拆" |
| §2 架构图 | 文字 / ASCII 图描述系统由哪些模块组成,模块间怎么连 |
| §2.x 数据形态(高层) | 列出"实体"(不写字段),如 User / Budget / Income / Expense / Apply |
| §2.x 接口清单(高层) | 列出"接口方向"(不写 path / method),如"用户信息 webhook(GET) / 记账 webhook(POST) / 审批 webhook(POST)" |
| §3 部署形态 | 容器 / 网络 / 反代 / 域名(对应 tech_stack §2.4) |
| §4 关键技术决策 | 解释"为什么选这条栈"(对应 tech_stack 偏离或锁级提升) |
| §5 风险 / 待办 | 已知风险 + 留给 Phase 3 细化的事项 |
| §6 决策记录 | 实现期改 Phase 1 / Phase 2 的反向回写位置 |

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
| Phase 1 未锁 | 报 `ERR_PHASE_LOCKED_BY_UPSTREAM` |
| Phase 2 是 `[x]` | 报"已锁,需先 unlock" |
| 实体漏覆盖 Phase 1 故事 | critic CRITICAL,提示"§2 数据形态缺 <实体> 用于 <故事>" |
| 接口方向无对应 AC | critic HIGH |
| 部署偏离 tech_stack | critic CRITICAL(需先 unlock Phase 0 改 §2.5) |

## 不要做的

- 不写 path / method(那是 3b)
- 不写字段(那是 3c)
- 不在 Phase 2 加 tech_stack 偏离项(必须先回 Phase 0)
