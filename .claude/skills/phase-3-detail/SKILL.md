---
name: phase-3-detail
description: 拉 docs/process/templates/03_detailed_design.md 模板(段标 [必填]/[可选] 标记),引导用户拆 3a 业务流程 + 3b API 接口 + 3c 数据表 DDL,跑 3 次 critic,sign-off 后调 update_state 锁 [x] Phase 3。
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

**c) Phase 1 + 2 完整性硬 grep**(改动 5,★关键,失败 = exit 不继续):

```bash
# Phase 1:4 anchor 必在 01_requirements.md
REQUIRED_ANCHORS_1=("role-scenario" "edge-scenarios" "exception-paths" "reverse-requirements")
MISSING=()
for anchor in "${REQUIRED_ANCHORS_1[@]}"; do
  if ! grep -q "<!-- ANCHOR: $anchor -->" docs/01_requirements.md 2>/dev/null; then
    MISSING+=("01:$anchor")
  fi
done

# Phase 2:02_high_level_design.md 必含"## 3. 接口清单"段
if ! test -s docs/02_high_level_design.md; then
  MISSING+=("02:file-missing")
elif ! grep -q "^## 3\. " docs/02_high_level_design.md; then
  MISSING+=("02:no-interface-list")
fi

if [ ${#MISSING[@]} -gt 0 ]; then
  echo "ERR_UPSTREAM_INCOMPLETE: ${MISSING[*]}"
  echo "→ 请先 /unlock 对应 phase 补产物,再回 phase 3"
  exit 1
fi
```

**为什么硬 grep**:phase 3 写 03a/3b/3c 时,如果 phase 1 没挖够或 phase 2 接口清单
没写,LLM 会"凭记忆"写一堆没依据的接口。硬 grep 强制上游真有证据。

### 2. 标记 in-progress

```bash
python3 .claude/scripts/update_state.py --phase 3 --status "[~]"
```

### 3. 引导填 3 个子产物

**Phase 3 与 0/1/2 不同**:3 个子产物**串行填写 + 串行 critic**(避免"3a 改了 3c 还没填"的混乱)。

#### 3a 业务流程 [必填]

读 `docs/process/critics/03a_business_process.md` 看检查项,引导写 `docs/03a_business_process.md`:
- 状态机(每个核心实体,如 Budget / Apply)
- 时序图(关键场景,如"孩子申请 → 父母审批 → 余额变化")
- 异常路径(余额不足 / 重复申请 / 状态非法)
- **每个流程必含 2 个 anchor**:`<!-- ANCHOR: process-N-normal -->` 和 `<!-- ANCHOR: process-N-exception -->`(N 是流程编号),缺一 = HIGH

填完跑:
```bash
/critic 3a
```

CRITICAL/HIGH → 停下等改。MEDIUM → 提示但可继续。

#### 3b API 接口 [必填]

读 `docs/process/critics/03b_api_design.md`,引导写 `docs/03b_api_design.md`:
- 完整 path / method / 入参 JSON Schema / 出参 JSON Schema / 错误码表
- 每个接口对应 Phase 1 AC 编号(便于 Phase 4 critic 做 AC 覆盖)
- 接口分组(webhook / 管理端 / 内部)
- **必含 anchor** `<!-- ANCHOR: api-list -->`,接口清单 7 列必填(ID/方法/路径/鉴权/请求体/响应体/错误码),缺列 = HIGH

填完跑:
```bash
/critic 3b
```

#### 3c 数据表 [必填]

读 `docs/process/critics/03c_data_schema.md`(已在会话上下文),引导写:
- `docs/03c_data_schema.md`(设计说明:实体关系 + 索引意图)
- `sql/schema.sql` 或 `sql/migrations/V00N__*.sql`(可执行 DDL)
- **必含 anchor** `<!-- ANCHOR: tables -->`,表注释/字段类型/索引意图 三栏必填,缺 = HIGH

填完跑:
```bash
/critic 3c
```

#### 3 附录(可选)

- 附录 A: 性能 / 容量基线 [可选] —— 简单项目可跳(整段不写)
- 附录 B: 安全 / 合规检查点 [可选] —— 同上

**挂了标题但内容是占位符 = `ERR_OPTIONAL_SECTION_FILLED_BUT_BLANK`**,提示"删标题 / 写内容"二选一。

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
  --template-sha "<pm-template root HEAD SHA>"
```

### 7. 提示下一步

> Phase 3 已锁(签字:<name> <YYYY-MM-DD>)。
> 下一步:运行 `/phase-4-implement` 写代码 + e2e。

## 错误处理

| 错误 | 行为 |
|---|---|
| `ERR_PHASE_1_INCOMPLETE` | phase 1 挖掘证据不全(改动 5 硬 grep),**回 phase 1 unlock 补** |
| `ERR_OPTIONAL_SECTION_FILLED_BUT_BLANK` | 附录 A/B 挂了标题但内容是占位符,提示"删标题 / 写内容"二选一 |
| Phase 2 未锁 | 报 `ERR_PHASE_LOCKED_BY_UPSTREAM` |
| Phase 3 是 `[x]` | 报"已锁,需先 unlock" |
| 3c DDL 语法错 | critic CRITICAL,贴 SQL 片段 |
| 3b 接口无对应 AC | critic HIGH |
| 3a 状态机漏异常路径 | critic HIGH |

## 不要做的

- **不绕过 3a/3b/3c 必填段** —— §A/§B/§C 各子项不可漏
- **不绕过附录 A/B [可选] 的二选一** —— 挂标题空内容 = ERR_OPTIONAL_SECTION_FILLED_BUT_BLANK
- 不在 3c 加新实体(必须先回 Phase 2 加)
- 不在 3b 加新接口方向(必须先回 Phase 2)
- 不在 3a 加 Phase 1 §5 反向需求里"不做"的状态
