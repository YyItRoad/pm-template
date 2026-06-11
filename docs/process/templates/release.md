# 模板 [Release] 版本发布日志

> 用途:每个发布版本记一行/一段,**版本号 + 包含的变更 + 部署信息**。
> 位置:`docs/releases.md`(单文件,不每版本一个 md)
> 触发:任意 `/change` 锁 [x] 后,在本文件追加一行(轻量手工即可,不必开 skill)

## 使用方式

```bash
# 锁变更后,一行 append:
## vX.Y.Z — YYYY-MM-DD

**类型**:feature / bugfix / refactor / hotfix / doc
**包含变更**:#0001, #0003, #0005
**作者**:
**部署**:
- 时间:YYYY-MM-DD HH:MM
- commit:<sha>
- 验证:✓ / ✗
**回滚方案**:
**关联 ADR**:#NNNN(如有)
**关联 5 phase 段**:Phase X §Y
```

## 版本规范(建议)

- **Major(v1 → v2)**:架构级变更,可能不向后兼容
- **Minor(v1.0 → v1.1)**:加新能力(feature 变更)
- **Patch(v1.0.0 → v1.0.1)**:修 bug / 文档 / 小重构
- **Suffix**:`-rc.1` / `-beta.2` / `-hotfix.1` 标注预发布

## 历史

<!-- 在此下方追加,最新的在最上面 -->

<!-- BEGIN EXAMPLE — 真实发布时整段删除 -->
## v0.11.0 — 2026-06-09(示例,真实发布时整段删除)

**类型**:feature
**包含变更**:#0001-feat-audit-log
**作者**:yyitroad
**部署**:
- 时间:2026-06-09 22:00
- commit:94871c4
- 验证:✓ e2e_smoke 30/30
**回滚方案**:`git revert 94871c4` + 重 deploy
**关联 ADR**:#0002-merge-budget-into-user
**关联 5 phase 段**:Phase 1 §0.1 / Phase 3 §B.5
<!-- END EXAMPLE -->

