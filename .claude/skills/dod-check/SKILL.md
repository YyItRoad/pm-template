---
name: dod-check
description: 单跑 pm-template 的 DoD 勾选,对指定 phase 产物逐条检查 Definition of Done,输出通过/缺失清单。
---

# /dod-check <phase> — 单跑 DoD 勾选

## 用途

按 `docs/process/dod/0X_*.md` 模板,对指定 phase 产物逐条勾 Definition of Done,输出"`N/M` 通过 + 缺啥"。

**不写 STATE.md**。只产清单(可选存档)。

## 触发

```
/dod-check 0    # 勾 Phase 0 charter
/dod-check 1    # 勾 Phase 1 requirements
/dod-check 2    # 勾 Phase 2 high-level design
/dod-check 3    # 勾 Phase 3 detailed design(覆盖 3a/3b/3c)
/dod-check 4    # 勾 Phase 4 implementation
```

## 执行步骤

### 1. 取 DoD 模板

按 phase 取 `docs/process/dod/<phase>_*.md`:

| 输入 | 模板路径 |
|---|---|
| `0` | `docs/process/dod/00_charter.md` |
| `1` | `docs/process/dod/01_requirements.md` |
| `2` | `docs/process/dod/02_high_level_design.md` |
| `3` | `docs/process/dod/03_detailed_design.md` |
| `4` | `docs/process/dod/04_implementation.md` |

缺失时:
- 项目本地无 → 报 `ERR_MISSING_TEMPLATE`
- 尝试从 GitHub raw 拉(URL 模板见 spec §5)
- 离线 → 提示"手动 git submodule add pm-template 补齐"

### 2. 解析 DoD 项

读 DoD 模板,提取每条勾选项(如 `- [ ] DoD-01: ...`)。

### 3. 逐条检查

**两种检查方式**(由 DoD 项描述决定):

**(a) 机械存在性** — 文件 / 段 / 行存不存在:
```bash
test -f docs/00_charter.md && echo OK
grep -q "## 1. 基础信息" docs/00_charter.md && echo OK
```

**(b) 内容判定** — 字段非空 / 勾选了 / 签字了:
- 用 Read tool 读对应段,人工判定
- 报告里写明判定依据

**绝不放水**:如果项目该字段为空,标"未通过",不写"近似通过"。

### 4. 输出清单

```
=== Phase 0 charter DoD 勾选 ===

  ✓ DoD-01: docs/00_charter.md §1 项目名非空
  ✓ DoD-02: §1 一句话描述非空
  ✓ DoD-03: §1 适用场景 ≥ 3 条
  ✗ DoD-04: §2.1 核心目标 ≥ 3 条(当前 2 条)
  ✓ DoD-05: §2.2 明确不做的事 ≥ 3 条
  ✓ DoD-06: §2.5 技术栈勾选 L1+L2
  ✗ DoD-07: §2.5 签字行未填
  ✓ DoD-08: §3 角色清单 ≥ 1 行
  ...

通过率: 11/13(84.6%)

❌ 缺 2 条,phase 0 不可锁:
  - DoD-04
  - DoD-07
```

### 5. 返回信号

**给调用方(`/phase-N-XXX` 或 `/new-project`)**:
- `通过率 < 100%` → 提示"缺 N 条,不可锁"
- `通过率 = 100%` → 提示"DoD 全过,可锁 + 跑 critic"

## 自我约束

- DoD 是"机械合规检查",**不查内容质量**(内容质量归 critic 管)
- 不替用户判断"差不多就行",缺一条报一条
- 不改产物文件
- 报告不强制写文件(用户要的话写 `docs/process/dod/reports/`,目录不存在则 mkdir)

## 不要做的

- 不调用 `update_state()` 写 STATE.md
- 不跑 critic 自审(那是 `/critic` 的事)
- 不改产物文件
