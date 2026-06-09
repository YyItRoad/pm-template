# 标准技术栈规范 — 设计 spec

> **状态**: ✅ 设计已批准,待实施
> **来源**: KidBudget 项目 5-phase 流程试点基础上,把已验证的技术选型抽象成可复用的"标准栈规范"
> **目标仓库**: `pm-template`(GitHub: [YyItRoad/pm-template](https://github.com/YyItRoad/pm-template))
> **关联 spec**: [standard-process-template-design.md](standard-process-template-design.md)(5 phase 流程模板)

---

## 一、Context(为什么做)

### 1.1 痛点

KidBudget 项目已完成 5-phase 流程试点,确认流程本身能跑通(模板 + DoD + critic + DoD 签字)。但试点同时暴露一个新问题:**技术选型每次都从零开始**,AI 自由发挥 / 用户临场决策,容易选错、选偏、临时凑合。

具体表现:
- 同一类项目(后端 + 管理端 SPA + 关系数据库)反复出现"Python 3.11 还是 3.12?FastAPI 还是 Flask?Vue 3 还是 React?Element Plus 还是 Ant Design?"之类的无意义决策疲劳
- 偏离标准的最常见原因不是"项目特殊",而是"AI 不知道项目历史选型,按训练数据默认给一套"
- 选型错误通常要等到部署 / 性能出问题才被发现,代价高

### 1.2 目标

把"web 应用 + 后台管理 SPA + 关系数据库"型项目的高频技术选型**沉淀成可复用规范**,新项目启动时直接套用,不再每次重新选。

- **不重新选**的占比目标: ≥ 80%(L1 锁层 + L2 推荐 + 部分 L3 默认)
- **必须说明偏离理由**的范围: L1 + L2(占总规范 70% 左右)
- **完全自由**的范围: L3(剩下 30%)

### 1.3 适用范围与不适用范围

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

---

## 二、设计总览(锁层级)

**目标**: 任何"web 应用 + 后台管理 SPA"型项目启动时,直接套用本规范,不需要每次重新做技术选型。栈选错的概率降到接近 0。

### 2.1 锁层级(中等锁定,3 层)

| 层级 | 标识 | 含义 | 偏离处理 |
|---|---|---|---|
| **L1 必须** | 🔒 | 锁死,项目默认按此执行,Phase 0 签完字就定 | 偏离必须 Phase 0 显式声明 + 走 unlock |
| **L2 推荐** | 🟡 | 默认按此;偏离需在 Phase 0 / Phase 2 文档中说明理由 | 偏离需文档化理由 |
| **L3 可选** | ⬜ | 项目按需选,不在本规范约束 | 自由选 |

### 2.2 存放位置与引用关系

- **规范本体**: `docs/process/tech_stack.md`(独立成文,本 spec 实施产物)
- **引用方**: `docs/process/templates/00_charter.md` 加 §2.5 "技术栈确认" 段,签字 = 锁
- **下游约束**: `docs/process/{dod,critics}/` 多处加 stack 检查项(见 §3)
- **升级机制**: 见 §5,`tech_stack.md` 独立版本号,不影响已锁定的项目

---

## 三、完整技术栈内容(按层)

### 3.1 后端栈

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

### 3.2 前端栈(Vue 3 管理端 SPA)

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

### 3.3 数据层

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

### 3.4 部署 / DevOps

| 类别 | 选型 | 锁级 |
|---|---|---|
| 容器 | Docker + Docker Compose | 🔒 |
| 反向代理 | nginx 1.27-alpine | 🔒 |
| 后端 | uvicorn 单进程(MVP) | 🔒 |
| 前端镜像 | multi-stage:`node:22-alpine` build → `nginx:1.27-alpine` serve | 🟡 |
| CI | GitHub Actions(basic build + test) | 🟡 |
| 触发部署 | `v*` tag push 触发 Actions | 🟡 |
| 镜像仓库 | 阿里云容器镜像服务 | ⬜ |
| 网络 | Docker `kbnet` / `local-network` 模式 | ⬜ |
| 环境变量 | .env 文件(env 注入容器,不入版本控制) | 🔒 |
| HTTPS | 暂不引入,部署在宝塔反代后即可 | 🟡 |

### 3.5 测试策略

| 类别 | 选型 | 锁级 |
|---|---|---|
| 后端单测 / 集成 | pytest + pytest-asyncio + httpx(AsyncClient) | 🔒 |
| 前端单测 | vitest + happy-dom(**仅核心逻辑,不写 Vue 组件测试**) | 🟡 |
| E2E | shell 脚本 `scripts/e2e_*.sh`(call 函数 + __NOAUTH__ 哨兵) | 🟡 |
| 覆盖率 | 后端 ≥ 80%,前端无强制 | 🟡 |
| 测试组织 | `tests/{unit,integration}/test_*.py` | 🟡 |

### 3.6 命名 / 接口 / 错误码约定

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

### 3.7 反向约束(Don'ts,容易 AI 自由发挥偷偷加的)

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

### 3.8 开发 / 运行环境

| 类别 | 选型 | 锁级 |
|---|---|---|
| 后端依赖管理 | venv 隔离,**不全局 pip install** | 🔒 |
| 开发期后端 | uvicorn 本地启动,**不构建 Docker** | 🟡 |
| 前端 dev server | `npm run dev`(Vite dev 代理 `/api` → 后端) | 🟡 |
| 本地数据库 | Docker `mysql8` 容器(MySQL 8.4.6,端口 3308) | 🟡 |
| 提交信息 | Conventional Commits(feat / fix / refactor / docs / test / chore) | 🔒 |
| 代码风格 | 后端: black + ruff;前端: prettier + eslint(项目级) | 🟡 |

### 3.9 后端分层架构 + 职责/约束(🔒 强约束)

> AI 自由发挥最常踩的坑就是"胖 API 层"(业务逻辑全写在 route 函数里)或"漏 service 层"(API 直接查 DB)。本节强制 4 层架构 + 单一职责。

#### 3.9.1 4 层架构(强制)

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

#### 3.9.2 跨层公共

| 位置 | 职责 | 不允许 |
|---|---|---|
| `app/deps.py` | FastAPI Depends(鉴权依赖、`get_session`) | 业务逻辑 |
| `app/security.py` | bcrypt + JWT 工具函数(hash / verify / create / decode) | 业务逻辑 |
| `app/main.py` | app 装配、router 挂载、exception_handler 全局异常 → code=500 | 业务逻辑 |
| `app/config.py` | pydantic-settings 读 .env(env 化所有可调参数) | 业务逻辑 |

#### 3.9.3 异常体系(强制)

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

#### 3.9.4 强制约束(Don'ts)

- ❌ API 层调 `db.query(...)` 直接查 DB(必须经 service)
- ❌ API 层写业务计算、if 状态判断
- ❌ Service 层接 Pydantic schema(只接原生类型 + ORM 对象)
- ❌ Service 层返 Pydantic schema(只返 ORM 对象或原生 dict)
- ❌ Service 层持有 db session(只接参数,不创建)
- ❌ 跨 service 互调(只能主 service 编排子 service,避免循环依赖)
- ❌ 在 Model 上写业务方法(model 只承载数据 + relationship)
- ❌ 业务逻辑写在 `main.py`(只能装配 + 异常处理)
- ❌ 抛 `HTTPException`(统一走 ServiceError 体系)

#### 3.9.5 单一文件职责(🟡 推荐,项目自定)

| 文件 | 行数上限(建议) | 触发拆分的信号 |
|---|---|---|
| `app/api/<name>.py` | ≤ 200 | 同一资源有 3+ 端点 → 拆 `*_admin.py` / `*_view.py` |
| `app/services/<name>.py` | ≤ 300 | 出现 2 个独立业务域(如 income + expense)→ 拆 |
| `app/models/<name>.py` | ≤ 100 | 多对多关系交叉复杂 → 拆中间表单独文件 |
| `app/schemas/<name>.py` | ≤ 300 | 一文件 > 5 个 schema 类,按业务域拆 |

---

## 四、模板嵌入设计(改 9 处)

| # | 资产 | 改动 | 锁级 |
|---|---|---|---|
| 1 | **新增** `docs/process/tech_stack.md` | 标准栈规范本体(L1/L2/L3 + 8 层内容 + §3.9 分层架构) | — |
| 2 | `docs/process/templates/00_charter.md` | 加 **§2.5 技术栈确认** 段:① 引用 `docs/process/tech_stack.md` ② 选项"按标准栈 / 偏离项 + 理由" ③ 签字 = 锁 | 🔒 |
| 3 | `docs/process/templates/02_high_level_design.md` | §1 架构视图段加 1 句"按 [`docs/process/tech_stack.md`](process/tech_stack.md) §3.1-§3.8 选型" | 🟡 |
| 4 | `docs/process/templates/03_detailed_design.md` | §A 流程 / §B 接口 / §C DDL 三处开头各加 1 句"命名 / 锁层级遵循 [`docs/process/tech_stack.md` §3.6 §3.7](process/tech_stack.md)" | 🟡 |
| 5 | `docs/process/dod/00_charter.md` | 加 DoD 项:"§2.5 技术栈确认签字完整(标准 / 偏离都需签字)" | 🔒 |
| 6 | `docs/process/dod/02_high_level_design.md` | 加 DoD 项:"技术选型未引入 §3.1-§3.8 L1 锁层之外的栈(若有偏离,Phase 0 已签字)" | 🟡 |
| 7 | `docs/process/dod/03_detailed_design.md` | 加 DoD 项:"§A/§B/§C 命名/接口/字段对齐 §3.6 §3.7" | 🟡 |
| 8 | `docs/process/critics/02_high_level_design.md` | 加检查项:"接口 / 库 / 工具是否引入技术栈 §3.1-§3.8 L1 锁层之外的栈" | 🟡 |
| 9 | `docs/process/critics/03c_data_schema.md` | 加检查项:"表命名 / 字段类型是否对齐 §3.3 数据层规范" | 🟡 |
| 10 | `docs/process/critics/04_implementation.md` | 加检查项:"实际代码与 Phase 0 选型一致;无未在 Phase 0/2 锁过的新依赖" | 🟡 |
| 11 | `docs/process/README.md` | 加 "技术栈规范" 章节入口,链向 `tech_stack.md` | 🟡 |
| 12 | `docs/process/CHANGELOG.md` | 记 v0.2.0(本变更) | — |

> 表格列出 12 处改动(用户原话"9 处",实际拆解为 12 个文件操作;实施时可一次 commit 完成)。

### 4.1 Phase 0 模板 §2.5 长这样(示意)

```markdown
## 2.5 技术栈确认

> 标准栈见 [`docs/process/tech_stack.md`](process/tech_stack.md)。
> 本节一旦签字,Phase 2/3/4 不再能改;偏航必须显式 unlock Phase 0 + 走 critic。

- **本项目栈选择**:
  - [ ] 按标准栈执行(L1 + L2 全锁,L3 自选)
  - [ ] 偏离标准栈,具体偏离项:
    - 偏离项 1: ___ (理由: ___)
    - 偏离项 2: ___ (理由: ___)

- [ ] 你本人签字: _______ (YYYY-MM-DD) — 锁生效
```

---

## 五、偏航 / Unlock 流程

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

### 5.1 轻量级 vs 重量级偏离

| 级别 | 范围 | 处理 |
|---|---|---|
| **轻量级** | L3 范围内的子选择(如"用 happy-dom 而不是 jsdom"、选具体 L3 库) | 不需要 unlock,Phase 0/2 文档补 1 句说明即可 |
| **重量级** | L1/L2 改动(如"放弃 FastAPI 改 Django"、引入新 L1 库) | 必须走上面 4 步 unlock |

---

## 六、文档结构 + 版本管理

### 6.1 结构

```
pm-template/
├── README.md                       (中英双语,5 phase + tech_stack 入口)
├── LICENSE (?)
├── docs/
│   └── process/
│       ├── README.md               (中英,模板使用指南)
│       ├── STATE.md                (空状态,等用户填)
│       ├── CHANGELOG.md            (v0.2.0 本变更)
│       ├── tech_stack.md           ← 新增,本设计核心交付
│       ├── templates/              (5 个 phase 模板)
│       │   ├── 00_charter.md       (加 §2.5 技术栈确认)
│       │   ├── 01_requirements.md
│       │   ├── 02_high_level_design.md   (加 stack 引用)
│       │   ├── 03_detailed_design.md     (加 stack 引用)
│       │   └── 04_implementation.md
│       ├── dod/                    (5 个)
│       │   ├── 00_charter.md       (加锁 Phase 0)
│       │   ├── 01_requirements.md
│       │   ├── 02_high_level_design.md   (加防 L1 偏航)
│       │   ├── 03_detailed_design.md     (加命名/接口/字段对齐)
│       │   └── 04_implementation.md
│       ├── critics/                (7 个)
│       │   ├── 00_charter.md
│       │   ├── 01_requirements.md
│       │   ├── 02_high_level_design.md   (加 stack 检查)
│       │   ├── 03a_business_process.md
│       │   ├── 03b_api_design.md
│       │   ├── 03c_data_schema.md        (加数据层规范检查)
│       │   ├── 04_implementation.md     (加实际代码与选型一致性)
│       │   └── reports/.gitkeep
│       └── (其他原有资产)
└── (其他原有顶层文件)
```

### 6.2 版本管理

- `tech_stack.md` 顶部标 `**版本: v1.0**`(初版)
- 每次升级大改 → version bump(v1.0 → v2.0)
- `docs/process/CHANGELOG.md` 记"v2 改了什么 + 为什么 + 旧项目如何过渡"
- **升级不影响已锁定的项目**——KidBudget 当时按 v0.1 锁,即使 v2 发布,Phase 0 已签的"按 v0.1"仍生效;新项目按 v2 锁

### 6.3 单文件 vs 拆 `tech_stack/` 多文件

**决定**: 不拆,单文件 + 内部章节(`## §3.1 后端栈` / `## §3.2 前端栈` ...)
- 理由: 简洁、grep 友好、跨层对比容易(单页能看到 L1/L2/L3 整体)
- 何时拆: 真正超长(> 1000 行)或需要"独立子文件做子版本管理"时 → v2 再说

---

## 七、交付物清单(实施时按此 commit)

- **新增** `docs/process/tech_stack.md`(标准栈规范本体,~400-500 行,本 spec §3 全部内容)
- **改动** `docs/process/templates/00_charter.md` 加 §2.5 技术栈确认段
- **改动** `docs/process/templates/02_high_level_design.md` / `03_detailed_design.md` 各加 1 句 stack 引用
- **改动** `docs/process/dod/00_charter.md` 加 DoD 项(锁 Phase 0)
- **改动** `docs/process/dod/02_high_level_design.md` / `03_detailed_design.md` 加 DoD 项(防止 L1 偏航)
- **改动** `docs/process/critics/02_high_level_design.md` / `03c_data_schema.md` / `04_implementation.md` 各加 stack 检查项
- **改动** `docs/process/README.md` 加 "技术栈规范" 章节入口
- **改动** `docs/process/CHANGELOG.md` 记 v0.2.0
- **新建** `LICENSE`(MIT)
- **不动** KidBudget 本仓库(本次只在 pm-template 仓库做)

---

## 八、Verification Checklist(实施后签收)

- [ ] `pm-template` 仓库 GitHub 创建 + 勾选 "Template repository"
- [ ] KidBudget 当前 `docs/process/` 全部内容(20+ 文件)同步过去
- [ ] `tech_stack.md` 写入(覆盖本 spec §3 全部 9 小节)
- [ ] 12 处模板/DoD/critic 资产改动完成(对照 §4 表格)
- [ ] `README.md` 更新(中英双语,5 phase + tech_stack 入口)
- [ ] `CHANGELOG.md` v0.2.0 记录完成
- [ ] `LICENSE` 文件就位
- [ ] commit + push 通过
- [ ] 浏览器 spot check: GitHub "Use this template" 按钮可点;`docs/process/tech_stack.md` 渲染正常

---

## 九、What's Next

- **本 spec 实施后**: 调用 `writing-plans` skill 出实施 plan,逐步 commit
- **未来**: 当 v2 升级时(Stack 有重大变化,如 FastAPI 0.116 → 1.0 / Vue 3.6 → 4.0),另开 spec 处理
- **跨项目**: 新项目用 "Use this template" 复制后,Phase 0 §2.5 签字 = 锁;之后任何 phase 偏航按 §5 流程
