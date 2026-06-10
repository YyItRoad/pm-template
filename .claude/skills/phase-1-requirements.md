---
name: phase-1-requirements
description: 拉 docs/process/templates/01_requirements.md 模板,引导用户写用户故事/AC/边界/反向需求,跑 DoD + critic,sign-off 后调 update_state 锁 [x] Phase 1。
---

# /phase-1-requirements — 需求 ★

## 用途

引导用户写 `docs/01_requirements.md`,把项目章程(Phase 0)拆成可验收的用户故事 + AC + 边界 + 反向需求。

**写 STATE.md**:Phase 1 → `[x]`(需 DoD 全过 + critic 无 CRITICAL/HIGH + 用户明示锁)

## 触发

```
/phase-1-requirements
```

前置:
- Phase 0 ∈ `[x]`(否则报"上游未锁")
- Phase 1 状态 ∈ `{[ ], [~], [UNLOCKED]}`

## 执行步骤

### 1. 启动检查

**a) 上游检查**:
```bash
python3 -c "import sys; sys.path.insert(0, 'scripts'); from update_state import find_state_file, parse_state, get_current_status; sp = find_state_file(); st = parse_state(sp); print(f'Phase 0: {get_current_status(st[0])}')"
```

Phase 0 不是 `[x]` → 报"`ERR_PHASE_LOCKED_BY_UPSTREAM`:Phase 0 未锁,先跑 /phase-0-charter"。

**b) 本 phase 状态**:
- Phase 1 是 `[x]` → 报"已锁,需先 /state --audit --unlock 解锁"
- Phase 1 是 `[x] LEGACY` → 报"历史包袱,不可改"

**c) 版本对齐**:同 Phase 0,对比 `template_sha` vs pm-template HEAD。

### 2. 标记 in-progress(可选)

```bash
python3 scripts/update_state.py --phase 1 --status "[~]"
```

### 3. 拉模板 + 引导填空

读 `docs/process/templates/01_requirements.md`,核心段:

| 段 | 必填项 |
|---|---|
| §1 需求总览 | 一段话讲清"做什么 / 给谁用" |
| §2 用户故事 | 每条故事:`作为 <角色>,我想 <动作>,以便 <价值>` + AC 编号(AC-001, AC-002 ...) |
| §3 验收标准 | 每个 AC 编号的 Given-When-Then 描述,**必须可"是/否"判定** |
| §4 业务边界 | 列表格(范围 / 在内 / 不在内),把"什么是范围"讲清 |
| §5 反向需求 | "明确不做的事"(对应 Phase 0 §2.2,但更细)+ critic 用来 grep 范围蔓延 |
| §6 非功能需求 | 性能 / 容量 / 安全 / 可用性(按需) |
| §7 决策记录 | 实现 / 部署相关的决定,后续 phase 回写 |

**关键提示**:
- §2 AC 编号必须全局唯一且稳定(后续 Phase 4 critic 用 AC 覆盖率验证)
- §5 反向需求越具体越好(不能光说"不做 X",要说"不做 X 的 Y 变种")
- §3 验收标准必须是 Given-When-Then 三段,不能写"系统应该 X"

### 4. 写产物

写到 `docs/01_requirements.md`(项目根,不是 docs/process/templates/)。

### 5. 跑 DoD

```bash
/dod-check 1
```

通过率 < 100% → 停下等补。

### 6. 跑 critic

```bash
/critic 1
```

CRITICAL > 0 或 HIGH > 0 → 停下等改。

**Phase 1 critic 重点**(详 `docs/process/critics/01_requirements.md`):
- AC 编号是否每个故事都有
- 边界和反向需求是否互斥(不能"在内"又说"不在内")
- 决策记录是否有"理由 + 备选 + 决定"三段

### 7. Sign-off 提示

同 Phase 0 §3.2 格式。

### 8. 锁

```bash
python3 scripts/update_state.py \
  --phase 1 \
  --status "[x]" \
  --signed-by "<name>" \
  --signed-at "<YYYY-MM-DD>" \
  --critic-report-path "docs/process/critics/reports/01_requirements_<YYYY-MM-DD>.md" \
  --dod-count "<M>/<M>" \
  --template-sha "<pm-template HEAD SHA>"
```

### 9. 提示下一步

> Phase 1 已锁(签字:<name> <YYYY-MM-DD>)。
> 下一步:运行 `/phase-2-design` 写概要设计。

## 错误处理

| 错误 | 行为 |
|---|---|
| Phase 0 未锁 | 报 `ERR_PHASE_LOCKED_BY_UPSTREAM`,提示先跑 Phase 0 |
| Phase 1 是 `[x]` | 报"已锁,需先 unlock" |
| AC 编号缺 | DoD 拦截,提示"§2 每条故事必须有 AC 编号" |
| 反向需求空话 | critic HIGH,提示"§5 反向需求要写'不做 X 的 Y 变种'" |

## 不要做的

- 不替用户写 AC(需求 = 合同,用户必须明示)
- 不绕过反向需求(防范围蔓延是 Phase 1 的核心价值)
- 不写 §6 决策记录时只写"决定"不写"理由 + 备选"
