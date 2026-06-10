# pm-template Skill 化 — 设计 spec

> **状态**: ✅ 设计已批准,待实施
> **目的**: 把 pm-template 的 5-phase 流程 + tech_stack 资产做成 Claude Code skill,从"死的文档"升级为"活的流程引擎"
> **范围**: 9 skill(1 入口 + 5 phase + 3 辅助)+ 1 共享状态 helper + 跨项目版本管理
> **关联 spec**: [standard-process-template-design.md](standard-process-template-design.md) · [standard-tech-stack-design.md](standard-tech-stack-design.md)

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

### 2.1 9 Skill 总览

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
```

### 2.2 9 Skill 职责矩阵

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

### 2.3 关键约束

- skill 写 STATE.md **必须**走唯一 helper `update_state()`(避免格式漂移 + 并发覆盖)
- 9 skill **只读** `docs/process/templates/` `dod/` `critics/` `tech_stack.md`(不修改模板)
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
3. 展示 tech_stack.md §1 锁层级,确认 L1 锁
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

---

## 四、状态读写协议(强约束)

### 4.1 唯一写 STATE.md 的 helper

```python
def update_state(phase: int, new_status: str, **kwargs):
    """唯一写 STATE.md 的 helper,9 skill 共享。
    
    Args:
        phase: 0|1|2|3|4
        new_status: [ ]| [~] | [x] | [SKIP] | [UNLOCKED] | [x] LEGACY
        **kwargs: signed_by, signed_at, critic_report_path, 
                 dod_count, lock_reason, template_sha
    """
    # 1. 读 <cwd>/docs/process/STATE.md
    # 2. 找到 "## Phase {phase}" 段,parse 当前 bullets
    # 3. 校验状态机:
    #    [x] → [UNLOCKED] 允许
    #    [ ] → [~] → [x] 允许
    #    [SKIP] / [x] LEGACY → [x] 需走 unlock
    #    其他报 ERR_INVALID_TRANSITION
    # 4. 合并 kwargs 到 bullets
    # 5. 原子写(先 .tmp 再 rename)
    # 6. 打印 diff 给用户确认
```

### 4.2 状态机

```
[ ] ──→ [~] ──→ [x]    (正常流程)
                      ↓
                  [UNLOCKED] ──→ [x]  (unlock 后重锁)
                  [SKIP]      (跳过,需写理由)
                  [x] LEGACY  (试点历史包袱)
```

**禁止转移**:
- `[x] → [~]`(锁了不能回退到进行中,必须先 UNLOCK)
- `[ ] → [x]`(必须经过 [~])
- `[SKIP] → [x]`(需先 [UNLOCKED])

### 4.3 9 skill 与 STATE.md 的关系

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
- 若缺失 → 报 ERR_MISSING_TEMPLATE,提示从 pm-template GitHub raw 拉

---

## 六、版本管理

### 6.1 单一真源:pm-template git tag = skill 版本

| pm-template tag | skill 版本 | docs/process/ | .claude/skills/ |
|---|---|---|---|
| (无 tag, main) | rolling | latest | latest |
| `v1.0` | v1.0 | v1.0 冻结 | v1.0 冻结 |
| `v1.1` | v1.1 | v1.0 + 增量 | v1.0 + 增量 |

### 6.2 子项目版本策略

- **默认**:`Use this template` → 拉 main → rolling 最新
- **稳定**:`Use this template` 选 `v1.0` tag → 锁版本
- **升级**:`git fetch origin + git merge v1.1` 一次性升 skill + 模板 + 文档

### 6.3 版本对齐 warn

每个 phase skill 启动时:

```
if <pm-template git SHA> != <STATE.md 记录的 template_sha>:
    提示: "skill 来自 <old SHA>,项目已升级到 <new SHA>,
           本 phase 已 [x] 锁,需 unlock 重跑 critic"
```

**记录位置**: `STATE.md` 每个 phase bullets 末尾加 `template_sha: <SHA>` 一行,首次锁时写入。

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
│   ├── process/                       ← 现有
│   └── superpowers/                   ← 现有
│       ├── specs/                     ← 加:本 spec
│       └── plans/                     ← 加:skill 实施 plan
└── .claude/                           ← 新增
    └── skills/                        ← 新增
        ├── new-project.md
        ├── phase-0-charter.md
        ├── phase-1-requirements.md
        ├── phase-2-design.md
        ├── phase-3-detail.md
        ├── phase-4-implement.md
        ├── state.md
        ├── critic.md
        └── dod-check.md
```

**pm-template 仓库增 11 文件** = 9 skill + 1 spec + 1 plan。

---

## 八、测试策略

| 维度 | 验证方式 | 通过条件 |
|---|---|---|
| **Skill 加载** | 9 个 skill 文件 frontmatter 合规,能被 Claude Code 识别 | `claude` 启动后 `/` 面板列出 9 条 |
| **State helper 单测** | `update_state` 函数 pytest,5 种合法转移 + 3 种非法转移 | 8/8 通过 |
| **happy path 跑通** | 真开 toy 项目,`/new-project` 跑完 5 phase 锁 | 中途无需手工改 STATE.md |
| **failure 跑通** | 故意给 critic 制造 CRITICAL,看是否正确阻塞 | Phase 不锁,STATE.md 不动 |
| **版本对齐 warn** | 升 pm-template 到 v1.1,子项目 git pull,看 skill 是否 warn | warn 触发,用户决定 |

---

## 九、Verification Checklist(实施后签收)

- [ ] 9 skill 文件 frontmatter 合规,被 Claude Code 识别
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
