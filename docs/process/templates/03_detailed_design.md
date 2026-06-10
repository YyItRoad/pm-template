# 模板 [Phase 3] 详细设计

> 用途: 基于 Phase 2 概要,定流程 / 接口 / DDL,直接可实施
> 产出 3 个文件(用本模板的章节 A/B/C 各自填充):
>   - `docs/03a_business_process.md` = 本模板 §A
>   - `docs/03b_api_design.md` = 本模板 §B
>   - `docs/03c_data_schema.md` = 本模板 §C
> 禁止: 不引入 §2.2 / 03 列表之外的新能力(范围蔓延)

> **章节必填规则**(本版起强制):
> - `[必填]` 段不可缺,空 = critic CRITICAL
> - `[可选]` 段**两种合法状态**:整段不写 / 写了填内容。**挂了标题但内容是占位符 ___** = `ERR_OPTIONAL_SECTION_FILLED_BUT_BLANK`
> - 每个流程/接口/表的子条目(A.1, B.X, C.X)是 `[必填]`,**不可漏**

---

## §A. 详细业务流程 → `docs/03a_business_process.md` [必填]

> 命名 / 锁层级遵循 [`docs/process/tech_stack.md` §3 §4](../tech_stack.md)。
> 每条流程的"正常 + 异常"配对齐全,涉及金额的标注"同事务内联动 balance"

### A.1 [流程名,如"创建收入记录"] [必填]

<!-- ANCHOR: process-1-normal -->
**正常流程**:
1. 步骤 1
2. 步骤 2
3. 同事务: INSERT income + UPDATE budget.balance += amount

<!-- ANCHOR: process-1-exception -->
**异常分支**:
- 余额不足(对支出): 返 409,提示 "余额 X,需要 Y"
- 并发重复触发: 二次幂等,返同结果不二次落账
- 鉴权失败: 返 401/403

**关联接口**: `POST /income-operate`(03b §B.X)

### A.2 [流程名] [必填]

<!-- ANCHOR: process-2-normal -->
**正常流程**:
<!-- ANCHOR: process-2-exception -->
**异常分支**:

---

## §B. 详细接口设计 → `docs/03b_api_design.md` [必填]

> 命名 / 接口风格遵循 [`docs/process/tech_stack.md` §3 §4](../tech_stack.md)。
> 接口清单 = Phase 2 §3 的 100%(不多不少)
> 每个接口 4 列必填:鉴权依赖 / 错误码清单 / 幂等策略 / 限频策略
> 入参"最小集",多一个冗余字段扣分

<!-- ANCHOR: api-list -->
### B.1 接口清单总表 [必填]

| 编号 | 路径 | 方法 | 鉴权依赖 | 错误码清单 | 幂等策略 | 限频策略 | 对应 AC |
|---|---|---|---|---|---|---|---|
| B.1 | `POST /api/v1/___` | POST | ___ | ___ | ___ | ___ | AC-XX.X |
| B.2 | ___ | ___ | ___ | ___ | ___ | ___ | ___ |

### B.X 接口详情 [必填]

#### B.X.1 [接口名]

| 项 | 值 |
|---|---|
| **路径 / 方法** | `POST /api/v1/___` |
| **鉴权依赖** | `require_role(parent)` / `require_coparent_of` / `require_admin_jwt` 等 |
| **入参**(最小集) | `{ field1, field2 }` |
| **出参** | `{ ... }` |
| **错误码清单** | 401 / 403 / 404 / 409 / 422 |
| **幂等策略** | (有/无,如何) |
| **限频策略** | (有/无,如何) |
| **对应 AC** | AC-XX.X |

**末尾自查**:列出"§B 中所有不在 Phase 2 §3 的接口",应为 0。

---

## §C. 数据表 DDL → `docs/03c_data_schema.md` + `sql/*_schema.sql` [必填]

> 命名 / 字段类型 / 字符集遵循 [`docs/process/tech_stack.md` §2.3 §3](../tech_stack.md)。
> DDL 可直接执行(放进 sql/ 跑一遍)
> 字段命名 100% 对齐 charter §3 规范,不用 admin_user_id 之类的别名
> 不引入 Phase 2 §2 数据模型之外的新表

<!-- ANCHOR: tables -->
### C.1 表清单总表 [必填]

| 编号 | 表名 | 用途 | 对应故事 |
|---|---|---|---|
| C.1 | `user` | 用户主表 | S-XX |
| C.2 | ___ | ___ | ___ |

### C.X 表 DDL [必填]

#### C.X.1 [表名]

```sql
CREATE TABLE ___ (
    id INT AUTO_INCREMENT PRIMARY KEY,
    -- 字段命名严格对齐 charter §3
    INDEX idx___ (___),
    UNIQUE KEY uk___ (___)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='___';
```

**末尾自查**:列出"所有不在 Phase 2 §2 数据模型里的新表",应为 0。

---

## 附录 A: 性能 / 容量基线 [可选]

> 简单项目可跳(整段不写)。复杂项目填具体 QPS / 容量估算。
> 挂了标题但内容是占位符 → ERR_OPTIONAL_SECTION_FILLED_BUT_BLANK

## 附录 B: 安全 / 合规检查点 [可选]

> 留"上线前必须复核的安全/合规项"位置。简单项目可跳。
> 挂了标题但内容是占位符 → ERR_OPTIONAL_SECTION_FILLED_BUT_BLANK

## 决策记录(3 个文件共享,每个文件末尾都写) [必填]

- YYYY-MM-DD: 砍掉 ___,因为 ___

## critic + 签字(每个文件末尾) [必填]

- [ ] 03a critic 报告无 CRITICAL/HIGH(`docs/process/critics/reports/03a_business_process_<YYYY-MM-DD>.md`)
- [ ] 03b critic 报告无 CRITICAL/HIGH(`docs/process/critics/reports/03b_api_design_<YYYY-MM-DD>.md`)
- [ ] 03c critic 报告无 CRITICAL/HIGH(`docs/process/critics/reports/03c_data_schema_<YYYY-MM-DD>.md`)
- [ ] 你本人 review + 签字: _______ (YYYY-MM-DD)
