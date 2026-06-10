# 测试覆盖边界说明

> 本流程模板采用 5 类门(状态机 / 签字 / DoD / Critic / 硬 grep)控制质量。
> 不是所有门都能机械断言 —— 本文档划清**可测 / 不可测**的边界,避免假阳性自信。

## 1. 机械测试覆盖范围(可断言)

`tests/test_skill_redesign_smoke.py` + `tests/test_update_state.py` 覆盖:

| 门 | 是否可测 | 测试文件 | 用例数 |
|---|---|---|---|
| **状态机门** | ✅ 全测 | test_update_state.py | 9 |
| **状态机端到端** | ✅ 全测 | test_skill_redesign_smoke.py | 3 |
| **硬 grep 门(phase 0)** | ✅ 全测 | test_skill_redesign_smoke.py | 3 |
| **硬 grep 门(phase 1)** | ✅ 全测 | test_skill_redesign_smoke.py | 4 |
| **硬 grep 门(phase 2)** | ✅ 全测 | test_skill_redesign_smoke.py | 3 |
| **硬 grep 门(phase 3)** | ✅ 全测 | test_skill_redesign_smoke.py | 4 |
| **[可选] 段占位符检测** | ✅ 全测 | test_skill_redesign_smoke.py | 2 |
| **合计** | | | **28** |

**全量回归**:`python3 -m pytest tests/ -v` → 28 passed

## 2. 不可机械测试(需要人或 LLM 子 agent)

| 门 | 为什么不可测 | 谁负责 |
|---|---|---|
| **签字门** | "用户是否真的 review 过产物"是主观判断 | 用户本人(每 phase 末 y/n/c) |
| **DoD 门** | DoD 是 checklist,需要逐条对照产物确认 | phase skill 引导用户勾选 |
| **Critic 门** | C/H/M/L 评分是 LLM 主观判断 | superpowers:code-reviewer 子 agent 跑 |
| **brainstorming 对话质量** | "问题是否聊透"无法用 grep 验证 | superpowers:brainstorming + 用户 |

这些"软门"由 `docs/process/critics/` 下的 prompt + spec §4.4 文档化,本测试**不**试图覆盖。

## 3. 为什么硬 grep 优先于 critic

- **可重现**:同一输入永远得到同一输出
- **可累加**:每加一个 anchor,断言即可加一条
- **可读**:失败信息直接告诉用户"缺 X anchor",而非"critic 觉得不够好"
- **零 LLM 成本**:跑测试不需要调 API

代价:硬 grep 只挡"形",不挡"神"——用户可以机械地写 20 条"废话"边界场景凑数。
**这个缺口由 critic + brainstorming 补**。

## 4. 端到端 toy 项目(后续工作)

当前测试仅覆盖 state machine + 硬 grep 单元测试,未做"完整跑一遍 5 phase 锁"的端到端 toy 项目验证。
**未来工作**:用 `pm-template` 自己当模板建一个 toy 项目(如"Skill 维护日志系统"),
实际跑 `/new-project` → phase 0/1/2/3/4 全锁,验证文档/skill 描述与实际行为一致。

这一 toy 项目的产物会成为 `/new-project` 的"活文档",帮助新用户对照。
