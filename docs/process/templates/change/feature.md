# 模板 [Change] Feature — 加功能

> 用途:为已锁 5 phase 项目加新能力(新 API / 新页面 / 新表 / 新角色权限)。
> 严格度:**重**(10 项 critic / 10 项 DoD / 1 人 + 1 reviewer 签字)。
> 禁止:不加新能力而"小幅改旧功能"——那用 bugfix 或 refactor。

---

## §1.1 动机 [必填]

> 1 句话说清**为什么加这个功能**。禁止写"因为 PM 提了" / "因为老板说要做"。

- **问题**:
- **谁会受益**(引用 Phase 1 §0.1 角色):

## §1.2 用户故事 + AC [必填]

> 沿用 Phase 1 风格。每条 AC 必可"是/否"判定。AC 编号续主 01 文档(不要 AC-F001 之类自创体系)。

- **故事 ID**:AC-XXX.X(续 Phase 1 编号)
- **故事**:
- **AC 1**:
- **AC 2**:
- **AC 3**:

## §1.3 设计 diff [必填]

> 标"+新接口/字段"而非全文重写。**只列新增**,不重述旧内容。

### 接口(如有)

| 路径 | 方法 | 用途 | 鉴权依赖 | 错误码 | 续 §X(主 03b 编号) |
|---|---|---|---|---|---|
| `POST /api/v1/__new__` | POST | ___ | ___ | ___ | B.X |

### 数据表(如有)

| 表名 | 变更类型 | 续 §X(主 03c 编号) |
|---|---|---|
| `__new_table__` | 新建 | C.X |

> 0 新增接口 + 0 新表 = 不是 feature,是 refactor,改 type 重新走。

### 现有影响(必填,无则写"无")

- 哪些旧接口被废弃 / 改语义?
- 哪些旧表加列 / 加索引?
- 哪些旧角色权限变化?

## §1.4 测试 diff [必填]

> 标"+N case"格式,引用 AC 编号。

| AC | 单元 / 集成 case | e2e case |
|---|---|---|
| AC-XXX.1 | ___ | `scripts/e2e_*.sh` §X |
| AC-XXX.2 | ___ | ___ |

> 缺 e2e 覆盖的 AC 编号 → critic HIGH。

## §1.5 部署 / 迁移 [必填]

- **migration 文件**:`sql/migrations/V<N+1>__<feature>.sql`(如有)
- **回滚方案**:___
- **feature flag / 灰度**:___

## §1.6 文档同步(可选用)

- [ ] README.md 同步
- [ ] API 文档同步
- [ ] CHANGELOG 同步

## §10 critic + 签字(2 人)

- [ ] 变更 critic 报告无 CRITICAL/HIGH(`docs/process/critics/reports/change_feature_<YYYY-MM-DD>.md`)
- [ ] DoD 10/10 ✓
- [ ] 起草人 review + 签字: _______ (YYYY-MM-DD)
- [ ] 独立 reviewer review + 签字: _______ (YYYY-MM-DD)
