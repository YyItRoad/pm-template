---
name: phase-4-implement
description: 按 03b 接口 + 03c 表 + 01 故事 + AC 写代码 + e2e,跑 critic 验证 AC 覆盖率 + 范围蔓延 + 反向需求,sign-off 后调 update_state 锁 [x] Phase 4。
---

# /phase-4-implement — 实现 + 验证

## 用途

与前 4 phase 不同——**写业务代码,不是文档**。

按 03b 接口清单 + 03c 数据表 + 01 用户故事 + AC,写代码 + e2e 脚本,跑 critic 验证:
1. **AC 覆盖率**(最严重):每个 Phase 1 AC 都有 e2e case
2. **范围蔓延**:代码里有 Phase 1 故事没出现的能力(尤其 admin 私活)
3. **反向需求真没做**:grep Phase 1 §5 反向需求,应 0 命中
4. **接口一致性**:03b path/method vs 实际后端 `@router` 装饰器 100% 一致
5. **部署可启动**:`docker compose up` 起得来

**写 STATE.md**:Phase 4 → `[x]`(DoD 全过 + critic 无 CRITICAL/HIGH + 用户明示锁)

## 触发

```
/phase-4-implement
```

前置:
- Phase 3 ∈ `[x]`
- Phase 4 状态 ∈ `{[ ], [~], [UNLOCKED]}`

## 执行步骤

### 1. 启动检查

**a) 上游检查**:Phase 3 必须 `[x]`,否则 `ERR_PHASE_LOCKED_BY_UPSTREAM`。

**b) 本 phase 状态 + 版本对齐**:同前。

### 2. 标记 in-progress

```bash
python3 .claude/scripts/update_state.py --phase 4 --status "[~]"
```

### 3. 拉设计资产(spec §13 骨架)

```bash
# 接口清单
cat docs/03b_api_design.md
# 数据表
cat docs/03c_data_schema.md
cat sql/schema.sql
# 故事 + AC
cat docs/01_requirements.md
```

把这些装进 context,作为实现期的"合同"。

### 4. TDD 循环(spec §13 第 3 步)

对每个接口(按 03b 顺序):

1. **写测试**:`tests/test_<接口>.py` 或 `tests/integration/test_<接口>.py`
   - happy path(主流程)
   - sad path(鉴权失败 / 字段缺失 / 业务校验失败)
2. **跑测试**:确认先 RED
3. **写实现**:`app/<module>.py` 的 router / service / model
4. **再跑**:确认 GREEN
5. **重构**:在测试保持绿的前提下抽公共代码

> **可选**:用 superpowers:subagent-driven-development 派发子任务做 TDD 实现(详 spec §13 注)
> **不强制**:可以按"实现优先,测试覆盖在末尾一次性补"风格(spec §13 不限制流程)

### 5. 写 e2e 脚本(详 spec §13 第 4 步)

`scripts/e2e_*.sh`:
- 每个 AC 编号至少 1 个 case
- 风格沿用 call() 函数 + `__NOAUTH__` / `__ANY__` 哨兵
- 测真实 HTTP(不走 in-process)

### 6. 跑 critic(spec §13 第 4 步 4 子项)

```bash
/critic 4
```

**Phase 4 critic 重点**(详 `docs/process/critics/04_implementation.md`):

#### AC 覆盖率(最严重)
- 提取 Phase 1 所有 AC 编号
- 对每个 AC 编号,grep `tests/` `e2e_*.sh`,是否有至少 1 个 case
- 缺 = **CRITICAL**(该 AC 没验证就上生产)

**自动化**:
```bash
# 提取 AC 编号
grep -oE "AC-[0-9]+" docs/01_requirements.md | sort -u > /tmp/ac_list.txt
# 检查 e2e 命中
while read ac; do
  if ! grep -rq "$ac" scripts/e2e_*.sh tests/; then
    echo "MISSING: $ac"
  fi
done < /tmp/ac_list.txt
```

#### 范围蔓延
- 提取 03b 接口列表
- 对每个接口 grep `app/`,是否有 @router 装饰器
- 多出 = **CRITICAL**(admin 私活是常见来源)
- 特别注意 `/admin/...` 路径,如果 Phase 1 故事没出现 = CRITICAL

#### 反向需求真没做
- 提取 Phase 1 §5 反向需求
- 对每条 grep 代码,应 0 命中
- 命中 = **CRITICAL**

#### 接口一致性
- diff `docs/03b_api_design.md` 的 path/method 列表 vs `app/` 里的 `@router.get` / `@router.post` 装饰器
- 不一致 = **CRITICAL**

#### 部署可启动
- `docker compose up -d --build` 起得来?
- 失败 = **CRITICAL**

### 7. 跑 DoD

```bash
/dod-check 4
```

**Phase 4 DoD 重点**(详 `docs/process/dod/04_implementation.md`):
- 所有 AC 编号都有 e2e 覆盖
- pytest 通过
- `docker compose up` 起得来
- 范围蔓延 grep 报告已附

### 8. Sign-off

```
> Phase 4 待锁(代码 + e2e)。
> AC 覆盖率: 23/23 ✓
> 反向需求: 0 命中 ✓
> 接口一致性: 0 偏差 ✓
> pytest: 111 passed
> docker compose up: 2 容器 healthy
> critic: docs/process/critics/reports/04_implementation_<YYYY-MM-DD>.md(C/H/M/L: 0/0/2/0)
> DoD: 15/15 ✓
>
> MEDIUM: 2(非阻塞,详报告)
> 请确认锁:[y / n / c(看 critic)]
```

### 9. 锁

```bash
python3 .claude/scripts/update_state.py \
  --phase 4 \
  --status "[x]" \
  --signed-by "<name>" \
  --signed-at "<YYYY-MM-DD>" \
  --critic-report-path "docs/process/critics/reports/04_implementation_<YYYY-MM-DD>.md" \
  --dod-count "<M>/<M>" \
  --template-sha "<pm-template HEAD SHA>"
```

### 10. 提示结束

> Phase 4 已锁(签字:<name> <YYYY-MM-DD>)。
> ✅ 5 phase 全部锁定,进入实施支持模式。
> 维护期改文档:用 `/state --audit` 检查版本对齐,决定是否 unlock 重跑。

## 错误处理

| 错误 | 行为 |
|---|---|
| Phase 3 未锁 | 报 `ERR_PHASE_LOCKED_BY_UPSTREAM` |
| Phase 4 是 `[x]` | 报"已锁,需先 unlock" |
| AC 未覆盖 | critic CRITICAL,贴未覆盖的 AC 编号清单 |
| 反向需求命中 | critic CRITICAL,贴命中的代码片段 |
| 接口不一致 | critic CRITICAL,贴 03b 写的 vs 代码实际的 path |
| docker compose 起不来 | critic CRITICAL,贴启动日志 |

## 不要做的

- 不擅自加 03b 没写的接口(那是范围蔓延,必须先回 Phase 3 unlock)
- 不擅自用 03c 没写的表
- 不绕过 e2e 直接锁(AC 覆盖率是这一 phase 的核心价值)
- 不在 Phase 4 改 Phase 0 的技术栈(改 → 必须先 unlock Phase 0)

## 与 superpowers 集成(可选)

Phase 4 skill 可调用 superpowers:subagent-driven-development 派发 TDD 实现子任务(每个接口一个子 agent),本期不强制。
