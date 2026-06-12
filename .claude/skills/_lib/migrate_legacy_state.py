"""migrate_legacy_state.py — 把旧项目的 [x] 状态批量改成 [x] LEGACY。

只用于迁移试点项目(如旧版 KidBudget)的 STATE.md,9 skill 全部无权限写 [x] LEGACY,
只有本脚本可写。

CLI 用法:
    python .claude/skills/_lib/migrate_legacy_state.py <project_root>           # 交互模式
    python .claude/skills/_lib/migrate_legacy_state.py <project_root> --all     # 全部 phase 标 LEGACY
    python .claude/skills/_lib/migrate_legacy_state.py <project_root> --phase 0  # 只标 phase 0
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

# 复用 update_state 的常量
sys.path.insert(0, str(Path(__file__).parent))
from update_state import (  # noqa: E402
    VALID_STATUSES,
    StateError,
    atomic_write,
    find_state_file,
    get_current_status,
    make_diff,
    parse_state,
    serialize_state,
)

LEGACY_REASON_DEFAULT = "试点项目迁移:实施在本流程引入前完成,通过 e2e 验证,未走 critic"


def mark_legacy(
    project_root: Path, phases: list[int], reason: str = LEGACY_REASON_DEFAULT
) -> str:
    """把指定 phase 状态改为 [x] LEGACY(仅本脚本可写)。"""
    state_path = find_state_file(project_root)
    template = state_path.read_text(encoding="utf-8")
    state = parse_state(state_path)

    for phase in phases:
        if phase not in range(5):
            print(f"  warn: 跳过 phase {phase}(越界)", file=sys.stderr)
            continue
        current = get_current_status(state[phase])
        if current != "[x]":
            print(
                f"  warn: phase {phase} 当前 {current},不是 [x],不标 LEGACY",
                file=sys.stderr,
            )
            continue
        state[phase]["状态"] = "[x] LEGACY"
        state[phase]["lock_reason"] = reason
        if "signed_at" not in state[phase]:
            from datetime import date
            state[phase]["signed_at"] = date.today().isoformat()

    new_content = serialize_state(state, template)
    diff = make_diff(template, new_content)
    atomic_write(state_path, new_content)
    return diff


def main() -> int:
    parser = argparse.ArgumentParser(
        description="把旧项目的 [x] phase 改成 [x] LEGACY(迁移脚本,9 skill 不可调)"
    )
    parser.add_argument("project_root", type=Path, help="项目根目录(STATE.md 上两级)")
    parser.add_argument(
        "--all", action="store_true", help="全部 5 个 phase 标 LEGACY"
    )
    parser.add_argument(
        "--phase", type=int, action="append", help="指定 phase(可多次)"
    )
    parser.add_argument("--reason", default=LEGACY_REASON_DEFAULT, help="LEGACY 原因")
    args = parser.parse_args()

    if args.all:
        phases = list(range(5))
    elif args.phase:
        phases = args.phase
    else:
        # 交互模式:扫描所有 [x] phase,逐个问
        state_path = find_state_file(args.project_root)
        state = parse_state(state_path)
        candidates = [
            i for i in range(5) if get_current_status(state[i]) == "[x]"
        ]
        if not candidates:
            print("没有 [x] phase 可标 LEGACY")
            return 0
        print(f"找到 {len(candidates)} 个 [x] phase: {candidates}")
        ans = input("全部标 LEGACY?(y/n) ")
        if ans.lower() != "y":
            print("取消")
            return 0
        phases = candidates

    try:
        diff = mark_legacy(args.project_root, phases, args.reason)
    except StateError as e:
        print(f"✗ {e}", file=sys.stderr)
        return 1

    print(f"✓ 标记 LEGACY: phase {phases}")
    if diff:
        print("\n--- diff ---")
        print(diff)
    return 0


if __name__ == "__main__":
    sys.exit(main())
