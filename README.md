# pm-template

> **Standard 5-phase project management process template + tech stack spec**
> 标准 5 阶段项目管理流程模板 + 技术栈规范

## 这是什么 / What is this

pm-template 是一个**可复用资产仓库**,为 **web 应用(后端业务层 + 后台管理 SPA + 关系数据库)** 型项目提供:

- **5 phase 流程** — 立项 / 需求 / 概要设计 / 详细设计 / 实现,每 phase 三件套(模板 + DoD + critic)
- **标准技术栈** — L1/L2/L3 锁级,Phase 0 签字 = 锁
- **双层验证** — AI critic 自审 + 用户签字

**不是**给单个项目用的脚手架。**是**给所有同类型项目共享的"流程 + 选型"标准。

## 3 个入口

| 用途 | 路径 |
|---|---|
| 流程使用指南 | [`docs/process/README.md`](docs/process/README.md) |
| 标准技术栈规范 | [`docs/process/tech_stack.md`](docs/process/tech_stack.md) |
| 设计 spec | [`docs/superpowers/specs/standard-process-template-design.md`](docs/superpowers/specs/standard-process-template-design.md) / [`standard-tech-stack-design.md`](docs/superpowers/specs/standard-tech-stack-design.md) |

## 怎么用

1. **新项目**: GitHub 顶部 → **"Use this template"** → 选 owner/repo → 创建
2. **初始化**: 把 `docs/process/templates/0X_*.md` 复制到新项目的 `docs/0X_*.md`,按模板填空
3. **Phase 0 签字**: 填 `docs/00_charter.md` §2.5,引用 [`docs/process/tech_stack.md`](docs/process/tech_stack.md) 选标准栈
4. **走完 5 phase**: 每 phase 完成 → 跑 critic → 勾 DoD → 签字 → 锁

## 适用

| ✅ 适用 | ❌ 不适用 |
|---|---|
| Web 应用(后端 + 管理端 SPA + 关系数据库) | CLI / 库 / SDK |
| 单体服务 / 中小规模 | 嵌入式 / 移动端原生 |
| 国内私有化部署 | 全球化 / 多区域部署 |

## 流程示意

```
Phase 0 立项        [x] ──┐
                          │
Phase 1 需求 ★      [x] ──┤
                          │
Phase 2 概要设计    [x] ──┤   每 phase: 模板填空 → critic 自审
                          │              → 勾 DoD → 签字 → 锁
Phase 3 详细设计    [x] ──┤
                          │
Phase 4 实现+验证   [x] ──┘
```

## 许可证

MIT — 详见 [LICENSE](LICENSE)
