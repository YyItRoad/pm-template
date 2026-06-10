# DoD [Phase 4] 实现 + 验证

> 全部勾上才允许把项目/特性标 release-ready。

- [ ] 编码(按项目习惯,本项目默认"先实现后测试")
- [ ] 单测: 覆盖 Phase 3b 接口(每接口 ≥1 happy + 1 sad)
- [ ] e2e: 覆盖 Phase 1 每条 AC(每 AC ≥1 e2e case,AC 编号 = e2e case 名)
- [ ] 部署: `docker compose up` 起得来,health check 通过
- [ ] 文档反向同步: 03b 接口 vs 实际后端代码 100% 一致(grep 查 path/method)
- [ ] 反向需求验证: Phase 1 §5 反向需求列的"不做的事"在代码里真的没做(grep 反向需求关键字,代码中应 0 命中)
- [ ] 决策记录更新: 实现中发现与文档不一致的,回写 Phase 2/3 §6
- [ ] critic(code-reviewer 自审)无 CRITICAL/HIGH
- [ ] 你本人 review + 签字
