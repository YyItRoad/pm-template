---
name: unlock
description: 解锁一个已锁 [x] phase 以便修改产物。cascade 自动解锁下游 phase,提示需逐个重跑 critic + 签字。/state 只读不写,本 skill 是改产物的实际入口。
---

# /unlock <phase> — 解锁已锁 phase

## 用途

解锁一个 `[x]` phase,转 `[UNLOCKED]`,**cascade 自动解锁下游 phase**(N+1..4)。

**写 STATE.md**:phase → `[UNLOCKED]`(走 `update_state.py` CLI)

## 触发

```
/unlock 0          # 解锁 Phase 0
/unlock 2          # 解锁 Phase 2
/unlock --all      # 列出所有 [x] phase,逐个问是否解锁
/unlock --dry      # 只看 cascade 影响,不真解锁
```

## 执行步骤

### 1. 启动检查

**a) 找 STATE.md + 解析**:
```bash
python3 -c "
import sys
sys.path.insert(0, '.claude/scripts')
from update_state import find_state_file, parse_state, get_current_status
sp = find_state_file()
st = parse_state(sp)
for i in range(5):
    print(f'Phase {i}: {get_current_status(st[i])}')
"
```

**b) 检查目标 phase 状态**:
- `[x]` → 正常解锁,继续
- `[x] LEGACY` → 报"终态,不可解锁(用 migrate_legacy_state.py 才可改)",exit
- `[UNLOCKED]` → 提示"已解锁,无需重复",exit
- `[ ]` / `[~]` → 提示"未锁,无需 unlock;如要标进行中,跑 /phase-N-XXX",exit
- `[SKIP]` → 提示"已 SKIP,无需 unlock",exit

### 2. 展示 cascade 影响

读 STATE.md,显示目标 phase **之后**的所有 phase 状态(spec §3.4):

```
> 目标: Phase 0(当前 [x],签字:Alice 2026-06-10)
>
> Cascade 影响: 解锁 Phase 0 → 自动解锁下游 phase
>
> 下游状态:
>   Phase 1: [x] by Bob 2026-06-10  ← 将被 cascade 解锁
>   Phase 2: [x] by Carol 2026-06-10  ← 将被 cascade 解锁
>   Phase 3: [x] by Dave 2026-06-10  ← 将被 cascade 解锁
>   Phase 4: [x] by Eve 2026-06-10  ← 将被 cascade 解锁
>
> 解锁后需逐 phase 重跑:critic + DoD + sign-off(详 spec §3.4)
```

**注意**:cascade 只解 `[x]` / `[UNLOCKED]`,不触碰 `[ ]` / `[~]` / `[SKIP]`(update_state.py 实现)。

如果是 `--dry`,到此 exit(不调 update_state)。

### 3. 收集 unlock_reason

```
> 请输入 unlock 原因(自由文本,会写入 STATE.md 永久留痕):
>   例:"docs/00_charter.md 项目名拼错"
>   例:"Phase 2 接口清单要加端点"
>   例:"pm-template 升 v1.1,template_sha 过期,需重跑"
```

非空,长度 ≤ 200 字符。

### 4. 二次确认(y/n)

```
> 确认解锁 Phase 0 + cascade Phase 1/2/3/4?
>   原因:<reason>
>   [y] 确认
>   [n] 取消
```

**用户输入 `n`** → exit,STATE.md 不动。

### 5. 调 update_state

```bash
python3 .claude/scripts/update_state.py \
  --phase 0 \
  --status "[UNLOCKED]" \
  --lock-reason "<reason>"
```

输出 `✓ update_state(phase=0, status='[UNLOCKED]') 成功` + diff。

**`update_state.py` 内部 cascade**:自动把 N+1..4 标 `[UNLOCKED]` + `lock_reason="upstream re-opened"`(已实现,详 spec §3.4)。

### 6. 打印 diff

把 update_state 输出的 diff 完整展示,让用户看到 STATE.md 的变化。

### 7. 提示下一步

```
> ✓ Phase 0 已解锁(原因:<reason>)
> ✓ Cascade:Phase 1/2/3/4 同步解锁
>
> 下一步:
>   1. 编辑 Phase 0 产物(对应 artifact 路径见 STATE.md 段)
>   2. /critic 0            (重跑自审)
>   3. /dod-check 0
>   4. /phase-0-charter     (sign-off 重锁回 [x])
>   5. Phase 1/2/3/4 同样循环(每个 critic + DoD + sign-off + 锁)
>   6. /state               (看最终进度)
```

## `--all` 模式

```
> 扫描 [x] phase...
> 找到 N 个:Phase 0 [x]、Phase 2 [x]、Phase 4 [x]
>
> 批量解锁?(输入 y/n,**谨慎**,所有 [x] phase 都会 cascade 解锁)
>   [y] 批量解锁(共用同一 reason)
>   [n] 取消
```

如果 `[x]` phase 不连续(比如 0 和 2 都 [x],1 是 [~]),cascade 仍按各自下游扩散。

## `--dry` 模式

只跑 §1 + §2(显示当前状态 + cascade 影响),不收集 reason,不调 update_state。

适合"我先看看 unlock 会影响啥"。

## 错误处理

| 错误 | 行为 |
|---|---|
| `[x] LEGACY` | 报"终态,不可解锁(只有 migrate_legacy_state.py 可写 LEGACY)" |
| `[UNLOCKED]` | 提示"已解锁,无需重复" |
| `[ ]` / `[~]` | 提示"未锁,无需 unlock;如要标进行中,跑 /phase-N-XXX" |
| `[SKIP]` | 提示"已 SKIP,无需 unlock" |
| Phase 越界(>4) | 报错"phase 只能是 0/1/2/3/4" |
| 缺 STATE.md | 报"未初始化,先跑 /new-project" |
| `ERR_INVALID_TRANSITION` | 状态机拒绝(由 update_state.py 抛),透传错误码 |
| 用户 n 取消 | exit,STATE.md 不动 |

## 不要做的

- 不替用户填 unlock_reason(改什么必须明示,留痕用)
- 不批量 unlock 不二次确认
- 不在 unlock 后自动跑 critic(留给用户)
- 不修改产物文件(unlock 只改 STATE.md 状态,改 docs/0X_*.md 是用户的活)
- 不在 /unlock 内部跑 phase skill(unlock 和 phase skill 是解耦的)
- 不自动重锁任何 phase(包括被 unlock 的那个)

## 与 `/state --audit` 配合

典型工作流:
```
1. /state --audit              # 看哪些 phase template_sha 过期
2. /unlock 2 --dry             # 看 unlock Phase 2 的 cascade 影响
3. /unlock 2                   # 确认解锁
4. 编辑 docs/02_high_level_design.md
5. /critic 2; /dod-check 2; /phase-2-design  # 重跑 + 重锁
6. Phase 3/4 同样(已被 cascade 解锁)
```

`/state --audit` 是"看"(`/unlock --dry` 也是"看");`/unlock` 是"动"。两者职责分清。
