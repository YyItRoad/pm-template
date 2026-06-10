# Critic [Phase 3c] 数据表 DDL

> 复制本文件全部内容 + 加"请对 `<artifact_file>` 跑自审"

## 你要检查的

1. **DDL 可执行性**
   - sql 文件可直接 `mysql < schema.sql` 无语法错误?
   - 列出具体哪条 CREATE TABLE 报错(若有)

2. **字段命名规范**
   - 字段命名 100% 对齐 charter §3 规范
   - grep 禁词(如 `admin_user_id`,`user_name` 之类的别名)
   - 命中 = HIGH

3. **新表范围检查**
   - 提取 03c 所有 CREATE TABLE 表名,跟 Phase 2 §2 求差集
   - 多出 = CRITICAL(范围蔓延)
   - 少 = CRITICAL(漏建表)

4. **唯一约束**
   - 业务上要求"唯一"的字段(如 `doubao_id`,`child_user_id` in budget)有 UNIQUE KEY?
   - 缺 = HIGH(防止脏数据)

5. **索引意图**
   - 经常 WHERE 用的字段有 INDEX?
   - 无故 INDEX 过多 = LOW(性能浪费)

6. **外键**
   - 有外键关系(虽然 MySQL 可不用,但表注释里应说明)?
   - 漏 = MEDIUM

7. **字段类型**
   - 金额字段用 DECIMAL,不是 FLOAT?
   - 时间字段用 DATETIME,不是 VARCHAR?
   - 主键用 INT AUTO_INCREMENT 或 BIGINT,不是 UUID(除非特别需要)?
   - 错 = HIGH

8. **数据层规范对齐**
   - 表命名 / 字段类型 / 字符集 / 索引命名是否对齐 `docs/process/tech_stack.md` §2.3 数据层规范
   - utf8mb4 + InnoDB + snake_case + DECIMAL(10,2) 全部满足?
   - 任一不满足 = HIGH

9. **必填槽位(机械 grep,新加)**
   - grep `<!-- ANCHOR: tables -->` 必命中
   - 必含表注释 / 字段类型 / 索引意图 三栏(任一缺 = HIGH)
   - 抽查 1 张表:三栏是否都填了(防"挂 anchor 留空")

## 输出格式

- markdown 报告
- **DDL 错误必须贴出具体 SQL 片段**
- 每条标注 **CRITICAL** / **HIGH** / **MEDIUM** / **LOW**

## 自我约束

- 同其他 phase
- **范围检查**是这一 phase 关键,新表是 AI 自由发挥最常塞的东西
