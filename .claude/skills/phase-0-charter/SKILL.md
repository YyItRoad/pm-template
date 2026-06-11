---
name: phase-0-charter
description: 先做挖掘回合(10 利益相关方/10 约束/5 非目标 穷举,输出到 §0),再拉模板填 §1-§5,跑 DoD + critic,sign-off 后调 update_state 锁 [x] Phase 0。
---

# /phase-0-charter — 立项

## 用途

引导用户填项目章程 `docs/00_charter.md`,回答"为什么做 / 给谁用 / 边界在哪 / 不能做什么 / 锁哪条技术栈"。

**关键创新:挖掘回合(强制)** —— 在填模板前,先做 3 轮结构化穷举,把项目利益相关方/约束/非目标列清楚。**挖掘回合不可跳过**,跳过 = critic CRITICAL,拒绝锁。这是"把不确定性预算消化在 phase 0"的硬性环节。

**写 STATE.md**:Phase 0 → `[x]`(需 DoD 全过 + critic 无 CRITICAL/HIGH + 用户明示锁)

## 触发

```
/phase-0-charter
```

前置:Phase 0 状态 ∈ `{[ ], [~], [UNLOCKED]}`(不能是 `[x]` 或 `[x] LEGACY`)。

## 执行步骤

### 1. 启动检查(同 spec §6.3)

**a) 找 STATE.md**:
```bash
python3 -c "import sys; sys.path.insert(0, 'scripts'); from update_state import find_state_file, parse_state, get_current_status; sp = find_state_file(); st = parse_state(sp); print(f'Phase 0: {get_current_status(st[0])}')"
```

- 抛 `StateFileCorruptError` → 报"STATE.md 缺失或损坏,先跑 `/new-project <topic>` 初始化"
- Phase 0 状态是 `[x]` → 报"`Phase 0 已锁,需先 /state --audit --unlock(谨慎) 解锁`"
- Phase 0 状态是 `[x] LEGACY` → 报"`Phase 0 是历史包袱,不可改`"

**b) 版本对齐**:对比 `STATE.md` 记录的 Phase 0 `template_sha` vs pm-template git HEAD。

```bash
# 取 pm-template SHA(子项目用 vendor/pm-template,pm-template 自仓库用 .)
git -C . rev-parse HEAD 2>/dev/null || git -C vendor/pm-template rev-parse HEAD
```

如果 `template_sha` 已记录且与当前 SHA 不一致:
- 提示:`⚠️ pm-template 已升级(<old> → <new>),建议先 /state --audit 决定是否 unlock 重跑`

**c) 上游检查**:Phase 0 是第一 phase,无上游。

### 2. 标记 in-progress(可选)

如果 Phase 0 当前是 `[ ]`:
```bash
python3 .claude/scripts/update_state.py --phase 0 --status "[~]"
```

不阻塞主流程,只是把 STATE.md 留个"进行中"痕迹,防止 `Ctrl+C` 后看不出在干啥。

### 3. 挖掘回合(强制,不可跳过 ★新加)

**为什么**:LLM 擅长"穷举 + 模拟角色",把这种能力用在前面,后期设计就少返工。挖不够 = phase 1/2 必返工。挖够 = phase 2 启动时直接用 §0 摘要当合同。

**做法**:3 轮,每轮一轮穷举,写到 `docs/00_charter.md` 的 `§0 挖掘证据` 段(模板已预留,带 anchor 注释)。

#### 3.1 利益相关方穷举(≥10 条)

提问引导:
- 谁能**用**这个项目?
- 谁**出资**或决策?
- 谁能**否决**这个项目?
- 谁能**被影响**但**不直接用**?(运营、客服、法务、监管、上下游)
- 谁**未来可能用**?(考虑 1-2 年扩展)

每条填:利益相关方名 / 关注点 / 为什么关心。**禁空话**("用户"不算,要写"家长用户,关心零花钱额度安全")。

#### 3.2 约束穷举(≥10 条,每条量化或可证伪)

提问引导:
- **技术**:性能 QPS?响应延迟?支持的并发用户数?数据量级?
- **时间**:项目交付 deadline?每天可投入工时?关键里程碑日期?
- **法规**:涉及 PII?需要等保?GDPR/个人信息保护法?
- **团队**:前端/后端/AI 各几人?技能栈熟练度?关键人员是否可投入?
- **预算**:服务器/数据库/第三方 API 月成本上限?

每条填:约束 / 类型 / 量化值。**禁空话**("代码要规范"不算,要写"PEP 8 + 100% 类型注解,违反 = 拒合并")。

#### 3.3 非目标穷举(≥5 条)

提问引导:
- **明确不做的范围**:同领域内常见能力,本项目**不做**哪些?(例:支付不做退款,搜索不做语义)
- **明确不做的用户群**:不服务哪些人?(例:不服务 12 岁以下儿童)
- **明确不做的部署形态**:不部署到哪些环境?(例:不部署到国产化 OS)

每条填:我们不做什么 / 决策理由。**禁空话**("不重要的功能"不算)。

#### 3.4 自检(挖掘回合结束的关口)

- 3 个 anchor 必在产物里:grep `<!-- ANCHOR: stakeholders -->` / `<!-- ANCHOR: constraints -->` / `<!-- ANCHOR: non-goals -->`
- 行数达标:10 / 10 / 5
- 任意不达标 → `ERR_INSUFFICIENT_EXPLORATION`,**回 §3 重挖**

### 4. 拉模板

读 `docs/process/templates/00_charter.md`,看每个 `##` 段(§1-§5)需要填什么。

**关键段(锁前必填)**:
- §1 基础信息(项目名 / 一句话 / 适用场景 ≥ 3 条)
- §2.1 核心目标 ≥ 3 条(可"是/否"判定)
- §2.2 明确不做的事 ≥ 3 条(防范围蔓延)
- **§2.5 技术栈确认**(必须勾"按标准栈"或"偏离具体项",且签字行必填)
- §3 角色清单 ≥ 1 行
- §4 核心约束 / 禁忌 ≥ 3 条
- §5 反向能力(项目自填)
- §6 决策记录(项目自填)

**注**:§0 已在 §3 挖掘回合填好,本节不重复。

### 5. 引导填空

按模板顺序逐段问用户。**不要一次全问**,一段填完确认再下一段。

**关键提示**:
- §0 挖掘证据已在 §3 完成,本节专注 §1-§6
- §2.5 锁技术栈,后续 phase 不可改;偏离要写理由
- §2.2 "明确不做的事"是给 critic 抓范围蔓延用的,不能空话(详 spec §3 + critics/00_charter.md)
- §4 禁忌要写"违反会导致什么",不能光说"不能做 X"
- **填 §1-§6 时可回看 §0 摘要,防止漏点**

### 6. 写产物

写到 `docs/00_charter.md`(相对项目根)。

如果项目已用 `Use this template` 从 pm-template 复制,`docs/process/templates/00_charter.md` 是模板,`docs/00_charter.md` 是产物,**别写错位置**。

### 7. 跑 DoD

```bash
/dod-check 0
```

通过率 < 100% → 列出缺哪几条,**停下来等用户补**。不绕过 DoD 强锁。

### 8. 跑 critic

```bash
/critic 0
```

CRITICAL > 0 或 HIGH > 0 → 报告路径给用户,**停下来等用户改**。

MEDIUM > 0 → 提示"建议修但非阻塞,继续请明示"。

**Phase 0 critic 重点**(详 `docs/process/critics/00_charter.md`):
- §0 挖掘证据完整性(机械 grep):3 anchor + 行数 10/10/5
- §2.1 目标 vs §2.2 非目标有无冲突
- §4 约束是否量化
- §5 反向能力是否覆盖"砍/选"关键决定

### 9. Sign-off 提示(spec §3.2 + §12)

```
> Phase 0 待锁。
> 产物: docs/00_charter.md (<N> 行)
> §0 挖掘证据: stakeholders/constraints/non-goals = <a>/<b>/<c> 行
> critic 报告: docs/process/critics/reports/00_charter_<YYYY-MM-DD>.md
>   CRITICAL: 0 / HIGH: 0 / MEDIUM: 0 / LOW: 0
> DoD 勾选: 12/12 ✓
>
> 请确认锁:
>   [y] 锁(签字: <name> <YYYY-MM-DD>)
>   [n] 不锁(返回修改)
>   [c] 只看 critic 报告
```

**用户输入 `y`** → 继续输入:
- `name?`(非空,≤50 字符)
- `date?`(回车默认今天)

**用户输入 `n`** → 问"需修改什么?",回到 §5 重填(§0 不用重挖,除非 n 指明挖掘不够)。

**用户输入 `c`** → 完整展示 critic 报告内容。

### 10. 锁

```bash
python3 .claude/scripts/update_state.py \
  --phase 0 \
  --status "[x]" \
  --signed-by "<name>" \
  --signed-at "<YYYY-MM-DD>" \
  --critic-report-path "docs/process/critics/reports/00_charter_<YYYY-MM-DD>.md" \
  --dod-count "12/12" \
  --template-sha "<pm-template root HEAD SHA>"
```

输出 `✓ update_state(phase=0, status='[x]') 成功` + diff。

### 11. 提示下一步

> Phase 0 已锁(签字:<name> <YYYY-MM-DD>)。
> 下一步:运行 `/phase-1-requirements` 写需求。

## 错误处理

| 错误 | 行为 |
|---|---|
| `ERR_INSUFFICIENT_EXPLORATION` | 挖掘证据不全(anchor 缺/行数不够),拒绝进 §4,**回 §3 重挖** |
| `ERR_INVALID_TRANSITION` | 当前状态不可进入(已锁 / LEGACY),提示解锁路径 |
| `ERR_MISSING_TEMPLATE` | 模板缺失,提示 git submodule 或 GitHub raw 拉 |
| `ERR_VERSION_MISMATCH` | pm-template 已升,建议先 --audit 再决定 |
| critic 报 CRITICAL/HIGH | 拒绝锁,等用户改产物 |
| DoD 缺项 | 拒绝锁,等用户补 |

## 不要做的

- **不跳过 §3 挖掘回合** —— 模板里有 §0 必须填,空 = critic CRITICAL
- **不绕过 §3.4 自检** —— 4 个 anchor 缺一就 ERR_INSUFFICIENT_EXPLORATION
- 不替用户填 §2.5 签字(技术栈 = 项目生死,必须用户明示)
- 不绕过 critic 强锁
- 不写 docs/process/templates/(那是只读模板)
- 不在挖掘回合中"凭空白想"摘要,内容必须从 §1-§6 提炼(防止 LLM 自由发挥)
