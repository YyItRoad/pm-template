# Critic [Phase 3a] 详细业务流程

> 复制本文件全部内容 + 加"请对 `<artifact_file>` 跑自审"

## 你要检查的

1. **正常 + 异常配对**
   - 每条流程有"正常流程"和"异常分支"两个小节?
   - 单独写"正常流程"无异常 = HIGH

2. **金额事务联动**
   - 涉及金额的流程(INCOME / EXPENSE / BUDGET_SETTING / APPLY_APPROVE)都标注"同事务内联动 balance"?
   - grep "同事务" 或 "事务内" 在相关流程中命中
   - 漏标 = **CRITICAL**(会导致数据不一致,生产 bug)

3. **关联接口**
   - 每条流程末尾有"关联接口"指向 03b?
   - 缺 = MEDIUM

4. **状态机非法**
   - 申请审批流程: approved 后还能改?
   - budget-setting: balance 改为负数?
   - 收入/支出: 二次重复触发是否幂等?
   - 上述任一没拦截 = CRITICAL

5. **范围蔓延**
   - 流程图里引入了 Phase 1/2 没出现的能力?
   - 实际 grep 流程小节标题,跟 Phase 2 §3 求差集

## 输出格式

- markdown 报告
- 每条标注 **CRITICAL** / **HIGH** / **MEDIUM** / **LOW**
- 事务联动漏标必须**指出具体流程名**

## 自我约束

- 同其他 phase
- 事务联动是这一 phase **最容易出生产 bug** 的点,严格报 CRITICAL,不要"作者意图如此"开脱
