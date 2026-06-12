---
name: new-project
description: 新建 / 续跑项目入口。初始化 STATE.md(若缺失),首启时调 superpowers:brainstorming 把问题聊透,引导 L1 技术栈锁确认,串行调度 phase 0→4,每个 phase 末自动跑 DoD + critic + sign-off,逐 phase 锁。中途 Ctrl+C 中断后再跑自动续跑(无 <topic> 模式)。维护期用 /change / /decision / /release,不用本 skill。
---

# /new-project <topic> — 项目启动入口

## 用途

项目的**唯一**入口 skill。串行调度 5 个 phase,逐 phase 锁。

**不直接写 STATE.md**(各 phase skill 自己写)。

## 触发

```
/new-project <topic>                       # 启动项目(首启时跑 brainstorming)
/new-project <topic> --skip-brainstorm     # 跳过 brainstorming,直接进 phase 0
/new-project                               # 续跑(无 <topic>,跳过 L1 锁 + brainstorming)
/new-project --status                      # 只看当前进度(等价 /state)
```

`<topic>` 是一句话项目名(如"童账轻管系统"、"订单中台")。可省,纯续跑模式直接跑现状。

**`--skip-brainstorm` 旗标**:用户明确"我已经想清楚了,直接开干"时跳过 brainstorming。**默认仍跑 brainstorming**(因为多数项目 LLM 自由发挥的根源是"对问题理解不够")。即使跳了 brainstorming,phase 0 的"挖掘回合"(机械 3 轮穷举)仍必跑。

## 执行步骤(spec §3.1)

### 1. 初始化 STATE.md(若缺失)

```bash
python3 -c "
import sys
sys.path.insert(0, '.claude/skills/_lib')
from update_state import find_state_file, StateFileCorruptError
try:
    sp = find_state_file()
    print(f'EXISTS: {sp}')
except StateFileCorruptError:
    print('MISSING')
"
```

`MISSING` → 拉空 STATE 模板写到 `<cwd>/docs/STATE.md`:
- 模板路径:`docs/STATE.md`(pm-template 仓库内,**只读格式模板**)
- 用 Read tool 读全文 → Write tool 写到目标 `<cwd>/docs/STATE.md`
- 写完提示:"已初始化 docs/STATE.md,接下来:"

> **架构说明**:`docs/STATE.md` 是 pm-template 内的**格式模板**(只读,定义 5 phase + 变更日志 + 决策日志 段结构);target 项目的 **runtime 状态文件** 在 `docs/STATE.md`,由本步生成,后续 `update_state.py` 原地读写。

`EXISTS` → 解析并显示当前状态(用 `python3 .claude/skills/_lib/update_state.py --check`)。

### 1.5. 调 superpowers:brainstorming(改动 3,★首启时)

**触发条件**:`<topic>` 提供了 + STATE.md 刚初始化(首次启动)。**续跑模式(无 `<topic>` 或已初始化)跳过**。

**触发 Skill tool**:
```
Skill: superpowers:brainstorming
Args: <topic>(原始用户输入)+ <project_root_path>(<cwd>)
```

**brainstorming 跑完后,产出"问题理解"小结**:
- brainstorming 自己可能写 spec/plan 文档(按其内部约定)
- new-project 额外把 1-2 段"问题理解"小结写到 `docs/00_charter.md` 的 `§-1 brainstorming 小结` 段(模板已加这个占位段)
- §-1 内容是"对什么 / 给谁 / 边界 / 已知未知"4 句话,作为 phase 0 挖掘回合的输入

**职责分工(不重复)**:

| 阶段 | 形式 | 目的 |
|---|---|---|
| brainstorming(本步骤) | 对话式 | 把问题聊透(谁 / 什么 / 为何 / 边界 / 已知未知) |
| phase 0 §3 挖掘回合 | 结构化清单 | 3 轮穷举(利益相关方 / 约束 / 非目标) |
| phase 1 §3 挖掘回合 | 结构化清单 | 4 轮穷举(角色×场景 / 边界 / 异常 / 反向) |

**brainstorming 是"对话",挖掘回合是"清单"**。前者补"我还没想清楚的部分",后者强制"把已知的列全"。

**`--skip-brainstorm` 旗标行为**:跳过本步,直接进 §2。但 phase 0 挖掘回合仍必跑(那是机械保证,不靠 brainstorming)。

### 2. 找第一个非 [x] phase

```bash
python3 -c "
import sys
sys.path.insert(0, '.claude/scripts')
from update_state import find_state_file, parse_state, get_current_status
st = parse_state(find_state_file())
for i in range(5):
    s = get_current_status(st[i])
    print(f'Phase {i}: {s}')
"
```

- 全部 `[x]` → 提示"`✅ 5 phase 已全锁,进入维护模式。运行 /state --audit 检查版本对齐`" → exit
- 首个非 `[x]` 是 Phase N → 从 N 开始
- 有 `[UNLOCKED]` → 提示"`⚠️ Phase {N} cascade unlock,需重跑 critic + 签字`" → 从 N 开始
- 有 `[x] LEGACY` → 当 [x] 看待(跳过)

### 3. 引导 L1 技术栈锁确认(spec §3.5)

**只对 Phase 0 跑一次**(其他 phase 触发不重复)。

读 `docs/process/tech_stack.md` §1 锁层级总览,提取所有 L1 锁(🔒 标记):

```
L1-001: Python 3.12+
L1-002: FastAPI 0.115+
L1-003: SQLAlchemy 2.x
L1-004: Pydantic v2
L1-005: bcrypt rounds=12
L1-006: PyJWT (cookie for web, Bearer for AI)
L1-007: Vue 3.5+ Composition API
L1-008: Vite 6+
L1-009: TypeScript 5.6+
L1-010: Element Plus 2.8+
L1-011: Pinia 2.2+
L1-012: Vue Router 4.4+
L1-013: Axios 1.7+
L1-014: MariaDB 10.3+ / MySQL 8.x
L1-015: utf8mb4 / utf8mb4_general_ci
L1-016: InnoDB only
L1-017: snake_case 命名
L1-018: INT AUTO_INCREMENT 主键
L1-019: DECIMAL(10,2) 金额
L1-020: DATETIME 时间字段
L1-021: 显式 idx_*/uk_* 索引
L1-022: Docker + Docker Compose
L1-023: nginx 1.27-alpine
L1-024: .env 环境变量(不入版本控制)
L1-025: pytest + pytest-asyncio + httpx
L1-026: 后端测试 ≥ 80% 覆盖率
L1-027: tests/{unit,integration}/ 组织
... (其他见 tech_stack §2)
```

**展示**:
```
> 读 tech_stack.md §1 锁层级(共 N 条 L1 锁):
>   🔒 L1-001: Python 3.12+
>   🔒 L1-002: FastAPI 0.115+
>   ...
>
> 全部接受? (输入 y/n)
>   [y] 接受全部 L1 锁,准备写 docs/00_charter.md §2.5
>   [n] 中断,需手动改 tech_stack.md(重量级偏航)
```

**`y`** → 把 L1 锁列表写进 `docs/00_charter.md` §2.5(由 Phase 0 skill 接管后填)。

**`n`** → exit,提示"`重量级偏航,需手动编辑 tech_stack.md 后重启 /new-project`"。

### 4. 串行调度 phase 0→4(spec §3.1 步骤 4)

```python
phase_skills = [
    (0, "/phase-0-charter"),
    (1, "/phase-1-requirements"),
    (2, "/phase-2-design"),
    (3, "/phase-3-detail"),
    (4, "/phase-4-implement"),
]

for phase, skill_cmd in phase_skills:
    if state[phase] == "[x]" or state[phase] == "[x] LEGACY":
        continue  # 跳过已锁
    if state[phase] == "[UNLOCKED]":
        print(f"⚠️ Phase {phase} 已 cascade unlock,需重跑")
    # 调对应 phase skill(同会话内,作为子流程)
    invoke_skill(skill_cmd)
    # 重新解析 STATE.md 看是否锁成功
    state = parse_state(find_state_file())
    new_status = get_current_status(state[phase])
    if new_status != "[x]":
        print(f"Phase {phase} 未锁({new_status}),等待用户介入")
        # 退出 /new-project,留给用户处理
        break
```

**`invoke_skill(skill_cmd)`** = 把 phase skill 的执行步骤作为子流程运行(同 Claude Code 会话内,直接按 phase skill 文件的步骤做)。

**注意**:
- Phase N 未成功锁 → 中断 /new-project,提示用户
- 用户 `Ctrl+C` → STATE.md 留 `[~]`,下次 `/new-project` 续

### 5. 全部 [x] → 实施支持模式

```
> ✅ 5 phase 全部锁定!
> Phase 0: [x] by <name> on <date>
> Phase 1: [x] by <name> on <date>
> Phase 2: [x] by <name> on <date>
> Phase 3: [x] by <name> on <date>
> Phase 4: [x] by <name> on <date>
>
> 维护期:
>   - 改文档:用 /state --audit 检版本对齐,unlock 重跑
>   - 改代码:继续按 Phase 4 风格 TDD,新接口必须先 unlock Phase 3
>   - 升 pm-template:git fetch + merge,触发 /state --audit
```

## 关键设计原则

1. **串行不并行**:5 phase 必须顺序,前一 phase 锁是下一 phase 前提(spec §3.1)
2. **用户明示锁**:skill 不替用户锁,每 phase 末问 y/n/c(spec §3.2)
3. **L1 锁一次过**:只在 /new-project 启动时确认一次,phase 0 之后不再问
4. **失败即停**:critic CRITICAL / DoD 缺项 / 用户 n → /new-project 退出,等用户改
5. **可续跑**:Ctrl+C 后 STATE.md 留 [~] 或 [UNLOCKED],下次 /new-project 自动识别
6. **cascade unlock 自动处理**:phase skill 内部触发 /state --audit 提示,不需要 /new-project 介入

## 错误处理

| 错误 | 行为 |
|---|---|
| `ERR_STATE_FILE_CORRUPT` | 备份原文件 + 拉空模板 + 提示用户手动迁移 |
| `ERR_INVALID_TRANSITION` | 上游 phase 未锁,提示先跑上游 |
| `ERR_VERSION_MISMATCH` | pm-template 已升,提示 /state --audit 决定 |
| Phase N 用户 n 锁 | 退出 /new-project,等用户改产物 |
| Phase N critic CRITICAL | phase skill 内部停下,退出 /new-project |
| 用户 Ctrl+C | STATE.md 留 [~] 或 [UNLOCKED],等用户 /new-project 续 |

## 不要做的

- **不默认跳过 §1.5 brainstorming** —— 多数项目 LLM 自由发挥的根源是"对问题理解不够",brainstorming 是定调
- **不把 --skip-brainstorm 设成默认** —— 用户既然跑 /new-project 就该走完整流程;只有用户明确说"跳过"才跳
- **不跳过 phase 0/1 的挖掘回合** —— 即使 brainstorming 跑过,挖掘回合仍必跑(那是机械保证,不靠 brainstorming)
- 不直接调 `update_state()` 写 STATE.md(交给 phase skill)
- 不并行调多个 phase skill(顺序依赖,Phase N 锁是 Phase N+1 前提)
- 不替用户决定 L1 锁接受/偏离(用户必须明示)
- 不在 5 phase 之外新增 phase(锁级 5 = 5)
- 不在 /new-project 内部手动改产物(改产物是各 phase skill 的事)

## 中途加入(无 `<topic>` 或已经初始化过)

```
/new-project         # 续跑,从头扫 STATE.md 找第一个非 [x] phase
```

行为同带 `<topic>` 一致,只是跳过 L1 锁确认(已确认过)。
