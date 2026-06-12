---
name: phase-1-requirements
description: 先做挖掘回合(角色×场景矩阵/20 边界/10 异常/10 反向,输出到 §0),再拉模板填 §1-§6,跑 DoD + critic,sign-off 后调 update_state 锁 [x] Phase 1。
---

# /phase-1-requirements — 需求 ★

## 用途

引导用户写 `docs/01_requirements.md`,把项目章程(Phase 0)拆成可验收的用户故事 + AC + 边界 + 反向需求。

**关键创新:挖掘回合(强制)** —— 在填模板前,先做 4 轮结构化穷举(角色×场景矩阵 / 边界场景 / 异常路径 / 反向需求)。**挖掘回合不可跳过**,跳过 = critic CRITICAL,拒绝锁。**挖掘回合的产物是 phase 2 启动时的硬 grep 目标**(改动 5),挖不够 = phase 2 拒绝启动。

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
python3 -c "import sys; sys.path.insert(0, '.claude/skills/_lib'); from update_state import find_state_file, parse_state, get_current_status; sp = find_state_file(); st = parse_state(sp); print(f'Phase 0: {get_current_status(st[0])}')"
```

Phase 0 不是 `[x]` → 报"`ERR_PHASE_LOCKED_BY_UPSTREAM`:Phase 0 未锁,先跑 /phase-0-charter"。

**b) 本 phase 状态**:
- Phase 1 是 `[x]` → 报"已锁,需先 /state --audit --unlock 解锁"
- Phase 1 是 `[x] LEGACY` → 报"历史包袱,不可改"

**c) 版本对齐**:同 Phase 0,对比 `template_sha` vs pm-template HEAD。

### 2. 标记 in-progress(可选)

```bash
python3 .claude/skills/_lib/update_state.py --phase 1 --status "[~]"
```

### 3. 挖掘回合(强制,不可跳过 ★新加)

**为什么**:Phase 1 的输出是 phase 2+ 的"合同",合同不细 = 设计阶段无穷返工。挖掘回合是"细"。

**做法**:4 轮,每轮一轮穷举,写到 `docs/01_requirements.md` 的 `§0 挖掘证据` 段(模板已预留,带 anchor 注释)。

#### 3.1 角色×场景 矩阵

输入:从 phase 0 §0.1 利益相关方 + §1 角色清单提炼出"系统内角色"。

横轴:典型场景(用户生命周期:注册 / 首次使用 / 日常使用 / 异常 / 退出)
纵轴:角色(从 phase 0 继承)

每格:这个角色在这个场景下会做什么?(≤1 句话,只列,不要写 AC —— 详细 AC 写到 §2)

#### 3.2 边界场景穷举(≥20 条)

提问引导:
- **正常边界**:操作成功路径的"边界值"(金额=0 / 金额=最大 / 时间=凌晨跨天)
- **输入边界**:用户输入的极端值(超长字符串 / 特殊字符 / emoji / 空字符串)
- **时间边界**:重复触发(幂等)/ 过期操作 / 跨时区
- **状态边界**:已删除数据访问 / 已禁用账号 / 已结案工单

每条 ≤1 句话,只列场景,不写期望行为(详细期望写到 §3 边界场景与异常)。

#### 3.3 异常路径穷举(≥10 条,4 类各 ≥1)

- **鉴权失败**:未登录 / 已过期 / 无权限 / 跨租户访问
- **字段缺失**:必填字段空 / 字段类型错 / 字段超长
- **状态非法**:已删除数据操作 / 状态机非法转移
- **并发**:同操作并发触发 / 读已写读

每条填:异常类型 / 触发条件 / 期望响应 / HTTP 码。

#### 3.4 反向需求穷举(≥10 条,★phase 4 critic 用来反作弊)

提问引导:
- **AI 容易偷偷加的**:登录用手机号 / 验证码 / 找回密码 / 第三方登录 → 这些**我们不**做吗?
- **范围蔓延诱因**:分享 / 邀请 / 推荐 / 评论 / 点赞 → 这些**我们不**做吗?
- **优化诱因**:缓存 / 队列 / 搜索 / 排序 → 这些**我们不**做吗?

每条填:系统不应做 / 常见诱因(AI 容易偷偷加的)/ 我们怎么挡住(机制:没接口 / 没字段 / 有校验)。

#### 3.5 自检(挖掘回合结束的关口)

- 4 个 anchor 必在产物里:grep `<!-- ANCHOR: role-scenario -->` / `<!-- ANCHOR: edge-scenarios -->` / `<!-- ANCHOR: exception-paths -->` / `<!-- ANCHOR: reverse-requirements -->`
- 行数达标:边界 ≥20 / 异常 ≥10 / 反向 ≥10
- 任意不达标 → `ERR_INSUFFICIENT_EXPLORATION`,**回 §3 重挖**

### 4. 拉模板 + 引导填空

读 `docs/process/templates/01_requirements.md`,核心段(§0 已在 §3 填好):

| 段 | 必填项 |
|---|---|
| §1 角色清单 | 从 charter §0.1 利益相关方 + §3 角色清单继承,允许细化 |
| §2 用户故事 | 每条故事:`作为 <角色>,我想 <动作>,以便 <价值>` + AC 编号(AC-001, AC-002 ...) |
| §3 边界场景与异常 | 把 §0.2 + §0.3 展开成"场景-期望-不允许"三栏 |
| §4 非功能需求 | 性能 / 容量 / 安全 / 可用性(按需) |
| §5 反向需求 | 把 §0.4 展开成"系统不应做 + 原因" |
| §6 决策记录 | 实现 / 部署相关的决定,后续 phase 回写 |

**关键提示**:
- §0 已在 §3 挖掘回合填好,本节专注 §1-§6
- §2 AC 编号必须全局唯一且稳定(后续 Phase 4 critic 用 AC 覆盖率验证)
- §5 反向需求越具体越好(不能光说"不做 X",要说"不做 X 的 Y 变种")
- §3 验收标准必须是 Given-When-Then 三段,不能写"系统应该 X"

### 5. 写产物

写到 `docs/01_requirements.md`(项目根,不是 docs/process/templates/)。

### 6. 跑 DoD

```bash
/dod-check 1
```

通过率 < 100% → 停下等补。

### 7. 跑 critic

```bash
/critic 1
```

CRITICAL > 0 或 HIGH > 0 → 停下等改。

**Phase 1 critic 重点**(详 `docs/process/critics/01_requirements.md`):
- §0 挖掘证据完整性(机械 grep,★最关键):4 anchor + 行数 20/10/10
- AC 编号是否每个故事都有
- 边界和反向需求是否互斥(不能"在内"又说"不在内")
- 决策记录是否有"理由 + 备选 + 决定"三段

### 8. Sign-off 提示

同 Phase 0 §9 格式。

```
> Phase 1 待锁。
> 产物: docs/01_requirements.md (<N> 行)
> §0 挖掘证据: role-scenario matrix / edge-scenarios / exception-paths / reverse-requirements = <a>/<b>/<c>/<d> 行
> critic 报告: docs/process/critics/reports/01_requirements_<YYYY-MM-DD>.md
>   CRITICAL: 0 / HIGH: 0 / MEDIUM: 0 / LOW: 0
> DoD 勾选: 15/15 ✓
>
> 请确认锁:
>   [y] 锁(签字: <name> <YYYY-MM-DD>)
>   [n] 不锁(返回修改)
>   [c] 只看 critic 报告
```

**用户输入 `n`** → 问"需修改什么?",回到 §4 重填(§0 不用重挖,除非 n 指明挖掘不够)。

### 9. 锁

```bash
python3 .claude/skills/_lib/update_state.py \
  --phase 1 \
  --status "[x]" \
  --signed-by "<name>" \
  --signed-at "<YYYY-MM-DD>" \
  --critic-report-path "docs/process/critics/reports/01_requirements_<YYYY-MM-DD>.md" \
  --dod-count "<M>/<M>" \
  --template-sha "<pm-template root HEAD SHA>"
```

### 10. 提示下一步

> Phase 1 已锁(签字:<name> <YYYY-MM-DD>)。
> 下一步:运行 `/phase-2-design` 写概要设计。

## 错误处理

| 错误 | 行为 |
|---|---|
| `ERR_INSUFFICIENT_EXPLORATION` | 挖掘证据不全(anchor 缺/行数不够),拒绝进 §4,**回 §3 重挖** |
| Phase 0 未锁 | 报 `ERR_PHASE_LOCKED_BY_UPSTREAM`,提示先跑 Phase 0 |
| Phase 1 是 `[x]` | 报"已锁,需先 unlock" |
| AC 编号缺 | DoD 拦截,提示"§2 每条故事必须有 AC 编号" |
| 反向需求空话 | critic HIGH,提示"§5 反向需求要写'不做 X 的 Y 变种'" |

## 不要做的

- **不跳过 §3 挖掘回合** —— 模板里有 §0 必须填,空 = critic CRITICAL
- **不绕过 §3.5 自检** —— 4 个 anchor 缺一就 ERR_INSUFFICIENT_EXPLORATION
- 不替用户写 AC(需求 = 合同,用户必须明示)
- 不绕过反向需求(防范围蔓延是 Phase 1 的核心价值)
- 不写 §6 决策记录时只写"决定"不写"理由 + 备选"
- 不在挖掘回合中"凭空白想"摘要,内容必须从 §1-§6 提炼(防止 LLM 自由发挥)
