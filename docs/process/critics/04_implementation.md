# Critic [Phase 4] 实现 + 验证

> 复制本文件全部内容 + 加"请对 `<code_path>` 跑自审(代码 + e2e 脚本)"

## 你要检查的

1. **AC 覆盖率(最严重)**
   - 提取 Phase 1 所有 AC 编号
   - 检查 `e2e_*.sh` 或 `tests/` 目录:每个 AC 编号都对应至少 1 个 e2e case?
   - 缺 = **CRITICAL**(该 AC 没验证)

2. **范围蔓延(代码层)**
   - 代码里有 Phase 1 故事没出现的能力?
   - grep 关键路径:`/admin/...` route,Phase 1 故事里没出现 = CRITICAL
   - 特别注意 admin 用户的"私活"

3. **反向需求真没做**
   - 提取 Phase 1 §5 反向需求
   - 对每条 grep 代码:应 0 命中
   - 命中 = CRITICAL(明确说"不做"的被偷偷做了)

4. **接口一致性**
   - 03b 接口 vs 实际后端代码 path/method 100% 一致?
   - diff `03b_api_design.md` 的 path 列表 vs 后端 `@router.get/post` 装饰器
   - 不一致 = CRITICAL

5. **单测覆盖**
   - 每接口 ≥1 happy + 1 sad?
   - 缺 sad = MEDIUM

6. **决策记录更新**
   - 实现中发现与文档不一致,回写到 Phase 2/3 §6 了?
   - 没更新 = MEDIUM

7. **部署可启动**
   - `docker compose up` 起得来?
   - 失败 = CRITICAL

8. **技术栈一致性**
   - 实际代码使用的库 / 工具与 Phase 0 §2.5 选型一致
   - 无未在 Phase 0 / Phase 2 锁过的新依赖
   - 实际引入但未在 Phase 0 §2.5 / Phase 2 记录的库 = HIGH(擅自加依赖)

## 输出格式

- markdown 报告
- **每条 CRITICAL 必须列出 AC 编号 / 接口 path / 反向需求条目**,不能空泛

## 自我约束

- 同其他 phase
- **AC 覆盖率**是这一 phase 关键,没覆盖的 AC 意味着"该功能没验证"上生产
- 范围蔓延是这一 phase 第二大陷阱,admin 用户的"私活"是常见来源,严格报
