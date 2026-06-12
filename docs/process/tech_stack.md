# 标准技术栈规范

> **版本: v1.0**(初版)
> **配套**: [README.md](README.md) · [CHANGELOG.md](CHANGELOG.md)
> **作用**: 把"web 应用 + 后台管理 SPA + 关系数据库"型项目的高频技术选型沉淀为可复用规范,新项目启动直接套用,不再每次重新选

---

## §1 锁层级总览

| 层级 | 标识 | 含义 | 偏离处理 |
|---|---|---|---|
| **L1 必须** | 🔒 | 锁死,项目默认按此执行,Phase 0 签完字就定 | 偏离必须 Phase 0 显式声明 + 走 unlock 流程 |
| **L2 推荐** | 🟡 | 默认按此;偏离需在 Phase 0 / Phase 2 文档中说明理由 | 偏离需文档化理由 |
| **L3 可选** | ⬜ | 项目按需选,不在本规范约束 | 自由选 |

**升级机制**:`tech_stack.md` 独立版本号(v1.0),升级不影响已锁定的项目。新项目按当前最新版锁。

---

## §2 各层栈选型

### §2.1 后端栈

| 类别 | 选型 | 锁级 |
|---|---|---|
| 语言 | Python 3.12+ | 🔒 |
| Web 框架 | FastAPI 0.115+ | 🔒 |
| ASGI server | uvicorn(单进程,MVP) | 🔒 |
| ORM | SQLAlchemy 2.x(同步为主,async 可选) | 🔒 |
| Schema 校验 | Pydantic v2 | 🔒 |
| DB driver | PyMySQL(同步)/ aiomysql(async) | 🟡 |
| 配置 | pydantic-settings + .env(12-factor) | 🔒 |
| 鉴权 | bcrypt(rounds=12)+ PyJWT(JWT cookie for web;Bearer for AI 集成) | 🔒 |
| HTTP 客户端(用于 AI 集成) | httpx | 🟡 |
| 数据库迁移 | 手写 SQL 文件 `sql/migrations/V00N__name.sql`(不引入 Alembic) | 🟡 |
| 日志 | 标准 logging(容器 stdout 收集) | 🟡 |
| 异常体系 | 自建 `ServiceError` 体系 + FastAPI exception_handler 统一包成 `code=500` | 🟡 |

### §2.2 前端栈(Vue 3 管理端 SPA)

| 类别 | 选型 | 锁级 |
|---|---|---|
| 框架 | Vue 3.5+ Composition API | 🔒 |
| 构建 | Vite 6+ | 🔒 |
| 语言 | TypeScript 5.6+ | 🔒 |
| UI 库 | Element Plus 2.8+ | 🔒 |
| 状态 | Pinia 2.2+ | 🔒 |
| 路由 | Vue Router 4.4+ | 🔒 |
| HTTP | Axios 1.7+ | 🔒 |
| 按需加载 | unplugin-vue-components + unplugin-auto-import(Element Plus 自动导入) | 🟡 |
| 图标 | @element-plus/icons-vue | 🟡 |
| 测试 | Vitest 2.1+ + happy-dom(**仅逻辑测试,不写组件测试**) | 🟡 |
| Lint | ESLint + Prettier(项目级,不在本规范强制) | ⬜ |

### §2.3 数据层

| 类别 | 选型 | 锁级 |
|---|---|---|
| 数据库 | MariaDB 10.3+ / MySQL 8.x | 🔒 |
| 字符集 | utf8mb4 / utf8mb4_general_ci | 🔒 |
| 存储引擎 | InnoDB only | 🔒 |
| 命名 | snake_case | 🔒 |
| 主键 | INT AUTO_INCREMENT(统一 `id`,不用 `user_id` / `rel_id` / `budget_id` 前缀) | 🔒 |
| 金额 | DECIMAL(10,2),永不用 FLOAT | 🔒 |
| 时间 | DATETIME(`CURRENT_TIMESTAMP` / `ON UPDATE CURRENT_TIMESTAMP`) | 🔒 |
| 软删 | 不用(用 `*_time` + `*_user_id` 字段审计) | 🟡 |
| 索引 | 显式声明,命名 `idx_*` / `uk_*` | 🔒 |
| 外键 | 应用层校验,不强制声明 | 🟡 |

### §2.4 部署 / DevOps

| 类别 | 选型 | 锁级 |
|---|---|---|
| 容器 | Docker + Docker Compose | 🔒 |
| 反向代理 | nginx 1.27-alpine | 🔒 |
| 后端 | uvicorn 单进程(MVP) | 🔒 |
| 前端镜像 | multi-stage:`node:22-alpine` build → `nginx:1.27-alpine` serve | 🟡 |
| CI | GitHub Actions(basic build + test) | 🟡 |
| 触发部署 | `v*` tag push 触发 Actions | 🟡 |
| 镜像仓库 | 项目自选(阿里云 / DockerHub / GHCR) | ⬜ |
| 网络 | Docker 自定义网络模式(项目自定名) | ⬜ |
| 环境变量 | .env 文件(env 注入容器,不入版本控制) | 🔒 |
| HTTPS | 部署在反代后,具体方案项目自定 | 🟡 |

### §2.5 测试策略

| 类别 | 选型 | 锁级 |
|---|---|---|
| 后端单测 / 集成 | pytest + pytest-asyncio + httpx(AsyncClient) | 🔒 |
| 前端单测 | vitest + happy-dom(**仅核心逻辑,不写 Vue 组件测试**) | 🟡 |
| E2E | shell 脚本 `scripts/e2e_*.sh`(call 函数 + `__NOAUTH__` / `__ANY__` 哨兵) | 🟡 |
| 覆盖率 | 后端 ≥ 80%,前端无强制 | 🟡 |
| 测试组织 | `tests/{unit,integration}/test_*.py` | 🟡 |

---

## §3 命名 / 接口 / 错误码约定

| 项 | 规范 | 锁级 |
|---|---|---|
| 用户 ID 命名 | 统一 `user_id` / `parent_user_id` / `child_user_id`,**不用** `admin_user_id` 别名 | 🔒 |
| 时间字段 | `*_time` / `*_at`(DATETIME) | 🔒 |
| 操作人字段 | `*_user_id` / `*_by`(INT FK→user.id) | 🔒 |
| 金额 | Pydantic schema 用 `str`(decimal),JS 端无精度问题 | 🔒 |
| API 风格 | GET 查询 / POST 变更 / PATCH 局部更新 | 🔒 |
| 响应统一包 200 | 业务码走 `body.code`,HTTP 状态码永远是 200 | 🔒 |
| 错误码 | `200 / 400 / 401 / 403 / 404 / 409 / 500` | 🔒 |
| 鉴权双轨(若项目含 AI 集成) | 老 webhook Bearer + 新管理端 JWT cookie(httpOnly + samesite=lax) | 🟡 |

---

## §4 反向约束(Don'ts,容易 AI 自由发挥偷偷加的)

| 禁止项 | 常见诱因 |
|---|---|
| ❌ Websocket / SSE 实时推送 | "多端数据同步焦虑" |
| ❌ 群组 / 家庭组 / 圈子 | "多家庭场景想象" |
| ❌ 多账户 / 多币种 | "理财功能联想" |
| ❌ 通知 / 提醒 / 推送 | "产品完整性" |
| ❌ 多层级权限(超管 vs 普通) | "权限管理想象" |
| ❌ Token 刷新机制 | "用户体验想象" |
| ❌ `audit_log` 表 | "合规要求想象" |
| ❌ 拆 `parent_user` / `admin_user` / `child_user` 多表 | "角色独立想象" |
| ❌ Alembic 自动迁移 | "工程化想象"(标准栈用手写 SQL 迁移) |

---

## §5 后端分层架构 + 职责/约束(🔒 强约束)

> AI 自由发挥最常踩的坑就是"胖 API 层"(业务逻辑全写在 route 函数里)或"漏 service 层"(API 直接查 DB)。本节强制 4 层架构 + 单一职责。

### §5.1 4 层架构(强制)

```
┌─────────────────────────────────────────────────────────────┐
│ API 层  app/api/  app/admin_api/   (HTTP 唯一入口)         │
│   - FastAPI router 定义                                       │
│   - 入参校验(Pydantic schema 解析)                           │
│   - 鉴权依赖注入(require_role / require_coparent_of /         │
│     require_admin_jwt)                                       │
│   - 调 service 函数,无业务逻辑                               │
│   - 异常 → 业务码 翻译(统一 _helpers.ok / from_service)       │
└──────────────────────┬──────────────────────────────────────┘
                       │ 调用
┌──────────────────────▼──────────────────────────────────────┐
│ Service 层  app/services/  (业务逻辑中枢,纯函数)            │
│   - 业务规则实现(余额核算、状态流转、约束校验)               │
│   - 接 db: Session 参数(不持有,不创建)                      │
│   - 抛 ServiceError 体系(NotFound / Conflict /                │
│     PermissionDenied / InvalidParam)                         │
│   - 同事务:INSERT income + UPDATE budget.balance += amount    │
│   - 接原生类型 + ORM 对象,绝不接 Pydantic schema              │
│   - 返 ORM 对象 / 原生类型(不返 Pydantic)                    │
└──────────────────────┬──────────────────────────────────────┘
                       │ 用
┌──────────────────────▼──────────────────────────────────────┐
│ Model 层  app/models/  (ORM,表结构单一真源)                │
│   - SQLAlchemy 2.x 模型                                      │
│   - 定义 relationship / property                            │
│   - 不写业务方法                                             │
│   - 不写事务边界                                             │
└──────────────────────┬──────────────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────────────┐
│ Schema 层  app/schemas/  (DTO,只做校验/序列化)              │
│   - Pydantic v2 schema                                       │
│   - 字段约束(min / max / regex)                              │
│   - 金额字段用 str(decimal)                                  │
│   - 不写业务逻辑                                             │
│   - 不引用 db session                                        │
└─────────────────────────────────────────────────────────────┘
```

### §5.2 跨层公共

| 位置 | 职责 | 不允许 |
|---|---|---|
| `app/deps.py` | FastAPI Depends(鉴权依赖、`get_session`) | 业务逻辑 |
| `app/security.py` | bcrypt + JWT 工具函数(hash / verify / create / decode) | 业务逻辑 |
| `app/main.py` | app 装配、router 挂载、exception_handler 全局异常 → code=500 | 业务逻辑 |
| `app/config.py` | pydantic-settings 读 .env(env 化所有可调参数) | 业务逻辑 |

### §5.3 异常体系(强制)

```python
# app/services/errors.py
class ServiceError(Exception):
    code: int  # 业务码 400/401/403/404/409
    msg: str

class NotFoundError(ServiceError): code = 404
class ConflictError(ServiceError): code = 409
class PermissionDeniedError(ServiceError): code = 403
class InvalidParamError(ServiceError): code = 400
```

- **Service 层只抛 ServiceError 子类**,不抛 HTTPException、不返业务码字面量
- **API 层统一翻译**(`_helpers.from_service`):捕 ServiceError → 返 `{code, msg, data: {}}`
- **未捕获异常** → main.py 的 `exception_handler` → 统一包成 `code=500`(SQLAlchemy 错误 / 编程错误都走这条)
- **HTTP 状态码永远是 200**,业务码走 `body.code`

### §5.4 强制约束(Don'ts)

- ❌ API 层调 `db.query(...)` 直接查 DB(必须经 service)
- ❌ API 层写业务计算、if 状态判断
- ❌ Service 层接 Pydantic schema(只接原生类型 + ORM 对象)
- ❌ Service 层返 Pydantic schema(只返 ORM 对象或原生 dict)
- ❌ Service 层持有 db session(只接参数,不创建)
- ❌ 跨 service 互调(只能主 service 编排子 service,避免循环依赖)
- ❌ 在 Model 上写业务方法(model 只承载数据 + relationship)
- ❌ 业务逻辑写在 `main.py`(只能装配 + 异常处理)
- ❌ 抛 `HTTPException`(统一走 ServiceError 体系)

### §5.5 单一文件职责(🟡 推荐,项目自定)

| 文件 | 行数上限(建议) | 触发拆分的信号 |
|---|---|---|
| `app/api/<name>.py` | ≤ 200 | 同一资源有 3+ 端点 → 拆 `*_admin.py` / `*_view.py` |
| `app/services/<name>.py` | ≤ 300 | 出现 2 个独立业务域(如 income + expense)→ 拆 |
| `app/models/<name>.py` | ≤ 100 | 多对多关系交叉复杂 → 拆中间表单独文件 |
| `app/schemas/<name>.py` | ≤ 300 | 一文件 > 5 个 schema 类,按业务域拆 |

---

## §6 开发 / 运行环境

| 类别 | 选型 | 锁级 |
|---|---|---|
| 后端依赖管理 | venv 隔离,**不全局 pip install** | 🔒 |
| 开发期后端 | uvicorn 本地启动,**不构建 Docker** | 🟡 |
| 前端 dev server | `npm run dev`(Vite dev 代理 `/api` → 后端) | 🟡 |
| 本地数据库 | 项目自定(常用 Docker 容器) | 🟡 |
| 提交信息 | Conventional Commits(feat / fix / refactor / docs / test / chore) | 🔒 |
| 代码风格 | 后端: black + ruff;前端: prettier + eslint(项目级) | 🟡 |

---

## §7 偏航 / Unlock 流程

```
Phase 0 签字(§2.5 锁生效)
   │
   ▼
Phase 2 / 3 / 4 发现需偏航
   │
   ├─→ 1. 在 STATE.md 把 Phase 0 状态从 [x] 改为 [UNLOCKED] + 写解锁原因
   │
   ├─→ 2. 必须同步处理 5 项下游:
   │     - Phase 1 故事是否仍有效(若有接口能力变化,回写 §2 故事)
   │     - Phase 2 接口清单是否需调整
   │     - Phase 3 流程 / 接口 / DDL 是否需调整
   │     - Phase 0 章程 §2.5 偏航项更新
   │     - critic 报告追加新检查项
   │
   ├─→ 3. 跑 critic 重新自审 → 用户重签字
   │
   └─→ 4. 状态回 [x] + 在 STATE.md 记录"解锁 → 重锁"全过程
```

### §7.1 轻量级 vs 重量级偏离

| 级别 | 范围 | 处理 |
|---|---|---|
| **轻量级** | L3 范围内的子选择(如"用 happy-dom 而不是 jsdom"、选具体 L3 库) | 不需要 unlock,Phase 0/2 文档补 1 句说明即可 |
| **重量级** | L1/L2 改动(如"放弃 FastAPI 改 Django"、引入新 L1 库) | 必须走上面 4 步 unlock |

---

## §8 版本管理

- `tech_stack.md` 顶部标 `**版本: v1.0**`(当前)
- 每次升级大改 → version bump(v1.0 → v2.0)
- `docs/process/CHANGELOG.md` 记"v2 改了什么 + 为什么 + 旧项目如何过渡"
- **升级不影响已锁定的项目** —— 旧项目按当时的 v0.1 / v1.0 锁,新 v2 发布后仍生效;只有新项目用最新 v 锁

---

## §9 适用范围与不适用范围

| 适用 | 不适用 |
|---|---|
| Web 应用(后端业务层 + 后台管理 SPA + 关系数据库) | CLI 工具 / 库 / SDK |
| 单体服务 / 微服务雏形 | 嵌入式 / 移动端原生 |
| 中小规模(用户 < 100 万,流量 < 10 万 QPS) | 超大规模(需要专门架构评审) |
| 国内私有化部署 / 单服起步 | 全球化 / 多区域部署 |

**不进标准栈**的项(各项目按需选):
- AI 智能体层(豆包 / OpenAI / Claude / 自研)→ 项目级选型
- 具体云厂商(阿里云 / 腾讯云 / AWS)→ 项目级选型
- 监控 / 链路追踪 / 备份 → 项目级选型
- i18n / a11y → 项目级选型
