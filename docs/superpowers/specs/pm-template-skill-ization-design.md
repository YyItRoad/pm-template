# pm-template Skill 化 — 设计 spec

> **状态**: ✅ 设计已批准,实施中
> **目的**: 把 pm-template 的 5-phase 流程 + tech_stack 资产做成 Claude Code skill,从"死的文档"升级为"活的流程引擎"
> **范围**: 13 skill(1 入口 + 5 phase + 4 辅助 + 3 维护期/跨切面)+ 1 共享状态 helper + 跨项目版本管理
> **关联 spec**: [standard-process-template-design.md](standard-process-template-design.md) · [standard-tech-stack-design.md](standard-tech-stack-design.md)
> **版本**: 与 pm-template git tag 绑定(v1.0 = 本 spec 初版)

---

## 一、Context(为什么做)

### 1.1 痛点

pm-template 仓库已落地:`docs/process/{templates,dod,critics,tech_stack.md}` 共 20+ 文件齐全,GitHub "Use this template" 可用。

但实际使用时,**流程靠用户自觉**:
- 用户必须自己读懂 5 phase 是什么、顺序怎么走
- 用户必须自己记得每个 phase 跑 critic、勾 DoD、签字
- 用户必须自己维护 STATE.md(常写错格式 / 漏填字段)
- 用户必须自己判断"Phase 2 改了,Phase 3 要不要重跑"(unlock 流程)

**结果**: 即使有完整模板资产,用户在填空时还是会偷懒 / 漏掉 critic / 跳过签字,等于白做。

### 1.2 目标

把 pm-template 资产封装成 Claude Code skill,实现:

| 维度 | 现状 | skill 化后 |
|---|---|---|
| 流程一致性 | 靠人记 | 强制按 5 phase 走 |
| 模板填空 | 人 copy + 找 AI | 一句话触发 |
| critic 跑 | 人记得才跑 | 模板填完自动跑 |
| DoD 勾选 | 人对照手勾 | skill 逐条验证 |
| STATE.md | 人手动维护 | 共享 helper 强制规范 |
| 锁确认 | 人脑子记 | skill 显式 sign-off 提示 |
| 偏航检测 | 靠人警觉 | critic 自动抓 |

### 1.3 非目标(明确不做)

- ❌ 远程 skill marketplace
- ❌ 多人协作锁
- ❌ 跨项目状态聚合 dashboard
- ❌ skill 自动升级(子项目自己 `git pull`)
- ❌ skill 单独走 semver(版本分裂)
- ❌ Phase 0 之前的"项目候选阶段"

---

## 二、架构总览

### 2.1 Skill 总览

```
Claude Code 会话
    │
    ▼ 用户输入
/new-project <topic>     ← 唯一入口 skill
    ├── 读 <cwd>/docs/process/STATE.md
    ├── 读 <cwd>/docs/process/tech_stack.md (L1 锁)
    └── 串行调度 phase 0→4:
         /phase-0-charter → /phase-1-requirements → /phase-2-design
         → /phase-3-detail → /phase-4-implement
                    │
                    ▼
              /state    ← 任何 phase 末手动调,显示进度

辅助 skill(独立可用):
  /critic <phase>       ← 单跑 critic 模板
  /dod-check <phase>    ← 单跑 DoD 勾选
  /unlock <phase>       ← 解锁 [x] phase + cascade 下游(spec §3.4)
```

### 2.2 13 Skill 职责矩阵

> spec 最初标 10 skill(变更入口后扩为 11,P2 #14 修复加 decision / release → 13)。

| # | Skill 文件 | 触发命令 | 职责 | 写 STATE.md |
|---|---|---|---|---|
| 1 | `new-project.md` | `/new-project <topic>` | 入口,串行调度 phase 0→4 | 不直接写 |
| 2 | `phase-0-charter.md` | `/phase-0-charter` | 拉模板填 §1-§6 + §2.5 stack 签字 | 写 [x] Phase 0 |
| 3 | `phase-1-requirements.md` | `/phase-1-requirements` | 拉模板写故事/AC/边界 + critic | 写 [x] Phase 1 |
| 4 | `phase-2-design.md` | `/phase-2-design` | 拉模板写架构/数据/接口清单 | 写 [x] Phase 2 |
| 5 | `phase-3-detail.md` | `/phase-3-detail` | 拉模板拆 3a/3b/3c + 3 critic | 写 [x] Phase 3 |
| 6 | `phase-4-implement.md` | `/phase-4-implement` | 写代码 + e2e + DoD 末条 AC 覆盖 | 写 [x] Phase 4 |
| 7 | `state.md` | `/state` | 读 STATE.md,渲染当前 phase + 建议下一步 | 只读 |
| 8 | `critic.md` | `/critic <phase>` | 单跑 critic 模板,产报告存档 | 不写 |
| 9 | `dod-check.md` | `/dod-check <phase>` | 单跑 DoD 勾选,缺啥报啥 | 不写 |
| 10 | `unlock.md` | `/unlock <phase>` | 解锁 [x] phase + cascade 下游(改产物的入口) | 写 [UNLOCKED] |
| 11 | `change.md` | `/change <type> <name>` | 维护期变更入口(feature/bugfix/refactor/hotfix/doc) | 写变更日志段 |
| 12 | `decision.md` | `/decision <title>` | ADR 入口(架构决策记录,贯穿全程) | 写决策日志段 |
| 13 | `release.md` | `/release vX.Y.Z` | 聚合 [x] 变更 → 1 个 release + git tag | 不写(写 docs/releases.md) |

### 2.3 关键约束

- skill 写 STATE.md **必须**走唯一 helper `update_state()`(避免格式漂移 + 并发覆盖)
- 13 skill **只读** `docs/process/templates/` `dod/` `critics/` `tech_stack.md`(不修改模板)
- Phase 4 特殊:写业务代码,不是文档
- 所有 skill 启动时**先检查 pm-template git SHA 是否变更**(版本对齐 warn)

---

## 三、Orchestrator 算法

### 3.1 `/new-project <topic>` 执行步骤

```
1. 读 <cwd>/docs/process/STATE.md
   ├─ 不存在 → 拉空 STATE 模板 → 写到 <cwd>/docs/process/STATE.md
   └─ 存在   → 解析每个 phase 状态
2. 找第一个非 [x] 的 phase,从那里开始(支持中途加入)
3. 展示 tech_stack.md §1 锁层级,让用户确认 L1 锁(逐条展示 L1 项,用户输入 y 接受 → 写入 `docs/00_charter.md` §2.5)
4. 串行执行:
   for phase in [0, 1, 2, 3, 4]:
     if STATE[phase] == [x] : 跳过(已锁)
     else:
       调 /phase-N-XXX skill(同会话内)
       用户签字 → update_state(phase, '[x]', signed_by, signed_at)
5. 全部 [x] → 提示"5 phase 全部锁,进入实施支持模式"
```

### 3.2 Sign-off 模式(用户介入点)

每个 phase skill 锁前必须问:

```
> Phase 0 待锁。
> 产物: docs/00_charter.md (187 行)
> critic 报告: docs/process/critics/reports/00_charter_YYYY-MM-DD.md (无 CRITICAL/HIGH)
> DoD 勾选: 12/12 ✓
>
> 请确认锁:
>   [y] 锁(签字: <name> <YYYY-MM-DD>)
>   [n] 不锁(返回修改)
>   [c] 只看 critic 报告
```

**核心原则**: 锁 = 用户明示,skill 不替用户锁。

### 3.3 失败 / 偏航处理

| 场景 | 行为 |
|---|---|
| critic 报 CRITICAL/HIGH | 不推下一步,显示报告,等用户改 |
| DoD 缺项 | 同上,显示缺哪几项,等用户补 |
| 用户中途 `Ctrl+C` | STATE.md 留 [~],下次 `/new-project` 续 |
| Phase N 已锁,Phase N-1 改了 | 走 unlock:提示重跑 Phase N-1 critic + N 签字 |

### 3.4 Unlock 详细流程(依赖 phase 联动)

当 `update_state(phase, '[UNLOCKED]', reason=...)` 被调用时:

```
1. update_state 内部:
   - 写 phase 为 [UNLOCKED],记 unlock_reason + unlocked_at
   - 找到所有 phase > unlock_phase,自动标 [UNLOCKED] + reason="upstream re-opened"
   (即解锁 Phase 2 会连锁 unlock Phase 3/4)
2. 下次 /state 或 /new-project 启动时:
   - 提示"Phase 2/3/4 已 cascade unlock,需逐 phase 重跑 critic + 签字"
3. 用户可手动选 phase 重跑,或 /new-project 顺序跑
```

**例**:Phase 2 改了接口清单 → Phase 2 [UNLOCKED] → Phase 3 [UNLOCKED](cascade) → Phase 4 [UNLOCKED](cascade)。下次跑从 Phase 2 开始,3 和 4 也会被 critic 抓出"上游接口变了"。

### 3.5 L1 锁确认细节

`/new-project` 第 3 步的具体交互:

```
> 读 tech_stack.md §1 锁层级(38 条 L1 锁)
> 展示给你确认:
>   🔒 L1-001: Python 3.12+
>   🔒 L1-002: FastAPI 0.115+
>   ...(共 38 条)
>
> 全部接受?(输入 y/n)
>   [y] 接受全部 L1 锁,写 docs/00_charter.md §2.5
>   [n] 中断,需手动改 tech_stack.md(重量级偏航,需写偏离项)
```

---

## 四、状态读写协议(强约束)

### 4.1 状态机(单一真源)

```
[ ] ──→ [~] ──→ [x] ⇄ [UNLOCKED] ──→ [x]   (正常流程 + unlock)
                                          
另外两个终态:
[SKIP]                                       (主动跳过,写理由)
[x] LEGACY                                   (历史包袱,试点项目用)
```

**所有合法转移**:
- `[ ] → [~]`:开始干活
- `[~] → [x]`:完成 + 签字
- `[x] → [UNLOCKED]`:发现错了,解锁重做
- `[UNLOCKED] → [~]`:开始重做
- `[UNLOCKED] → [x]`:重做完成,重新锁
- `[ ] → [SKIP]`:判定本 phase 不需要(必须写 `skip_reason`)

**禁止转移**(报 `ERR_INVALID_TRANSITION`):
- `[x] → [~]`(锁了不能直接回退,必须先 [UNLOCKED])
- `[ ] → [x]`(必须经过 [~])
- `[SKIP] → [x]`(需先 [UNLOCKED])
- `[x] LEGACY → 任何`(历史包袱不可改)
- `[UNLOCKED] → [ ]`(避免状态机回退到起点)
- 任何"跳级"如 `[ ] → [UNLOCKED]`

**特殊状态**:
- `[x] LEGACY`:试点项目专用(如旧项目的历史 phase),**只能由 migration 脚本**(在 pm-template 仓库内提供)写入。skill 10 个均无权限设 LEGACY。这是"只读历史包袱"。

### 4.2 唯一写 STATE.md 的 helper

```python
# 位置: pm-template/.claude/scripts/update_state.py
# 13 skill 通过 `from update_state import update_state` 引用
# 路径相对 <pm-template root>,子项目通过 `git submodule` 或 pip 路径解析

def update_state(phase: int, new_status: str, **kwargs):
    """唯一写 STATE.md 的 helper,13 skill 共享。
    
    Args:
        phase: 0|1|2|3|4
        new_status: 6 个合法状态之一
        **kwargs:
            signed_by: str                 # 签字人
            signed_at: str                 # YYYY-MM-DD
            critic_report_path: str        # 相对 <project root>
            dod_count: str                 # "12/12" 格式
            lock_reason: str               # UNLOCKED 时必填
            skip_reason: str               # [SKIP] 时必填
            template_sha: str              # git SHA,锁时记录(版本对齐)
    
    Returns:
        写成功的 STATE.md diff 字符串
    
    Raises:
        ERR_INVALID_TRANSITION: 状态机非法
        ERR_STATE_FILE_CORRUPT: STATE.md 解析失败
        ERR_MISSING_REQUIRED_FIELD: kwargs 缺必填
        ERR_CONCURRENT_WRITE: 文件锁失败
    """
    # 1. 校验 new_status ∈ 6 个合法值
    # 2. 校验 kwargs 必填字段(按 new_status 类型)
    # 3. 读 <cwd>/docs/process/STATE.md + 解析
    # 4. 找 "## Phase {phase}" 段,parse 当前 status
    # 5. 状态机转移校验(对照 §4.1 合法表)
    # 6. 合并 kwargs 到 bullets
    # 7. 原子写(先 .tmp 再 rename + 文件锁 fcntl)
    # 8. 打印 diff 给用户
```

### 4.3 13 skill 与 STATE.md 的关系

| Skill | 读 STATE.md | 写 STATE.md | 走 update_state |
|---|---|---|---|
| new-project | ✓(找起点) | ✗ | — |
| phase-0-charter | ✓(查 [x] 跳过) | ✓(锁时) | ✓ |
| phase-1-requirements | ✓ | ✓ | ✓ |
| phase-2-design | ✓ | ✓ | ✓ |
| phase-3-detail | ✓ | ✓ | ✓ |
| phase-4-implement | ✓ | ✓ | ✓ |
| state | ✓ | ✗ | — |
| critic | ✗ | ✗ | — |
| dod-check | ✗ | ✗ | — |
| unlock | ✓(查状态 + cascade 展示) | ✓(解锁时) | ✓ |

### 4.4 五类门(phase 转移的检查体系)

每个 phase 锁前要过 5 类门,缺一不可。设计目的:**把 LLM 主观打分(critic)和机器机械检查(grep)分开**,失败行为不同,用户能区分"我没勾"vs"前 phase 没挖够"vs"状态不对"。

| 门 | 谁判 | 判什么 | 飘忽度 | 错误码 | 失败行为 |
|---|---|---|---|---|---|
| **1 状态机门** | `update_state.py` | 转移是否合法(如 `[ ]→[x]` 必过 `[~]`) | 0(代码) | `ERR_INVALID_TRANSITION` | 抛异常,不动 STATE.md |
| **2 签字门** | 用户 | "我是否认可这份产物" | 0(用户 y/n) | `ERR_USER_DECLINED` | 用户说 n,exit |
| **3 DoD 门** | LLM + 模板 | "清单上每项是否都做了" | 中(LLM 勾) | `ERR_DOD_INCOMPLETE` | 报告未勾项,可补 |
| **4 Critic 门** | LLM + critic 模板 | "有没有 C/H 级问题" | 高(LLM 主观) | `ERR_CRITIC_HAS_BLOCKING` | C/H 报告路径,必修 |
| **5 硬 grep/anchor 门** | 脚本(grep) | "前 phase 产物是否含必含 anchor" | 0(机器) | `ERR_UPSTREAM_INCOMPLETE` / `ERR_PHASE_1_INCOMPLETE` | **强制回上游 phase unlock** |

**第 5 类门(硬 grep 门)的关键特性**:
- 失败 = 强制回上游 phase unlock(改动 5 落地)
- 不是 phase 内部"修一下",是返工
- 用 anchor 注释(`<!-- ANCHOR: xxx -->`)替代中文字段 grep,防误伤
- 配合第 3 类门(DoD 必填段)使用:DoD 必填段在 critic 跑时再查 grep,启动时再查 grep,**双保险**

**为什么 5 类分开报错误码**(不分"phase X 未通过"):

用户看到错误时,需要区分三种情况:
- "我 DoD 没勾完" → 第 3 类,补
- "我前 phase 没挖够" → 第 5 类,回 phase 1 unlock 重挖
- "我状态机不对" → 第 1 类,技术 bug

混在"phase X 未通过"里,用户不知道该 unlock 1 还是 unlock 2。

### 4.5 第二层状态机:变更日志(`/change` 入口)

5 phase 锁完后,项目进入维护期。对已存在项目做修改的入口是 **`/change <type> <name>`**,与 5 phase **独立**的第二层状态机。

**为什么独立**:变更频繁 + 类型差异大(feature 重 / hotfix 轻)+ 不应 cascade 重跑基础 phase。如果沿用 5 phase 状态机,加 1 个 feature 得 unlock phase 1/2/3/4 全套,代价过大。

**5 个 type**(已实现):

| type | 严格度 | 签字 | 模板 | critic | DoD |
|---|---|---|---|---|---|
| feature | 重(10 项) | 1 + 1 reviewer | `change/feature.md` | `critics/change/feature.md` | `dod/change/feature.md` |
| bugfix | 中(6 项) | 1 人 | `change/bugfix.md` | `critics/change/bugfix.md` | `dod/change/bugfix.md` |
| refactor | 中(7 项) | 1 + 1 reviewer | `change/refactor.md` | `critics/change/refactor.md` | `dod/change/refactor.md` |
| hotfix | 极轻(4 项) | 1 人 | `change/hotfix.md` | `critics/change/hotfix.md` | `dod/change/hotfix.md` |
| doc | 轻(3 项) | 1 人 | `change/doc.md` | `critics/change/doc.md` | `dod/change/doc.md` |

**未实现的 type**(优先级中,触发才扩展):upgrade / perf / migration / deprecation,详见 `docs/process/TODO.md` §1。

**变更日志状态机**(与 5 phase 完全独立):

```
[ ] ──→ [~] ──→ [x]      (正常完成)
              ↘
               [DEPRECATED]   (被新方案替代 / 项目重写)
               [ABORTED]      (讨论后取消)
```

| 状态 | 谁能改 | 含义 |
|---|---|---|
| `[ ]` | 起草人 | 已分配号,未填 |
| `[~]` | 起草人 | 填写中 |
| `[x]` | reviewer(或操作者) | 已签字(代码已合并) |
| `[DEPRECATED]` | 任何 reviewer | 弃用 |
| `[ABORTED]` | 起草人 | 取消 |

**编号规则**:
- NNNN 4 位 0 补,单调递增
- 废弃号(DEPRECATED / ABORTED)不重用
- 系统自动分配,避免人为手写出错

**与 5 phase 状态机的关系**:
- **不重审 5 phase 产物**:已锁 = 已锁
- **不修改 5 phase 文档**:变更 spec 只**引用** phase 文档,不**修改**
- **不在 5 phase 状态机里加变更状态**:避免状态机爆炸(5 phase × 5 状态 + 5 变更 × 3 状态 = 不可读)

**变更 → 5 phase 增量**:变更 [x] 后,user 在对应 phase 文档里**追加**新故事 / 新接口 / 新表(增量),旧内容**不动**。这是手工追加,不是 skill 强制的——若需要强制度,见 TODO §3。

**跨切面**:
- **ADR**:`/decision <title>` 写 `docs/decisions/NNNN-<title>.md`,贯穿项目全程(不是一次性事件)
- **Release log**:变更 [x] 后,在 `docs/releases.md` 追加一行(轻量手工)

详见 `docs/process/TODO.md` 与 `.claude/skills/change.md`。

---

### 4.6 第三层:ADR 入口(`/decision`,spec 早期遗漏,P2 #14 修复加)

**为什么独立**:
- decision ≠ change:决策是"为什么",change 是"做了什么"。一个 change 可能触发 N 个 decision。
- decision 贯穿项目全程(不像 change 是一次性事件),放 5 phase 状态机会污染主流程。

**状态机**(`docs/process/STATE.md` "决策日志" 段):

```
proposed ──→ accepted ──→ deprecated
                ↓
            superseded (被新 ADR 替代)
```

| 状态 | 谁能改 | 含义 |
|---|---|---|
| `proposed` | 起草人 | 起草中,未定 |
| `accepted` | 起草人 / reviewer | 已被项目接受 |
| `deprecated` | 任何人 | 弃用(不再用,但没替代品) |
| `superseded` | 任何人 | 被 #NNNN 替代(必填关联号) |

**`supersede` 流程**:
- 自动创建新 ADR(状态:proposed)
- 在旧 ADR 末尾追加:状态变更 `accepted → superseded by #NNNN (签字: <name> YYYY-MM-DD)`
- 在新 ADR 元信息 "关联决策" 字段填:`supersedes #NNNN`

**与 change / release 关系**:
- decision 不进 STATE.md 主 5 phase 状态机(与 change 一样是独立第二层)
- decision → release log:决策被 supersede 时,在 release log 加一行 ADR 变更说明
- change → decision 反查:某变更被哪些 ADR 驱动(双向链接,见 TODO §3)

### 4.7 第四层:Release 入口(`/release`,spec 早期遗漏,P2 #14 修复加)

**为什么独立**:
- release 是"变更的聚合视图",与变更个体不同
- release log 是审计追溯的关键载体,必须独立

**版本号规范**(`vX.Y.Z`):

| 级别 | 格式 | 场景 | 例 |
|---|---|---|---|
| **Major** | v0 → v1 | 架构级 / 不向后兼容 | v1.0.0 → v2.0.0 |
| **Minor** | v0.0 → v0.1 | 加新能力(feature 变更) | v1.0.0 → v1.1.0 |
| **Patch** | v0.0.0 → v0.0.1 | 修 bug / 文档 / 小重构 | v1.0.0 → v1.0.1 |
| **Suffix** | `-rc.1` / `-beta.2` | 预发布 | v1.0.0-rc.1 |

**`/change → /release` 联动**:
- `/change <type> <name>` 锁 [x] 后,提示用户"是否走 /release 聚合"
- 单变更 → `/release vX.Y.Z --include #NNNN`
- 多变更累计 → 定期(如每周)跑 `/release vX.Y.Z`(聚合所有 [x])

**`docs/releases.md` 文件格式**:
- 首部:模板说明 + BEGIN/END EXAMPLE 段(锁定不删)
- 中间:真实 release 段(按时间倒序)
- 末尾:留空(给未来追加)
- `/release` 写入时**只在 BEGIN/END EXAMPLE 段下方追加**,不动模板说明

**与 ADR 联动**:release 段 `**关联 ADR**:#NNNN` 填对应决策号。

**自动化**(TODO §3):git tag 触发自动写 release log(GitHub Actions)。

---

## 五、资产映射

| Skill 需要的内容 | 来源 | 读写 |
|---|---|---|
| 模板填空 | `docs/process/templates/0X_*.md` | 只读 |
| critic 跑自审 | `docs/process/critics/0X_*.md` | 只读 |
| DoD 勾选 | `docs/process/dod/0X_*.md` | 只读 |
| tech_stack L1 锁 | `docs/process/tech_stack.md` | 只读 |
| STATE.md schema | `docs/process/STATE.md` 模板(只读)+ 实例(项目内可写) | — |

**模板内容怎么拉**:
- 优先读项目本地 `docs/process/templates/0X_*.md`(已用 Use this template 复制过来)
- 若缺失 → 报 `ERR_MISSING_TEMPLATE`,提示从 pm-template GitHub raw 拉:
  - URL pattern: `https://raw.githubusercontent.com/YyItRoad/pm-template/<SHA>/docs/process/templates/0X_*.md`
  - `<SHA>` 默认用项目 `STATE.md` 记录的 `template_sha`(避免拉错版本)
  - 离线(无网络)→ 提示"无法拉,需手动 git submodule add pm-template 补齐"
- 子项目也可以用 `git submodule add YyItRoad/pm-template vendor/pm-template` 把模板资产 pin 在 vendor/

---

## 六、版本管理

### 6.1 单一真源:pm-template git tag = skill 版本

| pm-template tag | docs/process/ | .claude/skills/ |
|---|---|---|
| (无 tag, main) | latest | latest |
| `v1.0` | v1.0 冻结 | v1.0 冻结 |
| `v1.1` | v1.0 + 增量 | v1.0 + 增量 |

### 6.2 子项目版本策略

- **默认**:`Use this template` → 拉 main → rolling 最新
- **稳定**:`Use this template` 选 `v1.0` tag → 锁版本
- **升级**:`git fetch origin + git merge v1.1` 一次性升 skill + 模板 + 文档

### 6.3 版本对齐 warn

**`/state` 启动时** + **每个 phase skill 启动时** 都做版本对齐检查(不只 phase skill 启动时):

```
if <pm-template git SHA> != <STATE.md 记录的 template_sha>:
    提示: "skill 来自 <old SHA>,项目已升级到 <new SHA>,
           本 phase 已 [x] 锁,需 unlock 重跑 critic"
```

**记录位置**: `STATE.md` 每个 phase bullets 末尾加 `template_sha: <SHA>` 一行,首次锁时写入。

**`/state` 的 version 模式**:`/state --audit` 命令扫描所有 phase 的 template_sha,列出过期 phase 清单(给用户决定是否批量 unlock)。

### 6.4 禁止

- ❌ skill 单独走 semver(避免版本分裂)
- ❌ npm/pip 装 skill(无外部依赖)
- ❌ 远程 marketplace(本期不做)

---

## 七、文件结构(终态)

```
pm-template/                           ← 现有结构不变
├── LICENSE
├── README.md
├── .gitignore
├── docs/                              ← 现有
│   ├── process/                       ← 现有(20 文件)
│   │   ├── tech_stack.md
│   │   ├── templates/{00-03}_*.md     ← 4 文件
│   │   ├── dod/{00-04}_*.md           ← 5 文件
│   │   ├── critics/{00,01,02,03a,03b,03c,04}_*.md  ← 7 文件
│   │   ├── critics/reports/.gitkeep
│   │   ├── README.md / STATE.md / CHANGELOG.md
│   └── superpowers/                   ← 现有
│       ├── specs/                     ← 加:本 spec
│       └── plans/                     ← 加:skill 实施 plan
├── .claude/                           ← 新增
    ├── skills/                        ← 新增(13 skill + 1 readme)
    │   ├── README.md
    │   ├── new-project.md
    │   ├── phase-0-charter.md
    │   ├── phase-1-requirements.md
    │   ├── phase-2-design.md
    │   ├── phase-3-detail.md
    │   ├── phase-4-implement.md
    │   ├── state.md
    │   ├── critic.md
    │   ├── dod-check.md
    │   ├── unlock.md
    │   ├── change.md                  ← Batch A 追加
    │   ├── decision.md                ← P2 #14 追加
    │   └── release.md                 ← P2 #14 追加
    └── scripts/                       ← 新增
        ├── update_state.py            ← 共享 helper(§4.2)
        └── migrate_legacy_state.py    ← 写 [x] LEGACY 专用
```

**pm-template 仓库增 18 文件** = 14 (13 skill + 1 skill README) + 1 spec + 1 plan + 2 scripts。

---

## 八、测试策略

| 维度 | 验证方式 | 通过条件 |
|---|---|---|
| **Skill 加载** | 10 个 skill 文件 frontmatter 合规,能被 Claude Code 识别 | `claude` 启动后 `/` 面板列出 10 条 |
| **State helper 单测** | `update_state` 函数 pytest,5 种合法转移 + 3 种非法转移 | 8/8 通过 |
| **happy path 跑通** | 真开 toy 项目,`/new-project` 跑完 5 phase 锁 | 中途无需手工改 STATE.md |
| **failure 跑通** | 故意给 critic 制造 CRITICAL,看是否正确阻塞 | Phase 不锁,STATE.md 不动 |
| **版本对齐 warn** | 升 pm-template 到 v1.1,子项目 git pull,看 skill 是否 warn | warn 触发,用户决定 |

---

## 九、Verification Checklist(实施后签收)

- [ ] 13 skill 文件 frontmatter 合规,被 Claude Code 识别
- [ ] `update_state` helper 8 个 pytest 全过
- [ ] toy 项目 `/new-project` 跑通 Phase 0→4 全部锁
- [ ] critic CRITICAL 时正确阻塞,不锁
- [ ] pm-template 升 tag 后,子项目 pull 触发 version warn
- [ ] pm-template 仓库 push 成功,GitHub 上 `is_template=true` 保持
- [ ] 子项目用 `Use this template` 复制后,`.claude/skills/` 完整跟随

---

## 十、What's Next

- 实施时调用 `writing-plans` skill 出 per-task plan
- Phase 4 skill 涉及实际编码,与 superpowers:subagent-driven-development / tdd-guide 集成(可选,后续细化)
- 未来 skill 数量 > 20 时,考虑拆 plugin marketplace(本期不做)

---

## 十一、错误码目录

| 错误码 | 触发条件 | 行为 | 5 类门归属 |
|---|---|---|---|
| `ERR_INVALID_TRANSITION` | 状态机非法转移(如 [x] → [~]) | 报错 + 提示合法路径 | 1 状态机门 |
| `ERR_STATE_FILE_CORRUPT` | STATE.md parse 失败 | 备份原文件 + 拉空模板 + 提示用户手动迁移 | 1 状态机门 |
| `ERR_MISSING_REQUIRED_FIELD` | kwargs 缺必填字段 | 提示补什么字段 | 1 状态机门 |
| `ERR_CONCURRENT_WRITE` | 文件锁失败(fcntl) | 重试 3 次,失败报错 | 1 状态机门 |
| `ERR_MISSING_TEMPLATE` | 项目本地 + GitHub 都没模板 | 提示手动 `git submodule add` 补齐 | (基础设施) |
| `ERR_VERSION_MISMATCH` | STATE 记录的 template_sha ≠ pm-template 当前 SHA | 提示用户解锁重跑 | (基础设施) |
| `ERR_PHASE_LOCKED_BY_UPSTREAM` | 想改已锁 phase,但上游 [UNLOCKED] | 提示先处理上游 | 1 状态机门 |
| `ERR_CRITIC_HAS_BLOCKING` | critic 报告含 CRITICAL/HIGH,skill 试图锁 | 拒绝锁,显示报告 | 4 Critic 门 |
| `ERR_USER_DECLINED` | 用户在 sign-off 说 n | 不锁,回 phase 末尾问"改什么" | 2 签字门 |
| `ERR_DOD_INCOMPLETE` | DoD 模板里有未勾项 | 列出未勾项,可补 | 3 DoD 门 |
| `ERR_INSUFFICIENT_EXPLORATION` | phase 0/1 挖掘回合 anchor 缺 / 行数不够 | 拒绝进 §4,**回 §3 重挖** | 3 DoD 门(本地) |
| `ERR_OPTIONAL_SECTION_FILLED_BUT_BLANK` | 模板里 [可选] 段挂了标题但内容是占位符 | 提示"删标题 / 写内容"二选一 | 3 DoD 门(本地) |
| `ERR_PHASE_1_INCOMPLETE` | phase 2/3/4 启动时 grep 01 缺 4 anchor | 提示 `/unlock 1` 回去补挖掘证据 | **5 硬 grep 门** |
| `ERR_UPSTREAM_INCOMPLETE` | phase 3/4 启动时 grep 上游缺关键段 | 提示 `/unlock` 对应 phase 补 | **5 硬 grep 门** |
| `ERR_CHANGE_TYPE_INVALID` | `/change <type>` type 不在白名单 | 提示看 `docs/process/TODO.md` 扩展 | 1 状态机门(变更) |
| `ERR_CHANGE_REQUIRES_GREENFIELD` | `/change` 调用但主 5 phase 0 个 [x] | 提示先 `/new-project` | 1 状态机门(变更) |
| `ERR_CHANGE_FILE_EXISTS` | 同号 NNNN-<type>-<name>.md 已存在 | 检查编号 | 1 状态机门(变更) |
| `ERR_RELEASE_VERSION_INVALID` | `/release` 版本号非 vX.Y.Z 格式 | 报格式要求 | 1 状态机门(release) |
| `ERR_RELEASE_DUPLICATE` | 同一版本号已存在 | 提示用 patch 号(0.0.1 → 0.0.2) | 1 状态机门(release) |
| `ERR_RELEASE_NO_CANDIDATES` | `/release` 调用但 0 个 [x] 变更 | 提示"等 /change 锁完再来" | 1 状态机门(release) |

**统一处理**: helper 抛异常时,skill 立即退出 + 展示 traceback 关键 3 行 + 错误码,便于用户排查。

---

## 十二、Sign-off 输入解析

§3.2 sign-off 提示用户输入 `y/n/c`:
- `y` → 解析为 lock,进入 sign 提示:`name?` + `date?(回车默认今天)` → 调 `update_state`
- `n` → 解析为不锁,return 当前 phase 末尾提示"需修改什么?"
- `c` → 解析为展示完整 critic 报告

**name 验证**: 非空,长度 ≤ 50 字符。无格式校验(中文 / 英文 / 数字都可)。
**date 验证**: 必须是 `YYYY-MM-DD` 格式,默认今天(`datetime.date.today().isoformat()`)。

**例**:
```
> [y] 锁
> 请输入签字人姓名: <name>
> 请输入签字日期(YYYY-MM-DD,回车默认今天): [回车]
> 签字: <name> YYYY-MM-DD
> update_state(0, '[x]', signed_by='<name>', signed_at='YYYY-MM-DD', ...) ✓
```

---

## 十三、Phase 4 skill 提示词骨架

`/phase-4-implement` 与其他 phase 不同:写业务代码,不是文档。骨架:

```
1. 读 <cwd>/docs/03b_api_design.md §B 接口清单
2. 读 <cwd>/docs/01_requirements.md §2 故事 + AC
3. 调 TDD 循环:对每接口 写测试 → 实现 → 跑 e2e
4. 跑 dod/04_implementation.md 自检:
   - AC 覆盖率 = e2e 命中 AC 数 / Phase 1 AC 总数
   - 范围蔓延(代码层 grep)
   - 接口一致性(diff @router 装饰器 vs 03b path/method)
   - 反向需求真没做(grep Phase 1 §5)
5. update_state(4, '[x]', ...)
6. 提示"5 phase 全锁,进入维护模式"
```

**与 superpowers 集成**(可选): Phase 4 skill 可调用 subagent-driven-development 派发 TDD 实现子任务,但本期不强制。
