---
name: release
description: 把当前所有 [x] 变更聚合为 1 个 release 版本,写 docs/releases.md 一行 / 一段。轻量级手工操作,不强制 critic。tag 命名遵循 v<X>.<Y>.<Z>(major/minor/patch)。
---

# /release — 版本发布

## 用途

把所有 `[x]` 状态的变更聚合成 1 个 release 版本,写 `docs/releases.md` 一行(或一段) + git tag。

**位置**:`docs/releases.md`(单文件,不每版本一个 md)
**模板**:`docs/process/templates/release.md`

**写 STATE.md**:不直接写(STATE.md 的"变更日志"段是变更的列表,release 是其聚合视图)。

## 触发

```bash
/release v0.12.0                    # 显式版本号 + 聚合所有 [x] 变更
/release v0.12.0 --include #0001,#0003    # 指定变更号(否则聚合所有 [x])
/release --list                      # 列所有 release(读 docs/releases.md)
/release --dry v0.12.0               # 只预览,不写文件
```

## 版本号规范

| 级别 | 格式 | 场景 | 例 |
|---|---|---|---|
| **Major** | v0 → v1 | 架构级 / 不向后兼容 | v1.0.0 → v2.0.0 |
| **Minor** | v0.0 → v0.1 | 加新能力(feature 变更) | v1.0.0 → v1.1.0 |
| **Patch** | v0.0.0 → v0.0.1 | 修 bug / 文档 / 小重构 | v1.0.0 → v1.0.1 |
| **Suffix** | `-rc.1` / `-beta.2` | 预发布 | v1.0.0-rc.1 |

## 执行步骤

### 1. 扫 STATE.md 变更日志

读 `docs/process/STATE.md` "变更日志" 段,提取所有 `[x]` 状态 + `[DEPRECATED]` 状态(后者标废弃,不入新 release)。

```bash
python3 -c "
import sys
sys.path.insert(0, '.claude/scripts')
from update_state import find_state_file, parse_state
# 注:变更日志是 markdown 表格,不是状态机 — 用 grep 提取更合适
"
```

实际更简单:用 `grep -E '^\| [0-9]+ ' docs/process/STATE.md` 提取表格行。

### 2. 选变更

默认聚合所有 `[x]` 状态变更。
`--include <#NNNN,...>` 显式指定。
`--exclude <#NNNN,...>` 排除某些。

### 3. 引导写 release 段

按模板段填:
- 版本号(必填)
- 日期(回车默认今天)
- 类型(看本次聚合的 type 占比:全 feature = feature, 全 bugfix = bugfix, 混合 = mixed)
- 包含变更(自动填 `--include` 或聚合结果)
- 作者 / 部署 / 验证 / 回滚方案 / 关联 ADR / 关联 5 phase 段

**模板格式**(详 `docs/process/templates/release.md`):
```markdown
## vX.Y.Z — YYYY-MM-DD

**类型**:feature / bugfix / refactor / hotfix / doc / mixed
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

### 4. 写 `docs/releases.md`(按时间倒序)

新 release 段**插入**到文件顶部(BEGIN/END EXAMPLE 段之下),保持最新在上。

### 5. 提示 git tag(可选)

```
> 建议执行:
>   git tag -a v0.12.0 -m "Release v0.12.0 — 5 changes"
>   git push origin v0.12.0
```

**不自动打 tag**(打 tag 是外部动作,需用户明示)。--auto-tag 旗标可自动打(谨慎)。

## /change → /release 联动

`/change <type> <name>` 锁 [x] 后,提示用户"是否走 /release 聚合"。

- 单变更 → 直接 `/release vX.Y.Z --include #NNNN`
- 多变更累计 → 定期(如每周)跑 `/release vX.Y.Z`(聚合所有 [x])

## 与 docs/releases.md 文件的兼容性

- 文件首部是模板说明 + BEGIN/END EXAMPLE 段(锁定不删)
- 中间是真实 release 段(按时间倒序)
- 文件末尾留空(给未来追加)

`/release` 写入时**只在 BEGIN/END EXAMPLE 段下方追加**,不动模板说明。

## 错误处理

| 错误 | 行为 |
|---|---|
| 0 个 `[x]` 变更 | 提示"无 release 候选,等 /change 锁完再来" |
| 版本号格式错 | 报 `ERR_RELEASE_VERSION_INVALID`,要求 vX.Y.Z 格式 |
| docs/releases.md 不存在 | 拉 release.md 模板复制 |
| 同一版本号已存在 | 报 `ERR_RELEASE_DUPLICATE`,提示用 patch 号(0.0.1 → 0.0.2) |

## 不要做的

- 不直接 git push(打 tag + push 是用户动作)
- 不改历史 release 段(只追加新的)
- 不把"进行中"`[~]` 状态变更合入 release(必须 [x])
- 不在 release 段写"已知 bug"列表(那是 issue tracker 的事)
- 不混用 [DEPRECATED] 变更进新 release(标记为废弃的不算"包含"内容)
- 不批量删除历史 release 段(审计追溯,必须留)

## 跨切面

- **ADR 联动**:release 段关联 ADR 时填 `**关联 ADR**:#NNNN`
- **变更 → release 反查**:每个变更 spec 的 `§9 关联引用` 段可填对应 release 号
- **自动化**(TODO §3):git tag 触发自动写 release log(GitHub Actions)
