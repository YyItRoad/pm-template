---
name: decision
description: 创建 ADR(架构决策记录)写 docs/decisions/NNNN-<title>.md。决策贯穿项目全程,与一次性 change 区别开。轻量级,1 人签字,无 critic 强制(可选用)。状态机:proposed/accepted/deprecated/superseded。
---

# /decision <title> — 写架构决策记录(ADR)

## 用途

记录**重大技术决策**("为什么用 X 库" / "为什么合并到 user 表" / "为什么走 JWT cookie 而非 OAuth")。
决策**贯穿项目全程**,不像 change 是一次性事件。

**位置**:`docs/decisions/NNNN-<short-title>.md`(NNNN 4 位 0 补)
**模板**:`docs/process/templates/decision.md`

**写 STATE.md**:决策日志段加一行(状态:proposed → accepted)。

## 触发

```bash
/decision 用 FastAPI 而非 Django                    # 创建 ADR
/decision --list                                    # 列所有 ADR
/decision --status NNNN                             # 看具体 ADR 状态
/decision --supersede <old_NNNN> <title>            # 新 ADR 替代旧的
/decision --deprecate <NNNN>                        # 标废弃(不替代)
```

## 状态机

```
proposed → accepted → deprecated
              ↓
           superseded (被新 ADR 替代)
```

| 状态 | 谁能改 | 含义 |
|---|---|---|
| `proposed` | 起草人 | 起草中,未定 |
| `accepted` | 起草人 / reviewer | 已被项目接受 |
| `deprecated` | 任何人 | 弃用(不再用,但没替代品) |
| `superseded` | 任何人 | 被 #NNNN 替代(必填关联号) |

## 执行步骤

### 1. 拉模板 + 分配决策号

```bash
# 找下一个 NNNN
NEXT=$(ls docs/decisions/ 2>/dev/null | grep -oE '^[0-9]+' | sort -n | tail -1)
NEXT=$((NEXT + 1))
NEXT=$(printf "%04d" $NEXT)
FILE="docs/decisions/${NEXT}-${slug}.md"
mkdir -p docs/decisions/
cp docs/process/templates/decision.md "$FILE"
```

### 2. 引导填 spec

按模板段填,关键必填段(对应 DCR-NN 编号,见 `docs/process/dod/change/decision.md`):
- DCR-01 §1 元信息(决策号 / 加于日期 / 起草人 / 关联变更 / 关联 5 phase 段)
- DCR-02 §2 上下文(问题背景 + 约束 + 影响范围)
- DCR-03 §3 候选方案 ≥2 个(表 4 列:方案 / 优点 / 缺点 / 成本)
- DCR-04 §4 决策(选择哪个 + 1-3 句理由)
- DCR-05 §5 后果(正面 + 负面 + 风险缓解,**负面不可省**)
- DCR-06 §6 替代方案可逆性(改其他方案成本 / 是否需要 deprecation change)
- DCR-07 §7 签字(1 人 + 状态:proposed → accepted)

**关键提示**:
- §3 候选方案**必 ≥2 个**,1 个 = critic CRITICAL
- §5 负面后果**必填**,光写"性能更好"不可验证 = MEDIUM
- §7 必填"候选 ≥2" / "选了哪个写清" / "负面后果不是空话" / "签字" 4 个 checkbox

### 3. 跑 critic(轻量)

```bash
/critic change/decision     # 详见 critics/change/decision.md(7 项)
```

CRITICAL > 0 → 停下等改。**注意:decision 没强制 critic,可跳过**(轻量级)。

### 4. Sign-off

```
> ADR #0001-decide-fastapi 待锁。
> 候选方案: 2 个 (FastAPI / Django) ✓
> 决策: FastAPI
> 后果负面: 必填
> 签字: <name> (YYYY-MM-DD)
> 状态: proposed → accepted
> 请确认锁:[y / n / c]
```

`y` → 写 STATE.md "决策日志" 段:
```
| 0001 | decide-fastapi | accepted | 2026-06-10 | Alice |  |
```

### 5. supersede(替代)流程

```bash
/decision --supersede 0001 "用 FastAPI 改 NestJS 重构"
```

- 自动创建 #0002 决策(状态:proposed)
- 在 #0001 末尾追加:状态变更 `accepted → superseded by #0002 (签字: <name> YYYY-MM-DD)`
- 在 #0002 元信息 "关联决策" 字段填:`supersedes #0001`

> 完整 supersede 流程、与其他 skill 的关系、跨切面详见 spec §4.6。

## 错误处理

| 错误 | 行为 |
|---|---|
| 候选方案 < 2 | critic CRITICAL,补 |
| 负面后果空话("性能更好") | critic MEDIUM,补具体指标 |
| 缺 `docs/decisions/` 目录 | 自动 mkdir -p |
| NNNN 冲突 | 自动 +1,审稿人复查 |

## 不要做的

- 不写"显然选 X" — §3 必给 ≥2 候选 + 真实对比
- 不写"无负面" — 决策必有 trade-off,光写好话 = 失信
- 不在 ADR 里写代码 / 改代码 — ADR 是"为什么",不是"怎么做"
- 不把 ADR 当 spec 用 — spec 是 `docs/02_high_level_design.md` 段,ADR 是元层决策
- 不在 proposed 状态就改 STATE.md 标 accepted — 签字后才标
