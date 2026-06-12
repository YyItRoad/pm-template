---
name: change
description: 维护期变更入口(feature/bugfix/refactor/hotfix/doc 5 type)。基于已锁 5 phase,增量追加变更记录,不重跑基础设计。变更日志写 STATE.md"变更日志"段。
---

# /change <type> <name> — 变更记录入口

## 用途

对**已锁定 5 phase**的项目做单次变更。**不重跑** phase 0/1/2/3/4,只:
1. 复制对应 type 模板 → `docs/changes/NNNN-<type>-<name>.md`
2. 引导填变更 spec
3. 跑 critic(简化版,只审**新增**部分)
4. 跑 DoD
5. 用户签字
6. 写 STATE.md"变更日志"段

## 触发

```bash
/change feature audit-log         # 加功能
/change bugfix login-401          # 修 bug
/change refactor service-layer    # 重构
/change hotfix db-deadlock        # 紧急修复
/change doc readme-typo           # 文档
/change --list                    # 列所有未锁变更
/change --status <NNNN>           # 看某条变更状态
/change --deprecate <NNNN>        # 标废弃
```

`<type>` ∈ `{feature, bugfix, refactor, hotfix, doc}`(其他 type 见 `docs/process/TODO.md`)

## 前置条件

- 项目**已用 pm-template 跑过 5 phase**(`docs/STATE.md` 主 5 phase 含至少 1 个 `[x]`)
- 项目根有 `docs/changes/` 目录(无则自动建)

**无 STATE.md / 5 phase 未跑的项目** → 报 `ERR_CHANGE_REQUIRES_GREENFIELD`,提示先 `/new-project`。

## 执行步骤

### 1. 启动检查

**a) 验证 type 合法**:
```bash
case "$TYPE" in
  feature|bugfix|refactor|hotfix|doc) ;;
  *) echo "ERR_CHANGE_TYPE_INVALID: $TYPE (允许:feature/bugfix/refactor/hotfix/doc)"
     echo "→ 其他 type 详见 docs/process/TODO.md"
     exit 1 ;;
esac
```

**b) 检查 STATE.md 主 5 phase 至少 1 个 `[x]` 或 `[x] LEGACY`**:
```bash
python3 -c "
import sys
sys.path.insert(0, '.claude/skills/_lib')
from update_state import find_state_file, parse_state, get_current_status
st = parse_state(find_state_file())
locked = [get_current_status(st[i]) for i in range(5)]
# 接受 [x] 和 [x] LEGACY(试点项目用 LEGACY)
has_any_locked = any(s in ('[x]', '[x] LEGACY') for s in locked)
if not has_any_locked:
    print('ERR_CHANGE_REQUIRES_GREENFIELD (当前:', locked, ')')
    sys.exit(1)
"
```

**c) 拉 `docs/STATE.md` 解析"变更日志"段**(若不存在,初始化为空)。

### 2. 分配变更编号 + 建文件

```bash
NEXT=$(ls docs/changes/ 2>/dev/null | grep -oE '^[0-9]+' | sort -n | tail -1)
NEXT=$((NEXT + 1))
NEXT=$(printf "%04d" $NEXT)  # 4 位 0 补
FILE="docs/changes/${NEXT}-${TYPE}-${NAME}.md"
cp "docs/process/templates/change/${TYPE}.md" "$FILE"
```

**编号自动续**(不重用废弃号,保证单调递增)。

### 3. 标记 in-progress + 引导填 spec

```bash
# 在 STATE.md "变更日志" 段加一行,标 [~]
```

**按 type 选不同 critic 严格度**:

| type | critic 强度 | DoD 项数 | 签字流程 |
|---|---|---|---|
| hotfix | 极轻(4 项) | 4 | 1 人(操作者) |
| doc | 轻(3 项) | 3 | 1 人 |
| bugfix | 中(6 项) | 6 | 1 人 |
| refactor | 中(7 项) | 7 | 1 人 + 1 reviewer |
| feature | 重(10 项) | 10 | 1 人 + 1 reviewer |

**严格度含义**:critic 检查项数 / DoD 必勾项数 / 是否强制 reviewer。模板自带"必填段",critic 只查这些段。

### 4. 跑 critic

```bash
/critic change/<type>    # 调对应 critic,见 docs/process/critics/change/<type>.md
```

**关键原则**:**只审**变更 spec 内的**新增内容**。不重审已锁 phase 0/1/2/3/4 产物。

### 5. 跑 DoD

```bash
/dod-check change/<type>    # 调对应 DoD
```

### 6. Sign-off

按 type 走不同流程:
- **hotfix / doc / bugfix**:1 人 y/n/c
- **refactor / feature**:1 人 y/n/c **+** 1 reviewer y/n/c(可同一人,先后两次确认)

```
> 变更 #0001 (feature/audit-log) 待锁。
> critic: docs/process/critics/reports/change_feature_<DATE>.md (C/H/M/L: 0/0/1/0)
> DoD: 10/10 ✓
> 签字: <name> (YYYY-MM-DD)
> 请确认锁:[y / n / c]
```

### 7. 锁 + 写 STATE.md

```bash
# (1) 把变更号 + 状态写 STATE.md "变更日志" 段
# (2) 不调 update_state.py(那是 5 phase 状态机,变更日志是独立机制)
```

**变更日志状态机**(与 5 phase 独立):

| 状态 | 含义 | 谁能改 |
|---|---|---|
| `[ ]` | 已分配号,未填 | 起草人 |
| `[~]` | 填写中 | 起草人 |
| `[x]` | 已签字(对应代码已合并) | reviewer |
| `[DEPRECATED]` | 弃用(被新方案替代 / 项目重写) | 任何 reviewer |
| `[ABORTED]` | 取消(讨论后决定不做) | 起草人 |

### 8. 提示结束

```
> 变更 #0001 (feature/audit-log) 已锁(签字: <name> YYYY-MM-DD)。
> 同步任务:
>   1. 在 docs/01_requirements.md 追加新故事(可选,审增量)
>   2. 在 docs/03b_api_design.md 追加新接口(可选)
>   3. 写代码 + e2e
>   4. (如有 schema 变)在 sql/migrations/V<N+1>__<name>.sql 加 migration
>   5. tag 一个 release(如有 release log)
```

## 错误处理

| 错误 | 行为 |
|---|---|
| `ERR_CHANGE_TYPE_INVALID` | type 不在白名单,提示看 TODO.md |
| `ERR_CHANGE_REQUIRES_GREENFIELD` | 5 phase 未跑,提示先 /new-project |
| `ERR_CHANGE_FILE_EXISTS` | 同号文件已存在,检查编号 |
| critic CRITICAL | 停下等改 |
| DoD 缺项 | 列缺哪几条 |
| reviewer n | 退回到 [~] 等改 |

## 不要做的

- **不重审 5 phase 产物**:已锁就是已锁,改 phase 文档必须先 `/unlock`
- **不在变更 spec 内改 00_charter / 01 / 02 / 03 文档**:这些是项目事实,变更 spec 只**引用**它们
- **不把变更号重用给废弃的变更**:废弃的号留空,新变更用下一个号(审计追溯)
- **不在 hotfix 模板里写长设计**:hotfix 是"先止血再说",事后复盘另开 file
- **不强制要求 e2e 对每个变更**:小 bugfix / 文档可不写 e2e,DoD 里有这条

## 与 superpowers 集成(可选)

- 大型 feature / migration 可调 `superpowers:subagent-driven-development` 派发 TDD 子任务
- refactor 类变更可调 `superpowers:requesting-code-review` 强化 code review
- hotfix 类变更可调 `superpowers:systematic-debugging` 定位根因

## 跨切面联动(可选用)

- **ADR**:`/decision <title>` 创建决策记录 → 写 `docs/decisions/NNNN-<title>.md`
- **Release log**:变更 `[x]` 后,在 `docs/releases.md` 累加 changelog
- **TODO**:`docs/process/TODO.md` 列了未实现的 type / 场景,如需新 type 走"扩展 change 框架"而非直接 hack
