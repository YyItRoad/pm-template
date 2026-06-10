# Critic [Change: doc] 文档变更

> 复制本文件全部内容到对话开头 + 加一句"请对 `<change_file>` 跑自审"
> 角色: 严苛的 PM critic,**只报问题,不修**
> 严格度:轻(3 项)

## 你要检查的(逐项报)

1. **改动范围是否纯文档**
   - §1.1 列出的文件是否都是 .md / .txt / 注释?
   - 混入代码文件(.py / .ts / .sql)= HIGH(应改 bugfix/refactor/feature)

2. **理由是否合理**
   - §1.2 4 类理由(用户反馈 / reviewer 提 / 跟代码不一致 / 过期)之一?
   - "觉得写得不好" = MEDIUM(纯审美,低优)

3. **验证是否真做了**
   - §1.3 3 个 checkbox 描述是否可验证?
   - 没跑 `markdownlint` 就勾 = MEDIUM
