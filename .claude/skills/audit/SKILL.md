---
name: audit
description: 对已实现功能做 5 项机械审查(AC 覆盖 / 范围蔓延 / 反向需求 / 接口一致 / 单测覆盖),出报告存 docs/process/audit/reports/。用于"代码已写完,需要系统化查一遍有没有坑"。不写 STATE.md(只读,产报告)。
---

# /audit — 已实现功能审查

## 用途

对**已写完的代码**做系统化机械审查 — 不改代码,只查 5 项最常见的"实现漂移"问题:

1. **AC 覆盖率** — Phase 1 写了的验收标准,代码里有没有 e2e case 覆盖
2. **范围蔓延** — 写了但 Phase 3b 没记的接口(可能 admin 私活)
3. **反向需求真没做** — Phase 1 §5 说"不做"的事,代码里有没有偷偷做了
4. **接口一致性** — 03b path/method 写的与代码 `@router` 装饰器 100% 一致
5. **单测覆盖** — 每个接口都有至少 1 个 test case

**不写 STATE.md**。只产报告存 `docs/process/audit/reports/audit_<DATE>.md`。

## 何时用

- **刚完成 1 个大 feature** — 想知道代码与设计有多对齐
- **接手别人写的模块** — 找潜在 bug / 偏离
- **release 前** — 最后一遍扫(配合 `/release`)
- **代码 review 前** — 自审一遍,省 reviewer 时间

**不替代**:`/critic 4` 在 phase 4 末跑,产物上下文完整。`/audit` 是事后回头看,可单独跑、无产物上下文要求。

## 触发

```bash
/audit                  # 跑全 5 项
/audit --ac-only        # 只 AC 覆盖率
/audit --scope-creep    # 只范围蔓延
/audit --reverse-req    # 只反向需求
/audit --interface      # 只接口一致性
/audit --test-coverage  # 只单测覆盖
/audit --check          # 只跑不写报告(返回 exit code,可作 CI gate)
/audit --report-path X  # 写自定义报告路径
```

## 5 项检查标准(从 critic/04_implementation.md 提炼)

| 项 | 等级 | 含义 |
|---|---|---|
| AC 覆盖率 | **CRITICAL** | 提取 01 的 `AC-NNN` 编号 → grep `tests/` + `scripts/e2e_*.sh` → 缺则 CRITICAL |
| 范围蔓延 | **CRITICAL** | 提取 `app/src/backend/` 的 `@router.get/post` → 与 03b 求差集 → code 有 / 03b 无 = CRITICAL |
| 反向需求真没做 | **CRITICAL** | 提取 01 §5 的关键词("❌ 不做 X") → grep `app/src/` → 命中则 CRITICAL |
| 接口一致性 | **HIGH** | 03b 写了但代码无(漏实现) |
| 单测覆盖 | **MEDIUM** | 03b 接口在 tests/ 没出现(漏测试) |

**整体等级** = 5 项中最高(CRITICAL > HIGH > MEDIUM > PASS)。

## 执行步骤

### 1. 读产物

```bash
# 必读
docs/01_requirements.md          # AC 编号 + §5 反向需求
docs/03b_api_design.md           # 接口清单
```

缺失产物 → 报 `ERR_PHASE_MISSING`,提示先跑对应 phase。

### 2. 跑 5 项检查(全 grep/diff,无 LLM)

调用 `.claude/scripts/audit.py`:

```python
from audit import run_audit, render_report
import update_state  # noqa: F401  # 复用 find_state_file

audit = run_audit()  # 或 run_audit(["ac-coverage", "scope-creep", ...])
report = render_report(audit)
```

实际 CLI:
```bash
python3 .claude/scripts/audit.py
```

### 3. 写报告

**路径**:`docs/process/audit/reports/audit_<YYYY-MM-DD>.md`

报告格式:
```markdown
# Audit Report — 2026-06-12

**Overall**: CRITICAL
**检查项**:
- AC 覆盖率(ac-coverage): `CRITICAL`
- 范围蔓延(scope-creep): `PASS`
- 反向需求真没做(reverse-req): `PASS`
- 接口一致性(interface): `HIGH`
- 单测覆盖(test-coverage): `MEDIUM`

## AC 覆盖率 — `CRITICAL`
- AC 总数: 23
- 覆盖: 20
- **未覆盖 AC**:
  - AC-15
  - AC-18
  - AC-22

## 范围蔓延 — `PASS`
- 代码 routes: 18
- 03b 定义: 18

...

## 接口一致性 — `HIGH`
- 03b 定义: 18
- 代码已实现: 16
- **03b 写了但代码无**:
  - `GET /api/v1/expenses/{id}`
  - `POST /api/v1/expenses/{id}/approve`
```

### 4. 提示用户

```
> /audit 完成,overall: CRITICAL
> 报告: docs/process/audit/reports/audit_2026-06-12.md
>
> CRITICAL 项:1(AC 覆盖率 — 3 个 AC 缺 e2e)
> HIGH 项:1(接口一致性 — 2 个 03b 接口没代码实现)
> MEDIUM 项:1(单测覆盖 — 1 个接口无单测)
>
> 建议:
>   1. CRITICAL 必修(否则 release 不能锁)
>   2. HIGH 应修
>   3. MEDIUM 可后续
>
> 出口:
>   - 修了 → 跑 /audit --ac-only 复检
>   - 不修 → 在 audit 报告里加"已知问题,后续修"段,降级
```

## 与其他 skill 的区别(精简,详情见 spec)

`/audit` 不同于其他 4 个相关入口:

| Skill | 区别 |
|---|---|
| `/critic 4` | phase 4 **末**跑,产物上下文完整;`/audit` 事后回头看 |
| `/change refactor` | 改代码,带 critic 检 spec;`/audit` 不改 |
| `/change bugfix` | 修**已知** bug;`/audit` 主动**找** bug |
| `superpowers:code-review` | 通用 code review(外部);`/audit` 机械 grep + pm-template 集成 |

`/audit` 是**"review-only"** 入口,无对应 change spec 也不需 /unlock。

## 错误处理

| 错误 | 行为 |
|---|---|
| 缺 01_requirements.md | 报 `ERR_PHASE_MISSING`,提示先跑 phase 1 |
| 缺 03b_api_design.md | 报 `ERR_PHASE_MISSING`,提示先跑 phase 3b |
| 5 项中任何 CRITICAL/HIGH | 报告写,exit code 1(可作 CI gate) |
| 全 PASS | 报告写,exit code 0 |
| `--check` 模式 | 不写报告,只返 exit code |

## CI Gate 用法

```yaml
# .github/workflows/audit.yml
- name: Audit
  run: python3 .claude/scripts/audit.py --check
  # exit 0 = PASS,exit 1 = 有 CRITICAL/HIGH
```

## 不要做的

- **不修复** — 报告里给定位和建议,但代码修复是 `/change bugfix` 的事
- **不替用户决定严重度** — critic/04 怎么说就怎么标
- **不在产物缺时硬跑** — 缺 01/03b 必报错,不"猜"
- **不写 LLM-judge 风格的审查** — 5 项全机械 grep/diff,主观判断是 `/change refactor` 的事
- **不进 phase 状态机** — `/audit` 是只读审查,无 [x]/[~] 状态
