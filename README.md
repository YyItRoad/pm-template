# pm-template

> **Standard 5-phase project management process template + tech stack spec + 13 skills**
> 标准 5 阶段项目管理流程模板 + 技术栈规范 + 13 个 Claude Code skill

## 这是什么 / What is this

一个**可复用资产仓库**,为 **web 应用(后端业务层 + 后台管理 SPA + 关系数据库)** 型项目提供:

- **5 phase 流程** — 立项 / 需求 / 概要设计 / 详细设计 / 实现,每 phase 三件套(模板 + DoD + critic)
- **标准技术栈** — L1/L2/L3 锁级,Phase 0 签字 = 锁
- **13 个 Claude Code skill** — 把流程 + tech_stack 资产从"死的文档"升级为"活的流程引擎"
- **双层验证** — AI critic 自审 + 用户签字

**不是**给单个项目用的脚手架。**是**给所有同类型项目共享的"流程 + 选型 + skill"标准。

---

## 4 个入口

| 用途 | 路径 |
|---|---|
| 流程使用指南 | [`docs/process/README.md`](docs/process/README.md) |
| 标准技术栈规范 | [`docs/process/tech_stack.md`](docs/process/tech_stack.md) |
| 设计 spec | [`docs/superpowers/specs/standard-process-template-design.md`](docs/superpowers/specs/standard-process-template-design.md) / [`standard-tech-stack-design.md`](docs/superpowers/specs/standard-tech-stack-design.md) / [`pm-template-skill-ization-design.md`](docs/superpowers/specs/pm-template-skill-ization-design.md) |
| 13 skills 列表与职责 | [`.claude/skills/README.md`](.claude/skills/README.md) |

---

## 13 个 Skill(分 4 层)

| 层 | 数量 | 职责 |
|---|---|---|
| **入口** | 1 | `new-project` — 串行调度 phase 0→4,首启时调 brainstorming |
| **5 phase** | 5 | `phase-0-charter` / `phase-1-requirements` / `phase-2-design` / `phase-3-detail` / `phase-4-implement` |
| **辅助** | 4 | `state` / `critic` / `dod-check` / `unlock` |
| **维护期 + 跨切面** | 3 | `change` / `decision` / `release` |
| **合计** | **13** | 详见 [`.claude/skills/README.md`](.claude/skills/README.md) |

> **文档与 skill 职责分工**(原则):
> - **skill**(给 Claude Code 执行)只说"做什么 + 错误处理 + 不要做",1 行引用 spec
> - **doc**(给人看)解释"为什么 + 设计取舍 + 关系图",详情装这里
> - skill 描述**不依赖模板项目名**(新项目复制后描述仍准确)

---

## 怎么用(4 步)

### A. 新项目:5 phase 启动

1. **新项目**: GitHub 顶部 → **"Use this template"** → 选 owner/repo → 创建
2. **触发 `/new-project <topic>`**:
   - 自动初始化 `docs/process/STATE.md`(若缺失)
   - 首启时调 `superpowers:brainstorming` 把问题聊透
   - 引导 L1 技术栈锁确认(逐条展示,用户 y/n 接受)
   - 串行调度 phase 0→4,每 phase 末自动跑 DoD + critic + sign-off
3. **每 phase 流程**:
   ```
   模板填空 → 跑 /critic → 跑 /dod-check → 用户 y/n/c 签字 → 锁 [x]
   ```
4. **DoD 编号方案**:每 phase 用全局前缀 `D0-NN` / `D1-NN` / `D2-NN` / `D3-NN` / `D4-NN`,critic 报告可直接引用 `D1-06` 定位

### B. 中途中断与续跑

- **Ctrl+C 中断** → STATE.md 留 `[~]`,下次 `/new-project` 无参模式自动续跑
- **加新 phase / 改产物** → 必先 `/unlock <phase>`,cascade 自动解锁下游 phase

### C. 维护期:变更 / 决策 / 发布

5 phase 锁完后进入维护期。3 个独立入口:

```bash
# 1. /change — 加能力 / 修 bug / 重构(5 type,见下方)
/change feature audit-log         # 加功能
/change bugfix login-401          # 修 bug
/change refactor service-layer    # 重构
/change hotfix db-deadlock        # 紧急修复
/change doc readme-typo           # 文档

# 2. /decision — 架构决策记录(贯穿全程,不像 change 是一次性)
/decision use-fastapi             # 写 ADR
/decision --supersede 0001 ...    # 替代旧决策

# 3. /release — 把 [x] 变更聚合为 1 个版本
/release v0.12.0                  # 聚合所有 [x] 变更 → 写 docs/releases.md
```

变更日志状态机:`[ ]` → `[~]` → `[x]`(独立于 5 phase 状态机)。
未实现的 type(upgrade / perf / migration / deprecation)见 [`docs/process/TODO.md`](docs/process/TODO.md)。

---

## 适用

| ✅ 适用 | ❌ 不适用 |
|---|---|
| Web 应用(后端 + 管理端 SPA + 关系数据库) | CLI / 库 / SDK |
| 单体服务 / 中小规模 | 嵌入式 / 移动端原生 |
| 国内私有化部署 | 全球化 / 多区域部署 |

## 流程示意

```
Phase 0 立项        [ ] ──┐
                          │
Phase 1 需求 ★      [ ] ──┤
                          │
Phase 2 概要设计    [ ] ──┤   每 phase: 模板填空 → critic 自审
                          │              → 勾 DoD → 签字 → 锁
Phase 3 详细设计    [ ] ──┤
                          │
Phase 4 实现+验证   [ ] ──┘
```

> `[ ] = 未开始`,`[x] = 已锁`,`[~] = 进行中`,`[UNLOCKED] = 解锁中`。
> 本仓库自身的 STATE.md 保持空状态(模板仓库不跑流程),具体项目复制后填。

---

## 许可证

MIT — 详见 [LICENSE](LICENSE)
