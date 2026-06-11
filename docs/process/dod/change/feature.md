# DoD [Change: feature] 加功能

> 全部勾上才允许签字 / 锁。每条都是可机械验证的。
> 编号方案:**`CF-NN`**(`CF` = Change Feature,与 5 phase DoD 的 `D0-NN` / `D1-NN` ... 区分)。
> 与 critic 引用对齐(critic 写 `CF-NN` 即可定位到此文件具体行)。

- [ ] **CF-01** §1.1 动机段有"问题"+"受益角色"两行,非空
- [ ] **CF-02** §1.2 至少 1 个 AC,每条可"是/否"判定
- [ ] **CF-03** §1.3 接口表 / 数据表 / 现有影响 3 段都有(若某项无,显式写"无")
- [ ] **CF-04** §1.4 测试表覆盖所有 AC,每 AC ≥1 e2e case 引用
- [ ] **CF-05** §1.5 migration / 回滚 / feature flag 3 段都有
- [ ] **CF-06** §1.6 文档同步清单所有 checkbox 已勾或显式"不需要"
- [ ] **CF-07** **critic 报告无 CRITICAL/HIGH**(报告路径已填)
- [ ] **CF-08** 起草人签字(YYYY-MM-DD + 姓名)
- [ ] **CF-09** 独立 reviewer 签字(YYYY-MM-DD + 姓名)
- [ ] **CF-10** STATE.md "变更日志" 段已加本变更号,状态 [x]
