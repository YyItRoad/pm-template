# pm-template Skills

> 9 个 Claude Code skill,把 pm-template 的 5-phase 流程 + tech_stack 资产从"死的文档"升级为"活的流程引擎"。
> 设计 spec: [`docs/superpowers/specs/pm-template-skill-ization-design.md`](../../docs/superpowers/specs/pm-template-skill-ization-design.md)

---

## 9 Skill 一览

| # | Skill | 触发命令 | 职责 | 写 STATE.md |
|---|---|---|---|---|
| 1 | `new-project.md` | `/new-project <topic>` | 入口,串行调度 phase 0→4 | 不直接写 |
| 2 | `phase-0-charter.md` | `/phase-0-charter` | 立项:§1-§6 + §2.5 stack 签字 | 写 [x] Phase 0 |
| 3 | `phase-1-requirements.md` | `/phase-1-requirements` | 需求:故事/AC/边界 + critic | 写 [x] Phase 1 |
| 4 | `phase-2-design.md` | `/phase-2-design` | 概要设计:架构/数据/接口清单 | 写 [x] Phase 2 |
| 5 | `phase-3-detail.md` | `/phase-3-detail` | 详细设计:拆 3a/3b/3c + 3 critic | 写 [x] Phase 3 |
| 6 | `phase-4-implement.md` | `/phase-4-implement` | 实现:写代码 + e2e + DoD 末条 AC 覆盖 | 写 [x] Phase 4 |
| 7 | `state.md` | `/state` | 读 STATE.md,渲染当前 phase + 建议下一步 | 只读 |
| 8 | `critic.md` | `/critic <phase>` | 单跑 critic 模板,产报告存档 | 不写 |
| 9 | `dod-check.md` | `/dod-check <phase>` | 单跑 DoD 勾选,缺啥报啥 | 不写 |

## 推荐工作流

```
/new-project <topic>          ← 唯一入口,启动项目
                                │
                                ▼ (内部按需调用)
/phase-0-charter
/phase-1-requirements
/phase-2-design
/phase-3-detail
/phase-4-implement
                                │
                                ▼ 任何 phase 末尾可查进度
/state                         ← 读 STATE.md 渲染进度
/state --audit                 ← 跨 phase 检查 template_sha 过期

辅助(任何时机单跑):
/critic <phase>                ← 单跑 critic 模板
/dod-check <phase>             ← 单跑 DoD 勾选
```

## 关键约束(所有 skill 遵守)

- **写 STATE.md 必须走唯一 helper `update_state()`**(9 skill 共用,见 `scripts/update_state.py`)。
- **只读** `docs/process/templates/` `dod/` `critics/` `tech_stack.md` 资产,不修改模板本身。
- **每个 phase 锁前必须 sign-off**:用户明示 `y/n/c`,skill 不替用户锁(详 spec §3.2 / §12)。
- **启动时做版本对齐检查**:`/state` + 每 phase skill 启动时,对比 `STATE.md` 记录的 `template_sha` vs pm-template git SHA,不一致就 warn(详 spec §6.3)。

## 错误码(统一)

- `ERR_INVALID_TRANSITION` — 状态机非法转移
- `ERR_STATE_FILE_CORRUPT` — STATE.md parse 失败
- `ERR_MISSING_REQUIRED_FIELD` — kwargs 缺必填
- `ERR_CONCURRENT_WRITE` — 文件锁失败(fcntl)
- `ERR_MISSING_TEMPLATE` — 项目本地 + GitHub 都没模板
- `ERR_VERSION_MISMATCH` — template_sha 过期
- `ERR_PHASE_LOCKED_BY_UPSTREAM` — 上游 [UNLOCKED],下游不能直接动
- `ERR_CRITIC_HAS_BLOCKING` — critic 报告含 CRITICAL/HIGH,拒绝锁

完整说明见 [spec §11](../docs/superpowers/specs/pm-template-skill-ization-design.md#十一错误码目录)。

## 资产来源

| 需要的内容 | 路径(项目本地) | 缺失时 fallback |
|---|---|---|
| 模板填空 | `docs/process/templates/0X_*.md` | `https://raw.githubusercontent.com/YyItRoad/pm-template/<SHA>/docs/process/templates/0X_*.md` |
| critic 模板 | `docs/process/critics/0X_*.md` | 同上,改 `critics/` 段 |
| DoD 勾选 | `docs/process/dod/0X_*.md` | 同上,改 `dod/` 段 |
| tech_stack L1 锁 | `docs/process/tech_stack.md` | 同上 |

`<SHA>` 默认用项目 `STATE.md` 记录的 `template_sha`(避免拉错版本)。
