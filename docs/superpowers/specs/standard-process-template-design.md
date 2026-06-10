# 标准项目流程模板 设计

> **状态**: Draft([引入日期])
> **目的**: 解决"AI 自动生成文档 + 用户未仔细 review → 实现飘忽"的问题
> **试点**: 试点项目 同 repo 跑一遍
> **本文档双重用途**: ①设计说明(给 reviewer 看) ②用户手册(给将来的"我自己"用)

---

## 0. Context & 痛点

**现状问题**:
- 当前项目(试点项目)大部分设计文档是 AI 自动理解 + 生成的
- AI 自由发挥时,会出现"功能说明跟实际需求有出入"等情况(如家长端能不能看明细、申请列表的查询入口等)
- 用户没有在每一阶段做"出文档→停下→review→签字"的环节,问题累积到编码后才暴露

**目标**:
1. 固化一个 5 阶段的项目流程,**每阶段有显式 gate**
2. 每个阶段产出"模板 + DoD + critic"三件套,**给 AI 一个填空框,而不是给一段空白**
3. **双层验证**: AI critic 自审(不修,只报)→ 用户 review → 锁
4. 关键新增: **Phase 1 需求(独立门)**——把"需求"和"设计"分开,需求不锁设计不能动

**范围(本次试点)**:
- ✅ 5 phase 流程定义
- ✅ 每 phase 的三件套(模板/DoD/critic)
- ✅ 试点项目 上跑一遍做真实反馈
- ❌ 不实现自动检查脚本(后续 Plan 4+ 再考虑)
- ❌ 不强制阻塞(用户可以选择跳过,但跳过会在 critic 报告里被标红)

**非目标(明确不做)**:
- 不做"PM 全套 5-10 份文档"(PMP 软考标准),会显著增加维护成本
- 不做 RTM(需求追踪矩阵),单人项目 ROI 极低
- 不做 change request 流程,你就是审批人

---

## 1. 流程总览

```
Phase 0  立项 (Charter)
  artifact: docs/00_charter.md
  DoD: 目标 / 范围 / 角色 / 约束 / 禁忌
  critic: 范围蔓延 / 模糊词
  ─── AI critic 自审 → 你 review → 锁 ───
                ↓
Phase 1  需求 (Requirements) ★ 新增门
  artifact: docs/01_requirements.md
  DoD: 角色清单 / 用户故事(AC) / 边界场景
  critic: 故事可测性 / AC 模糊 / 角色闭环
  ─── AI critic 自审 → 你 review → 锁 ───
                ↓
Phase 2  概要设计 (High-level Design)
  artifact: docs/02_high_level_design.md
  DoD: 架构 / 数据模型 / 接口清单 / NFR
  critic: 范围蔓延(对 Phase 1)/ 过度设计
  ─── AI critic 自审 → 你 review → 锁 ───
                ↓
Phase 3  详细设计 (Detailed Design)
  artifact: docs/03{a,b,c}_*.md
  DoD: 100% 覆盖 Phase 2 / 异常 ≥90%
  critic: 参数最少性 / 异常码齐 / 闭环
  ─── AI critic 自审 → 你 review → 锁 ───
                ↓
Phase 4  实现 + 验证 (Impl + Verify)
  artifact: code + tests + deploy(无 doc 模板)
  DoD: 全部 AC 通过 e2e / 文档反向同步
  critic: 实现漏 AC / 范围蔓延 / 反向需求真没做
  ─── AI critic 自审 → 你 review → 锁 ───
```

**核心规则**:
1. **下游 100% 可追溯到上游** — Phase N 的每一项必须在 Phase N-1 找到出处
2. **未通过 DoD 不进下一 phase** — 哪怕下一 phase 的 doc 已写,先回来补 DoD
3. **每个 artifact 末尾有"决策记录"小节** — 记录"为什么砍 / 为什么加"
4. **critic 不修,只报** — 修是你和 AI 协作的事

---

## 2. 仓库结构

### 2.1 权威映射表(避免编号歧义)

> 编号是单一真源。看这一张表就能反查"这个 phase 产生哪些文件"。

| Phase | artifact 文件 | 模板文件 | DoD 文件 | critic 文件 |
|---|---|---|---|---|
| 0 立项 | `docs/00_charter.md` | `docs/process/templates/00_charter.md` | `docs/process/dod/00_charter.md` | `docs/process/critics/00_charter.md` |
| 1 需求 ★ | `docs/01_requirements.md` | `docs/process/templates/01_requirements.md` | `docs/process/dod/01_requirements.md` | `docs/process/critics/01_requirements.md` |
| 2 概要设计 | `docs/02_high_level_design.md` | `docs/process/templates/02_high_level_design.md` | `docs/process/dod/02_high_level_design.md` | `docs/process/critics/02_high_level_design.md` |
| 3a 详细业务流程 | `docs/03a_business_process.md` | `docs/process/templates/03_detailed_design.md` (章节 A) | `docs/process/dod/03_detailed_design.md` | `docs/process/critics/03a_business_process.md` |
| 3b 详细接口设计 | `docs/03b_api_design.md` | `docs/process/templates/03_detailed_design.md` (章节 B) | 同上(共享) | `docs/process/critics/03b_api_design.md` |
| 3c 数据表 DDL | `docs/03c_data_schema.md` + `sql/*_schema.sql` | `docs/process/templates/03_detailed_design.md` (章节 C) | 同上(共享) | `docs/process/critics/03c_data_schema.md` |
| 4 实现+验证 | (无 doc,代码 + tests) | (无) | `docs/process/dod/04_implementation.md` | `docs/process/critics/04_implementation.md` |

> 注:Phase 3 三件产物共享同一份模板(章节分 A/B/C),各自由独立 critic 文件做专业审视。

### 2.2 文件树

```
docs/
├── process/                          ← 流程资产(本次设计落地点)
│   ├── README.md                     ← 入口:流程总览 + 使用说明
│   ├── STATE.md                      ← 试点流转状态(见 §5)
│   ├── CHANGELOG.md                  ← 模板迭代历史(用户用顺手后回写)
│   ├── templates/                    ← artifact 模板(给 AI 看,让它填空)
│   │   ├── 00_charter.md
│   │   ├── 01_requirements.md       ★ 新增
│   │   ├── 02_high_level_design.md
│   │   └── 03_detailed_design.md     ← 章节 A/B/C 合一
│   ├── dod/                          ← DoD checklist
│   │   ├── 00_charter.md
│   │   ├── 01_requirements.md
│   │   ├── 02_high_level_design.md
│   │   ├── 03_detailed_design.md
│   │   └── 04_implementation.md
│   ├── critics/                      ← critic prompt
│   │   ├── 00_charter.md
│   │   ├── 01_requirements.md
│   │   ├── 02_high_level_design.md
│   │   ├── 03a_business_process.md
│   │   ├── 03b_api_design.md
│   │   ├── 03c_data_schema.md
│   │   └── 04_implementation.md
│   └── critics/reports/              ← critic 自审报告存档(强制)
│       ├── 00_charter_<YYYY-MM-DD>.md
│       ├── 01_requirements_<YYYY-MM-DD>.md
│       ├── 02_high_level_design_<YYYY-MM-DD>.md
│       ├── 03a_business_process_<YYYY-MM-DD>.md
│       ├── 03b_api_design_<YYYY-MM-DD>.md
│       ├── 03c_data_schema_<YYYY-MM-DD>.md
│       └── 04_implementation_<YYYY-MM-DD>.md
│
├── 00_charter.md                     ← Phase 0 artifact 实例(从 现有 项目章程.md 迁移)
├── 01_requirements.md                 ← Phase 1 artifact 实例(★ 待创建)
├── 02_high_level_design.md            ← Phase 2 artifact 实例(从 现有 概要设计文档.md 迁移)
├── 03a_business_process.md           ← Phase 3a artifact 实例
├── 03b_api_design.md                 ← Phase 3b artifact 实例
├── 03c_data_schema.md                ← Phase 3c artifact 实例
├── 功能说明.md                        ← 保留(读者视角,跨 phase 总结)
└── superpowers/
    ├── specs/                        ← 单次大改动设计 spec(见 §2.3)
    └── plans/                        ← 实施计划(与本流程正交,继续用)
```

**命名约定**: `0X_<name>.md` 编号一眼看出在流程的什么位置。新建项目照样用。

### 2.3 `docs/superpowers/specs/` vs `docs/process/` 的关系(易混点)

- **`docs/process/`** = **可复用的流程模板**,新项目拷过去就能用。本 spec 也是这个目录的入口 README 之一(待落地)。
- **`docs/superpowers/specs/`** = **当前项目某次具体大改动的设计 spec**(如"管理端扩展设计")。是一次性的,不会拷到下一个项目。
- 二者**正交**:`process/` 是"怎么走流程",`superpowers/specs/` 是"当前项目在某个 phase 里具体要做什么"。
- 类比:`process/` 是建筑规范,`superpowers/specs/` 是某栋楼的施工图。

---

## 3. 三件套的通用格式

### 3.1 `templates/0X_*.md` artifact 模板

> 用途: AI 生成时按章节填空,**给框不给自由**

骨架:
```markdown
# [Phase X] 文档名 模板

> 用途: ...
> 输入: 来自 Phase (X-1) ...
> 产出: ...

## 1. ...
## 2. ...
...

## N. 决策记录
- "为什么砍 X / 为什么选 Y 路径" — 重要决定要写,后人看得见

## N+1. critic 报告 + 签字(锁前最后一节)
- [ ] critic 自审:无 CRITICAL/HIGH
- [ ] 你本人 review + 签字:日期 ____ 签字 ____
```

### 3.2 `dod/0X_*.md` DoD checklist

> 全部勾上才允许进下一 phase。每条都是**可机械验证**的。

```markdown
# [Phase X] DoD Checklist

- [ ] 1.1 ... (可机械验证)
- [ ] 1.2 ... (数量要求,如"≥3 条")
- [ ] 2.1 ...
- ...
- [ ] **N+1.1 critic 自审报告无 CRITICAL/HIGH 问题**
- [ ] **N+1.2 你本人 review 过,在 §N+1 末尾签字 (YYYY-MM-DD)**
```

### 3.3 `critics/0X_*.md` critic prompt

> 复制这段发给 AI,让 AI 自审 `<artifact_file>`。角色是**严苛的 PM critic,只报不修**。

```markdown
# [Phase X] Critic Prompt

## 你要检查的(逐项报)

1. **范围蔓延** — ...
2. **角色闭环** — ...
3. **约束可执行性** — ...
4. **决策追溯** — ...
5. **可测性** — ...

## 输出格式
- 报告 markdown
- 每条问题标注级别: CRITICAL(必须修) / HIGH(应该修) / MEDIUM(建议修) / LOW(可忽略)
- CRITICAL/HIGH 不允许"作者意图如此"开脱
- 不修,只报

## 自我约束(防 critic 自行降级)

- **若你(AI critic)倾向于把 CRITICAL 标成 MEDIUM,先停**——自问:"如果我是人,看到这条会接受吗?"
- **若你给一条 CRITICAL 找到的反开脱是"作者意图如此 / 上下文合理"**,**必须升级到 ESCALATE-TO-HUMAN**,由人裁定。不要自降级。
- **若你的报告里 CRITICAL/HIGH 数量 = 0**,自检:"我真的认真查了吗?还是默认通过了?"默认是 0 的报告不可信,需在末尾写"我已自检,本次确无问题,基于:____"理由。
```

---

## 4. 各 Phase 详解

### 4.1 Phase 0 立项

**Artifact** `docs/00_charter.md`:

| § | 内容 | 关键约束 |
|---|---|---|
| 1 | 基础信息 | 项目名 / 一句话描述 / 适用场景 |
| 2 | 目标与非目标 | 核心目标 ≥3 条,非目标 ≥3 条(防范围蔓延) |
| 3 | 角色清单 | ≥2 角色,空角色也算一种状态 |
| 4 | 核心约束 / 禁忌 | ≥3 条,每条都写"违反会导致什么" |
| 5 | 反向能力(明确不引入) | ≥3 条,常见 AI 自由发挥会偷偷加的能力 |
| 6 | 决策记录 | ≥1 条 |
| 7 | critic + 签字 | 双层验证 |

**DoD 关键项**:
- §2.1 核心目标 ≥3 条,**每条都是可验证的(不是"做得好")**
- §2.2 非目标 ≥3 条,每条都明确"不做什么"
- §4 约束每条都"违反会导致什么",空话扣分
- critic 无 CRITICAL/HIGH + 你本人签字

**Critic 主要查**:
- 范围蔓延:§2.1 vs §2.2 有无冲突?有没有偷偷加的?
- 角色闭环:§3 是否覆盖所有用户类型?空角色/异常角色有定义吗?
- 约束可执行性:§4 是否每条都"违反会导致什么"?
- 决策追溯:§5 反向能力是否覆盖"砍/选"的关键决定?
- 可测性:§2.1 每条目标是否都可以"是/否"判定完成?

---

### 4.2 Phase 1 需求 ★ 新增门

**Artifact** `docs/01_requirements.md`:

| § | 内容 | 关键约束 |
|---|---|---|
| 1 | 角色清单(从 charter 继承,允许细化) | 4 列必填:角色/定位/位置/鉴权 |
| 2 | 用户故事 | 格式:**作为[角色],我想要[能力],以便[价值]** |
| 2.x | 故事格式 | 故事 ID(S-XX) + 来源(charter §X.X) + ≥1 条 AC |
| 3 | 边界场景与异常 | 5-15 条,覆盖并发/鉴权失败/数据不存在/状态非法 |
| 4 | 非功能需求 | 性能/安全/合规/可观测 |
| 5 | 反向需求(明确砍掉) | ≥3 条,防下 phase AI 偷偷加回 |
| 6 | 决策记录 | 重要决定的"为什么" + 推翻之前什么假设 |
| 7 | critic + 签字 | |

**故事拆分准则**(避免 AI 写 30 条琐碎或 5 条巨型):
- **一条故事 = 一个原子 AC**。如果一条故事的 AC 数 > 3,应拆分。
- **拆故事沿用 INVEST**:Independent(独立)/ Negotiable(可协商)/ Valuable(有价值)/ Estimable(可估)/ Small(小)/ Testable(可测)
- **合并条件**:两个 S 描述同一角色同一能力同一目的,合并;否则保留独立 S

**用户故事示例**:
```markdown
- **S-01** 作为儿童,我想要查看个人零花钱账户余额,以便知道自己还有多少钱可花
  - 来源: charter §3 角色:child
  - **AC-01.1**: 调用 `GET /get-balance?doubao_id=xxx&child_user_id=xxx` 返回 `balance` + `monthly_limit`
  - **AC-01.2**: 余额 = 0 时仍返回 200,balance = "0.00"
  - **AC-01.3**: doubao_id 与 child_user_id 不匹配时返 403
```

**完整模板样例(`docs/process/templates/01_requirements.md` 实际内容,直接 copy)**:
```markdown
# 需求文档模板

> 用途: 锁住"做什么、不做什么、做到什么程度算完"
> 输入: 来自 Phase 0 charter
> 产出: 用户故事 + 验收标准 + 边界场景,所有 phase 2+ 的源头
> 禁止: 不写架构、不写接口、不写表 — 那是 Phase 2/3 的事

## 1. 角色清单(从 charter 继承)
| 角色 | 一句话定位 | 出现位置 | 鉴权方式 |
|---|---|---|---|

## 2. 用户故事

> 格式: **作为 [角色],我想要 [能力],以便 [价值]**
> 每条: 故事 ID(S-XX) + 来源(charter §X.X) + ≥1 AC(AC-XX.Y)
> 拆分准则: 一条故事 = 一个原子 AC,AC 数 >3 必拆

### 2.1 [角色 A] 的故事
- **S-01** 作为 ___,我想要 ___,以便 ___
  - 来源: charter §___
  - **AC-01.1**: ___
  - **AC-01.2**: ___

### 2.2 [角色 B] 的故事
- **S-10** ...

## 3. 边界场景与异常

| # | 场景 | 期望行为 | 不允许的行为 |
|---|---|---|---|
| E-01 | 同一操作重复触发 | 二次幂等(返同结果不二次落账) | 二次扣款 |
| E-02 | ___ | ___ | ___ |

(覆盖:并发 / 鉴权失败 / 数据不存在 / 状态非法)

## 4. 非功能需求
- 性能: ___
- 安全: ___
- 合规: ___
- 可观测: ___

## 5. 反向需求(明确砍掉)
- ❌ 不做 ___(原因: ___)
- ❌ 不做 ___(原因: ___)

## 6. 决策记录
- YYYY-MM-DD: 砍掉 ___,因为 ___
- YYYY-MM-DD: 选了 ___,因为 ___

## 7. critic + 签字
- [ ] critic 自审报告无 CRITICAL/HIGH(报告路径: ___)
- [ ] 你本人 review + 签字: _______ (YYYY-MM-DD)
```

**DoD 关键项**:
- 1.1 角色清单 ≥2 行,每行 4 列都填
- 2.1 每条故事有 S-ID + 来源 + ≥1 AC
- 2.2 每条 AC 可机械验证(无"差不多就行")
- 2.3 故事数量 8-30 条(太少=没想清楚,太多=没拆)
- 3.1 边界场景 ≥5 条,覆盖:并发 / 鉴权失败 / 数据不存在 / 状态非法
- 5.1 反向需求 ≥3 条
- critic 无 CRITICAL/HIGH + 你本人签字

**Critic 主要查**:
- 故事可测性:每条 AC 是否可以"是/否"判定?模糊词("快速"/"友好")扣分
- AC 模糊性:有"差不多"/"基本"这类词报 CRITICAL
- 角色闭环:每个角色都有 ≥3 条故事?没有"未授权访客"的故事?
- 边界覆盖:并发场景(同操作重复触发)有没有?幂等策略?
- 反向需求:列的"不做"够具体?避免"反正不做 X"这种空话

---

### 4.3 Phase 2 概要设计

**Artifact** `docs/02_high_level_design.md`:

| § | 内容 | 关键约束 |
|---|---|---|
| 1 | 架构视图 | 文字图(模块/层级/数据流,3-5 段),不写代码/不写 DDL |
| 2 | 数据模型(逻辑层) | 每张表的目的 / 关键字段 / 唯一约束 / 索引意图 |
| 3 | 接口清单 | **每行必须追溯到 Phase 1 的 S-XX**,否则"未在需求出现" |
| 4 | 非功能需求落点 | 性能 / 安全 / 可观测 |
| 5 | 反向设计(明确不引入) | 不引入群组 / 不引入数据隔离 等被 charter 禁忌但 AI 容易加上的 |
| 6 | 决策记录 | |
| 7 | 末尾自查:孤儿检查 | 列出"§3 接口清单中所有 S-ID 不在 Phase 1 故事集合里的接口",应为 0 |
| 8 | critic + 签字 | |

**DoD 关键项**:
- §3 接口清单每行有 S-ID 追溯(100% 覆盖,无孤儿)
- §7 末尾自查:孤儿接口数 = 0(可机械验证 — 提取 S-ID 集合 vs Phase 1 故事 ID 集合,求差集)
- §5 反向设计 ≥3 条
- 没有出现 charter §4 禁忌的设计(如"群组隔离" / "数据按家长分库")
- §2 每张表都有"为什么需要"的一行注释(防止"先建着以后用")
- critic 无 CRITICAL/HIGH + 你本人签字

**Critic 主要查**:
- 范围蔓延:§3 接口清单里有无 Phase 1 故事没出现的"新能力"
- 过度设计:有无群组/隔离/层级这种被禁忌的设计被悄悄加回
- 表膨胀:§2 表数是否超出 charter 规定的数量

---

### 4.4 Phase 3 详细设计

**Artifact 拆 3 个文件**:

| 文件 | 内容 |
|---|---|
| `03a_business_process.md` | 详细业务流程(状态机图、流程图) |
| `03b_api_design.md` | 详细接口设计(path/method/入参/出参/错误码) |
| `03c_data_schema.md` | 数据表 DDL(sql/*_schema.sql) |

**DoD 关键项(更细)**:
- 03a 每条业务流程的"正常 + 异常"配对齐全
- 03a 涉及金额的流程都标注"同事务内联动 balance"(防漏更新)
- 03b 接口清单 = Phase 2 §3 的 100%(不多不少)
- 03b 末尾自查:列出"03b 接口清单中所有不在 Phase 2 §3 的接口",应为 0
- 03b 每个接口有 4 列必填:鉴权依赖 / 错误码清单 / 幂等策略 / 限频策略
- 03b 入参是"最小集"——多 1 个字段扣分
- 03c DDL 可直接执行(放进 sql/ 跑一遍)
- 03c 字段命名 100% 对齐 charter §3 规范
- 03c 末尾自查:列出"所有不在 Phase 2 §2 数据模型里的新表",应为 0
- critic 无 CRITICAL/HIGH + 你本人签字

**Critic 主要查**:
- 入参最小性:多一个冗余字段就报(防止"以后可能用")
- 异常码齐全:每个接口的 401/403/404/409/422 全部覆盖
- 闭环:每条流水改动都走"同事务内"——漏返 CRITICAL
- 状态机非法:approved 后还能改?
- 范围蔓延:同 §4.3 §7,检查 03a/b/c 新增内容是否都在 Phase 1/2 出现过

---

### 4.5 Phase 4 实现 + 验证

> Phase 4 **没有 template 文件**——它是动作,不是文档。但有 DoD 和 critic。

**DoD 关键项**:
- 编码(按项目习惯,本项目默认"先实现后测试")
- 单测: 覆盖 Phase 3b 接口(每接口 ≥1 happy + 1 sad)
- e2e: 覆盖 Phase 1 每条 AC(每 AC ≥1 e2e case,AC-编号 = e2e case 名)
- 部署: docker compose up 起得来
- 文档反向同步: 03b 接口 vs 实际后端代码 100% 一致
- 反向需求验证: Phase 1 §5 反向需求列的"不做的事"在代码里真的没做
- 决策记录更新: 实现中发现与文档不一致的,回写 §6
- critic 无 CRITICAL/HIGH + 你本人签字

**Critic(用 `docs/process/critics/04_implementation.md` 的 prompt 跑)**:
- 漏 AC:Phase 1 每条 AC 对应的接口/操作,代码里找得到对应实现?
- 范围蔓延:代码里有无 Phase 1 故事没出现的能力?(重点查"管理员"能干的私活)
- 反向需求:Phase 1 §5 列的"不做"在代码里真没做?
- 一致性:接口路径/方法/入参跟 03b 是否 100% 对齐?

---

## 5. STATE.md 状态文件

**位置**: `docs/process/STATE.md`

**格式**:
```markdown
# 流程流转状态

> 锁定状态用 [ ] / [~] / [x] 表示: [ ] 未开始 / [~] 进行中 / [x] 已锁
> (使用 ASCII 不用 emoji,git diff 友好)

## Phase 0 立项
- 状态: [x]
- 锁定时间: YYYY-MM-DD
- artifact: docs/00_charter.md
- DoD: 7/7 ✓
- critic 报告: docs/process/critics/reports/00_charter_YYYY-MM-DD.md
- 签字: <签字人>

## Phase 1 需求
- 状态: [~]
- artifact: docs/01_requirements.md
- DoD: 5/9 (缺: 5.1 反向需求 / 7.1 critic / 7.2 签字)
- 下一步: 补反向需求 → 跑 critic → 签字
```

**规则**:
- 每 phase 锁时,在 STATE.md 写入锁定时间 + DoD 计数 + 签字
- 锁定的 phase 不允许改动(若需改,走 §6.3 "开锁"流程)
- **跳过 phase 不允许沉默省略**——必须在 STATE.md 写一行:
  ```markdown
  ## Phase 2 概要设计
  - 状态: [SKIP]
  - 跳过原因: 本次改动只动 Phase 3(详设),不涉及架构层面调整
  - 跳过签字: [签字人] [引入日期]
  - 影响范围: 无下游影响
  ```
  这样 critic 不会因为"没产物"而漏检。

**LEGACY 例外**(试点历史包袱处理):
> 用于把"实施已完成但没用本流程"的旧 phase 标 `[x] LEGACY` 而非 `[x]`,理由附后。**不适用于新项目**。
```markdown
## Phase 4 实现+验证
- 状态: [x] LEGACY
- 锁定时间: YYYY-MM-DD(本流程引入日)
- LEGACY 原因: 实施在本流程引入前完成,已有 e2e/单测验证,未走本流程的 critic
- 追溯证据: <e2e 报告路径> + <单测报告路径>
- 签字: <签字人>
```

**解锁流程(unlock)格式**:
```markdown
## Phase 1 需求 [UNLOCKED]
- 原锁时间: YYYY-MM-DD
- 解锁时间: YYYY-MM-DD
- 解锁原因: <具体原因,引用 critic 报告或用户反馈>
- 影响范围: Phase 2/3 中所有依赖的接口(列出)
- 重新锁定时间: YYYY-MM-DD(待定)
- 重新签字: (待)

## ⚠️ 重新锁定前的下游处理
- [ ] Phase 2 §3 接口清单中相关接口已删除/调整
- [ ] Phase 3a/b 涉及相关流程已重写
- [ ] 代码中对应接口已废弃/重命名
- [ ] 重跑 Phase 2-3 的 critic
- [ ] 你本人签字
```

**强制**:解锁锁定 phase **必须**重跑所有下游 phase 的 critic + 签字,不能只改本 phase 文档。

---

## 6. 用户使用手册(How)

### 6.1 怎么开始一个新项目

1. 复制 `docs/process/templates/00_charter.md` 到 `docs/00_charter.md`
2. 告诉 AI:"请按 `docs/process/templates/00_charter.md` 填空,主题是 <你的项目>"
3. AI 出稿后,把产物交给 critic:
   - 复制 `docs/process/critics/00_charter.md` 的 prompt + `<artifact_file>` 路径
   - 让 AI 跑自审
4. 你 review critic 报告,**逐条判断**:
   - CRITICAL/HIGH → 让 AI 改,重跑 critic
   - MEDIUM/LOW → 自己决定改不改
5. 你本人勾完 `dod/00_charter.md` 全 7 项
6. 在 artifact 末尾 §7 签字(日期 + name)
7. 更新 `docs/process/STATE.md` 把 Phase 0 标 [x]
8. 进 Phase 1,重复 1-7

### 6.2 怎么跑一次 critic

- 把 `docs/process/critics/0X_*.md` 完整内容复制到对话开头
- 加一句:"请对 `<artifact_file_path>` 跑自审,产出 markdown 报告"
- 报告**必须**存到 `docs/process/critics/reports/0X_<phase>_<YYYY-MM-DD>.md`(强制,不可选)
- 在 STATE.md 填入报告路径

### 6.3 怎么签字 lock 与 unlock

**lock**:
- 在 artifact 文件末尾 §N+1(critic + 签字)写明日期和签名
- 在 `STATE.md` 把状态改 [x],写入 `locked_at`
- 一旦锁,**不允许改动**

**unlock**(发现锁定 phase 写错了):
- 在 STATE.md 用 §5 的 unlock 格式记录
- 改完 phase 后,**强制**重跑所有下游 phase 的 critic + 签字
- 这是不可绕过的(防止"上游改了,下游没跟上"的常见 bug)

### 6.4 怎么从 STATE.md 看进度

- 一眼看到当前在哪个 phase
- 一眼看到每个 phase 的 critic 报告位置
- 一眼看到 DoD 缺哪几项没勾

---

## 8. 决策记录(本设计的"为什么")

| 决定 | 备选 | 为什么选这个 | 何时重新评估 |
|---|---|---|---|
| 5 phase 而非 3 | 3 phase(立项+需求+合并) | 5 phase 把"需求"和"设计"严格分开,这是用户原话痛点("需求飘")的根因 | 若用户多次反馈"5 phase 太重想合并",可降回 4 phase |
| 新增 Phase 1 独立需求 | 把需求塞回概设 | 用户原话"必须独立成门" | 若需求规模固定 ≤5 条 S,可考虑合并到概设顶部 |
| 双层验证(AI critic + 人 review) | 只 AI critic / 只人 review | "AI 自由发挥"问题需要 AI 找 AI 漏洞,但最终签字必须人来 | 若试点发现 critic 误报率 > 70%,需重写 critic prompt |
| 不写自动检查脚本 | 写 Python 脚本强阻塞 | 单人项目,过重;用 markdown 勾选 + critic 报告做软约束足够 | 若多次"忘记勾 DoD 跳 phase",加脚本 |
| 同 repo `docs/process/` 放(早期) → 抽离独立仓库 pm-template | 一直放独立仓库 | 早期在试点项目内同仓迭代更快,跑通后抽离成 pm-template 供所有新项目复用 | 已在 pm-template v0.1.0 完成抽离 |
| 拆分文件(一个 phase 三件套) | 合并单文件 handbook | 用户原话;多文件更易维护,每件套独立可读 | 若用户反馈"找文件麻烦",可考虑加 README 索引 |
| `STATE.md` 独立文件 | YAML frontmatter | 用户原话;集中管理状态 | 若引入自动检查脚本,转回 frontmatter(更易被脚本读) |
| DoD 末两条固化 critic + 签字 | 不固化,靠自觉 | 用户原话痛点就是"没签字",固化才是真约束 | — |
| 反向需求 / 反向设计独立小节 | 写在决策记录里 | AI 自由发挥时最常"加回被砍的能力",独立小节让 critic 易扫 | — |
| 用户故事用 S-ID + AC 编号 | 用 FRD / UC 编号 | 与 e2e case 名一致,实现层 grep 可追溯 | — |
| Phase 4 无 template 文件 | 也要 template | Phase 4 是动作不是文档,有 DoD + critic 即可 | — |

---

## 9. 风险 & 缓解

| 风险 | 缓解 |
|---|---|
| 用户嫌 DoD 太多,跳过签字 | STATE.md 把"跳过签字"显式标红,而不是默默通过 |
| critic 误报太多,信任崩 | 跟踪 critic 报告与实际问题的吻合度,试点结束后调整 prompt |
| 模板太死,某些小项目不需要 5 phase | 暂不解决,试点数据说话;若确实需要,可后续加"快速模式"(3 phase) |
| 旧文档没及时迁移,新流程成了"额外的纸" | 强制要求所有现有 doc 迁移后才算跑通(用 LEGACY 标记 + 迁移 checklist) |
| 反向需求清单被 AI 自动"加回" | 反向需求写完后,Phase 2-4 critic 都要 grep 检查"反向需求关键字没出现在新 doc/代码中" |

---

## 10. 未来 (Plan 4+)

- ✅ v0.1.0 已完成:流程模板抽离成 `pm-template` 独立仓库
- 长期可考虑:**Claude Code skill** 把整个流程做成 `/new-project` slash command
- 长期可考虑:**自动检查脚本**(读 markdown 提取 DoD 勾选状态,未勾全让用户强制确认)
- 跨项目复用:**每个新项目 git submodule + 锁定版本**

---

## 11. 验收标准(本 spec 自身)

> 每条都是可机械验证的,不写"差不多就行"。

- [ ] **冷启动测试**:关掉所有 AI 上下文,用户根据 §6 用户手册,独立走完 Phase 0 → Phase 1 全流程,不查 spec 也能继续。判定:成功完成,不依赖任何外部解释。
- [ ] **模板填充测试**:把 `templates/01_requirements.md` 给一个新对话的 AI,主题"给家庭记账",跑一次填充。判定:产物需重写的 section 数 ≤ 3(总 section 数 7)。
- [ ] **DoD 模糊性审计**:grep `dod/*.md` 检查是否含 "差不多 / 还可以 / 大致 / 合理" 这类模糊词。判定:命中数 = 0。
- [ ] **critic 真问题率**:跑 3 次 critic 报告(对同一 artifact 不同时点),统计用户认可为"真问题"的 CRITICAL/HIGH 占比。判定:≥ 30%(3 次,3-9 个真问题)。
- [ ] **解锁流程跑通**:人为触发一次 unlock(改一个锁定的 phase),验证 §6.3 unlock 流程完整可走。判定:无歧义,STATE.md 留痕。
