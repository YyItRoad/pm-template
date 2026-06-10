# 模板 [Phase 3] 详细设计

> 用途: 基于 Phase 2 概要,定流程 / 接口 / DDL,直接可实施
> 产出 3 个文件(用本模板的章节 A/B/C 各自填充):
>   - `docs/03a_business_process.md` = 本模板 §A
>   - `docs/03b_api_design.md` = 本模板 §B
>   - `docs/03c_data_schema.md` = 本模板 §C
> 禁止: 不引入 §2.2 / 03 列表之外的新能力(范围蔓延)

---

## §A. 详细业务流程 → `docs/03a_business_process.md`

> 命名 / 锁层级遵循 [`docs/process/tech_stack.md` §3 §4](../tech_stack.md)。
> 每条流程的"正常 + 异常"配对齐全,涉及金额的标注"同事务内联动 balance"

### A.1 [流程名,如"创建收入记录"]

**正常流程**:
1. 步骤 1
2. 步骤 2
3. 同事务: INSERT income + UPDATE budget.balance += amount

**异常分支**:
- 余额不足(对支出): 返 409,提示 "余额 X,需要 Y"
- 并发重复触发: 二次幂等,返同结果不二次落账
- 鉴权失败: 返 401/403

**关联接口**: `POST /income-operate`(03b §B.X)

---

## §B. 详细接口设计 → `docs/03b_api_design.md`

> 命名 / 接口风格遵循 [`docs/process/tech_stack.md` §3 §4](../tech_stack.md)。
> 接口清单 = Phase 2 §3 的 100%(不多不少)
> 每个接口 4 列必填:鉴权依赖 / 错误码清单 / 幂等策略 / 限频策略
> 入参"最小集",多一个冗余字段扣分

### B.X 接口名

| 项 | 值 |
|---|---|
| **路径 / 方法** | `POST /api/v1/___` |
| **鉴权依赖** | `require_role(parent)` / `require_coparent_of` / `require_admin_jwt` 等 |
| **入参**(最小集) | `{ field1, field2 }` |
| **出参** | `{ ... }` |
| **错误码清单** | 401 / 403 / 404 / 409 / 422 |
| **幂等策略** | (有/无,如何) |
| **限频策略** | (有/无,如何) |

**末尾自查**:列出"§B 中所有不在 Phase 2 §3 的接口",应为 0。

---

## §C. 数据表 DDL → `docs/03c_data_schema.md` + `sql/*_schema.sql`

> 命名 / 字段类型 / 字符集遵循 [`docs/process/tech_stack.md` §2.3 §3](../tech_stack.md)。
> DDL 可直接执行(放进 sql/ 跑一遍)
> 字段命名 100% 对齐 charter §3 规范,不用 admin_user_id 之类的别名
> 不引入 Phase 2 §2 数据模型之外的新表

### C.X 表名

```sql
CREATE TABLE ___ (
    id INT AUTO_INCREMENT PRIMARY KEY,
    -- 字段命名严格对齐 charter §3
    INDEX idx___ (___),
    UNIQUE KEY uk___ (___)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
```

**末尾自查**:列出"所有不在 Phase 2 §2 数据模型里的新表",应为 0。

---

## 决策记录(3 个文件共享,每个文件末尾都写)

- YYYY-MM-DD: 砍掉 ___,因为 ___

## critic + 签字(每个文件末尾)

- [ ] 03a critic 报告无 CRITICAL/HIGH(`docs/process/critics/reports/03a_business_process_<YYYY-MM-DD>.md`)
- [ ] 03b critic 报告无 CRITICAL/HIGH(`docs/process/critics/reports/03b_api_design_<YYYY-MM-DD>.md`)
- [ ] 03c critic 报告无 CRITICAL/HIGH(`docs/process/critics/reports/03c_data_schema_<YYYY-MM-DD>.md`)
- [ ] 你本人 review + 签字: _______ (YYYY-MM-DD)
