---
name: state
description: 读取并渲染 docs/STATE.md,显示当前 5 phase 进度,支持 --audit 模式扫描 template_sha 过期。
---

# /state — 流程状态查看

## 用途

读 `<cwd>/docs/STATE.md`,把 5 phase 当前状态 + 上次签字 + template_sha 渲染出来,提示下一步。

**不写 STATE.md**。只读。

## 触发

```
/state           # 渲染当前进度
/state --audit   # 扫描所有 phase template_sha,列出过期 phase
```

## 执行步骤

### 1. 找 STATE.md

用 `python3 -c "import sys; sys.path.insert(0, '.claude/skills/_lib'); from update_state import find_state_file; print(find_state_file())"` 拿到绝对路径。

如果 `find_state_file` 抛 `StateFileCorruptError`(文件不存在):
- 输出:`✗ 未找到 docs/STATE.md`
- 提示:`是否首次跑?运行 /new-project <topic> 初始化`
- exit(不报错,只是没东西可看)

### 2. 解析 + 渲染

```bash
python3 .claude/skills/_lib/update_state.py --check
```

它会输出:
```
STATE.md: <绝对路径>
  Phase 0: [ ]                                       (空)
  Phase 1: [x] by Alice on 2026-06-09
  Phase 2: [~]
  Phase 3: [UNLOCKED] (lock_reason: ...)
  Phase 4: [x] LEGACY
```

### 3. 加建议下一步

根据当前状态,生成自然语言建议:

| 当前情况 | 建议 |
|---|---|
| 全部 `[ ]` | "未开始,运行 `/new-project <topic>` 启动项目" |
| 首个非 `[x]` 是 Phase 0 | "Phase 0 立项待跑,运行 `/phase-0-charter`" |
| 首个非 `[x]` 是 Phase N(1≤N≤4) | "从 Phase {N} 续跑,运行 `/phase-{N}-...`" |
| 有 `[UNLOCKED]` | "⚠️ Phase {N} 已 cascade unlock,需重跑 critic + 签字(详 spec §3.4)" |
| 有 `[x] LEGACY` | "Phase {N} 为历史包袱,不可改" |
| 全部 `[x]` | "✅ 5 phase 全部锁定,进入实施支持模式" |
| 全部 `[x]` 但 Phase 0 有 SKIP | "Phase 0 已跳过,实施照常进行" |

### 4. `--audit` 模式(版本对齐扫描)

额外跑:
```bash
# 对比 STATE.md 记录的 template_sha vs pm-template git HEAD SHA
git -C <pm-template root> rev-parse HEAD
```

或当 pm-template 是子项目 `vendor/pm-template` 时:
```bash
git -C vendor/pm-template rev-parse HEAD
```

**判定规则**:
- 对每个 phase,从 STATE.md 提取 `template_sha`(锁时记录的)
- 如果 `template_sha` ≠ pm-template 当前 HEAD,标"过期"
- 输出表格:

```
Phase | 锁定时 SHA  | 当前 SHA   | 状态
0     | abc1234     | def5678    | ⚠️ 过期(需 unlock + 重跑 critic)
1     | def5678     | def5678    | ✅ 一致
...
```

如果任何 phase 过期,提示:
> "存在 N 个过期 phase,运行 `/state --audit --unlock` 一键 cascade unlock(谨慎,会重置下游)"
>
> 默认不自动 unlock,需用户明示。

## 输出格式

```
=== 流程状态 ===

STATE.md: /path/to/docs/STATE.md
template SHA: <当前 HEAD>(对比 STATE.md 记录的)

  Phase 0 立项      : [ ]            — 未开始
  Phase 1 需求★     : [x] by Alice 2026-06-09  — 已锁(SHA: abc1234)
  Phase 2 概要设计  : [~]            — 进行中
  Phase 3 详细设计  : [UNLOCKED]     — ⚠️ cascade unlock(下游待重跑)
  Phase 4 实现+验证 : [x]            — 已锁

下一步: 运行 `/phase-2-design` 续跑
```

## 不要做的

- 不调用 `update_state()` 写 STATE.md
- 不重写或修复 STATE.md(坏了交给用户)
- 不主动 unlock(即使 --audit 模式也只列出)
