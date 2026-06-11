# 模板 [Change] 变更记录(公共骨架)

> 用途:每条变更(`/change <type> <name>`)的 spec 文件都基于本骨架,**type 模板只追加 type 特有段**。
> 用法:`cp docs/process/templates/change/_base.md docs/changes/NNNN-<type>-<name>.md` → 在 type 模板引导下填各段
> 完成后必跑对应 type 的 critic + DoD,签字后写 STATE.md "变更日志" 段

## §0 元信息(自动生成,起草不改)

- **变更号**:NNNN(由 `/change` 自动分配)
- **类型**:{feature|bugfix|refactor|hotfix|doc}
- **加于**:YYYY-MM-DD
- **起草人**:
- **签字**:
- **状态**:[ ]

## §1 type 特有段(由 type 模板追加)

> 每个 type 必填的段,**段标 [必填] 不可缺**,空 = critic CRITICAL。
> [可选] 段整段不写 = 合法的"跳过"用法,**挂占位符 ___** = ERR_OPTIONAL_SECTION_FILLED_BUT_BLANK

> **段号说明**:type 模板的 §1.x 段号在 _base 之下,**不必连续**也**不必对齐**——
> hotfix 用 §1.1-1.4(4 段),doc 用 §1.1-1.3(3 段),bugfix 用 §1.1-1.5(5 段),
> feature / refactor 用 §1.1-1.6(6 段)。
> 新加 type 时按需定段号,但 §10 签字必含(type 模板决定签字人数)。
> 详细段号在 type 模板的 `§10 critic + 签字` 段。

> 详细内容见 type 模板(`docs/process/templates/change/<type>.md`)。

## §9 关联引用(可选用,起草人填)

- **关联变更**:NNNN(同项目其他变更号)
- **关联 ADR**:NNNN(`docs/decisions/NNNN-*.md` 决策号)
- **关联 Release**:vX.Y.Z(`docs/releases.md` 版本号)
- **关联 5 phase 段**:`docs/01_requirements.md` §X / `docs/03b_api_design.md` §X(如有)

## §10 critic + 签字(由 type 模板追加)

> 每个 type 的签字流程不同(hotfix 1 人 / feature 1 人 + 1 reviewer)。
> 详见 type 模板的签字段。
