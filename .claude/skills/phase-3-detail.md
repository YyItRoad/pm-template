---
name: phase-3-detail
description: 拉 docs/process/templates/03_detailed_design.md 模板,引导用户拆 3a 业务流程 + 3b API 接口 + 3c 数据表 DDL,跑 3 次 critic,sign-off 后调 update_state 锁 [x] Phase 3。
---

# /phase-3-detail — 详细设计

## 用途

把 Phase 2 概要设计拆成 3 个**可执行**子产物:
- `docs/03a_business_process.md` — 业务流程(状态机 / 时序图)
- `docs/03b_api_design.md` — API 接口清单(path / method / 入参 / 出参 / 错误码)
- `docs/03c_data_schema.md` — 数据表 DDL(CREATE TABLE + 索引 + 注释)

每个子产物独立跑 critic,最后一次性锁 Phase 3。

**写 STATE.md**:Phase 3 → `[x]`(需 3 个子产物 DoD 全过 + 3 个 critic 无 CRITICAL/HIGH + 用户明示锁)

## 触发

```
/phase-3-detail
```

前置:
- Phase 2 ∈ `[x]`
- Phase 3 状态 ∈ `{[ ], [~], [UNLOCKED]}`

## 执行步骤

### 1. 启动检查

**a) 上游检查**:
```bash
python3 -c "...; print(f'Phase 2: {get_current_status(st[2])}')"
```

Phase 2 不是 `[x]` → 报 `ERR_PHASE_LOCKED_BY_UPSTREAM`。

**b) 本 phase 状态 + 版本对齐**:同前。

### 2. 标记 in-progress

```bash
python3 .claude/scripts/update_state.py --phase 3 --status "[~]"
```

### 3. 引导填 3 个子产物

**Phase 3 与 0/1/2 不同**:3 个子产物**串行填写 + 串行 critic**(避免"3a 改了 3c 还没填"的混乱)。

#### 3a 业务流程

读 `docs/process/critics/03a_business_process.md` 看检查项,引导写 `docs/03a_business_process.md`:
- 状态机(每个核心实体,如 Budget / Apply)
- 时序图(关键场景,如"孩子申请 → 父母审批 → 余额变化")
- 异常路径(余额不足 / 重复申请 / 状态非法)

填完跑:
```bash
/critic 3a
```

CRITICAL/HIGH → 停下等改。MEDIUM → 提示但可继续。

#### 3b API 接口

读 `docs/process/critics/03b_api_design.md`,引导写 `docs/03b_api_design.md`:
- 完整 path / method / 入参 JSON Schema / 出参 JSON Schema / 错误码表
- 每个接口对应 Phase 1 AC 编号(便于 Phase 4 critic 做 AC 覆盖)
- 接口分组(webhook / 管理端 / 内部)

填完跑:
```bash
/critic 3b
```

#### 3c 数据表

读 `docs/process/critics/03c_data_schema.md`(已在会话上下文),引导写:
- `docs/03c_data_schema.md`(设计说明:实体关系 + 索引意图)
- `sql/schema.sql` 或 `sql/migrations/V00N__*.sql`(可执行 DDL)

填完跑:
```bash
/critic 3c
```

**Phase 3c critic 重点**:
- DDL 可执行性(`mysql < schema.sql` 无语法错误)
- 字段命名 100% 对齐 tech_stack §2.3(snake_case / DECIMAL(10,2) / DATETIME / utf8mb4)
- 唯一约束 / 索引意图 / 外键说明

### 4. 跑 3 个 DoD

```bash
/dod-check 3
```

`docs/process/dod/03_detailed_design.md` 同时覆盖 3a/3b/3c,一次性全勾。

通过率 < 100% → 列出缺哪几条,等补。

### 5. Sign-off

3 个 critic 报告都展示:
```
> Phase 3 待锁(3 子产物)。
> 3a 业务流程:docs/03a_business_process.md
>   critic: docs/process/critics/reports/03a_*.md(C/H/M/L: 0/0/1/0)
> 3b API 接口:docs/03b_api_design.md
>   critic: docs/process/critics/reports/03b_*.md(C/H/M/L: 0/0/0/0)
> 3c 数据表:docs/03c_data_schema.md + sql/schema.sql
>   critic: docs/process/critics/reports/03c_*.md(C/H/M/L: 1/0/0/0)
> DoD: 18/18 ✓
>
> ⚠️ 3c 有 1 个 CRITICAL,需先修(详 3c 报告)
> 请确认锁:[y / n / c(看 3c critic)]
```

### 6. 锁

```bash
python3 .claude/scripts/update_state.py \
  --phase 3 \
  --status "[x]" \
  --signed-by "<name>" \
  --signed-at "<YYYY-MM-DD>" \
  --critic-report-path "docs/process/critics/reports/03a_*.md,03b_*.md,03c_*.md" \
  --dod-count "<M>/<M>" \
  --template-sha "<pm-template HEAD SHA>"
```

### 7. 提示下一步

> Phase 3 已锁(签字:<name> <YYYY-MM-DD>)。
> 下一步:运行 `/phase-4-implement` 写代码 + e2e。

## 错误处理

| 错误 | 行为 |
|---|---|
| Phase 2 未锁 | 报 `ERR_PHASE_LOCKED_BY_UPSTREAM` |
| Phase 3 是 `[x]` | 报"已锁,需先 unlock" |
| 3c DDL 语法错 | critic CRITICAL,贴 SQL 片段 |
| 3b 接口无对应 AC | critic HIGH |
| 3a 状态机漏异常路径 | critic HIGH |

## 不要做的

- 不在 3c 加新实体(必须先回 Phase 2 加)
- 不在 3b 加新接口方向(必须先回 Phase 2)
- 不在 3a 加 Phase 1 §5 反向需求里"不做"的状态
