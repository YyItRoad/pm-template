# 模板 [Change] Doc — 文档变更

> 用途:改 README / ADR / 注释 / 架构图 / 部署文档——**不改代码逻辑**。
> 严格度:**轻**(3 项 critic / 3 项 DoD / 1 人签字)。
> 禁止:借 doc 改代码——那用 bugfix/refactor/feature。

---

## §1.1 改动范围 [必填]

- **涉及文件**:
  - `README.md`(改了 §X)
  - `docs/02_high_level_design.md`(改了 §Y)
  - ___ (其他)
- **改动类型**:补漏 / 修正错误 / 同步代码(代码改了但文档没跟上) / 重写

## §1.2 改动理由 [必填]

- **为什么改**:
  - 用户反馈 / reviewer 提了 / 跟代码不一致 / 过期信息
- **为什么不在原 PR 里改**:(若适用,代码 PR 已合并,文档单独补)

## §1.3 验证 [必填]

- [ ] 文档拼写 / 链接 / 代码示例 通过(可本地 `markdownlint` / `mdsh`)
- [ ] 引用的代码路径 / 命令 / API 在当前 commit 仍存在
- [ ] 中英文版本(如有)同步

## §10 critic + 签字(1 人)

- [ ] 变更 critic 报告无 CRITICAL/HIGH
- [ ] DoD 3/3 ✓
- [ ] 起草人 review + 签字: _______ (YYYY-MM-DD)
