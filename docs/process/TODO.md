# pm-template 未来工作(TODO)

> 本文件列**未实现但有价值**的能力。优先级 / 触发条件 / 简易设计,留给后续 PR。
> 用法:有人提出"该做 X" 时,先看这里——避免重复设计。
> 维护规则:实现后从这里删一行,加到 `docs/process/CHANGELOG.md`。

## 1. 未实现的 /change type(优先级:中)

> `/change` 入口已实现 5 个常用 type(feature / bugfix / refactor / hotfix / doc)。
> 以下 type 需求存在但暂未模板化,需新加时按"Batch B"模式扩展。

| type | 描述 | 模板结构建议 | 严格度 |
|---|---|---|---|
| **upgrade** | 依赖升级(FastAPI 0.115 → 0.116,Vue 3.5 → 3.6) | 改动范围 / changelog 阅读 / 兼容性验证 / 回退路径 | 中(1 人) |
| **perf** | 性能优化(慢查询 / 慢端点 / 大表) | 现状度量(数字) / 优化方案 / 优化后度量 / 风险 | 中(1 人) |
| **migration** | 数据 / 架构迁移(N8N→FastAPI 风格) | 双写策略 / 切换策略 / 数据校验 / 回退 | 重(1+1 reviewer) |
| **deprecation** | 弃用旧能力(旧 N8N 工作流 / 旧 API 版本) | 弃用公告 / 用户迁移指南 / 实际下线步骤 / 灰度时间 | 中(1 人) |

**实现路径**:
1. 复制 `docs/process/templates/change/_base.md`
2. 加 `<type>.md` 模板(段数与严格度对应)
3. 加 `docs/process/critics/change/<type>.md` + `docs/process/dod/change/<type>.md`
4. 更新 `.claude/skills/change.md` 的 type 白名单
5. 加 4-5 个 pytest 用例
6. 提交 1 个 commit

## 2. 项目生命周期类(优先级:低,触发才做)

> 这些场景**频率低 + 与具体项目强相关**,**不**通用化,做"项目级 checklist"即可。

| 场景 | 简化方案 |
|---|---|
| **Project sunset** | 写一个 `docs/sunset.md`,列"最后 release / 仓库归档 / 域名续费 / 通知用户" 4 步 checklist,做完即结束 |
| **Team handoff** | 写一个 `docs/handoff.md`,列"代码地图 / 部署账号 / 紧急联系人 / 上手任务" |
| **Compliance audit** | 跟具体法规强相关(SOC2 / GDPR / 等级保护),模板化没价值,由外部审计师提供清单 |
| **Disaster recovery** | 跟具体架构强相关(SLA / RTO / RPO),写 `docs/dr/<scenario>.md` 即可 |
| **Stakeholder comms** | 跟组织结构强相关,无法模板化,每团队自定沟通节奏 |
| **Risk register** | 可选,写一个 `docs/risks.md` 表格(风险 / 概率 / 影响 / 缓解 / 负责人)即可,不必开 skill |

## 3. 跨切面增强(优先级:低)

| 增强 | 描述 |
|---|---|
| **ADR 全文搜索** | `grep -r "superseded by" docs/decisions/` 找过期决策 |
| **Release 自动化** | git tag → 自动写一行到 `docs/releases.md`(GitHub Actions) |
| **变更 → release 反查** | 某 release 包含哪些变更,一键导出 changelog |
| **变更 → ADR 反查** | 哪些变更受 ADR 驱动(双向链接) |

## 4. 工具 / 脚本类(优先级:低,触发才写)

| 工具 | 用途 |
|---|---|
| `scripts/validate_state.py` | 检查 STATE.md 主 5 phase + 变更日志两套状态机一致性 |
| `scripts/new_change.py` | `/change` 的 CLI 替代品(无 AI 时手动用) |
| `scripts/list_orphan_changes.py` | 找 STATE.md 标记 [x] 但 `docs/changes/` 里文件不存在的变更号 |

## 5. 不做(明确放弃)

| 场景 | 不做的理由 |
|---|---|
| **Story point 估算** | 主观且团队间差异大,无统一标准,引入反而制造噪音 |
| **Burndown / Velocity 图** | 跟具体迭代节奏强相关,非通用 |
| **甘特图** | 重型工具,通常被外部工具(Jira/飞书)替代 |
| **OKR / KPI 跟踪** | 组织管理范畴,跟代码无关 |
| **会议纪要模板** | 与 PM 工具无直接关系 |

## 6. 触发本 TODO 的判据

- 用户多次提到某类工作"流程不顺"
- 某 TODO 出现 ≥3 次相关 issue
- 项目变大到某阈值(如 phase 5 完成 + ≥20 个 change)

不要为了"完整性"提前实现本文件内容。
