"""update_state.py — pm-template skill 共享的 STATE.md 写入 helper。

唯一合法写 STATE.md 的入口,14 skill 全部通过 `from update_state import update_state` 调用。
状态机定义见本文件 `STATE_MACHINE` 段(单一真源,pm-template v0.4.0 起替代原 spec §4.1)。

CLI 用法:
    python .claude/skills/_lib/update_state.py --phase 0 --status "[x]" --signed-by "Alice" --signed-at "2026-06-10"
    python .claude/skills/_lib/update_state.py --check  # 只解析 STATE.md,打印当前状态表
"""

from __future__ import annotations

import argparse
import re
import sys
from datetime import date
from pathlib import Path
from typing import Any

# ===== 状态机定义(单一真源) =====

VALID_STATUSES = {"[ ]", "[~]", "[x]", "[UNLOCKED]", "[SKIP]", "[x] LEGACY"}

# 合法转移: from_status -> {allowed to_status}
LEGAL_TRANSITIONS: dict[str, set[str]] = {
    "[ ]": {"[~]", "[SKIP]"},
    "[~]": {"[x]"},
    "[x]": {"[UNLOCKED]"},
    "[UNLOCKED]": {"[~]", "[x]"},
    "[SKIP]": {"[UNLOCKED]"},  # 跳过的 phase 也可解锁
    "[x] LEGACY": set(),  # 终态,不可改
}

# 必填 kwargs(按目标状态)
REQUIRED_KWARGS: dict[str, set[str]] = {
    "[x]": {"signed_by", "signed_at", "template_sha"},
    "[UNLOCKED]": {"lock_reason"},
    "[SKIP]": {"skip_reason"},
}

# 合法 kwargs 名
VALID_KWARGS = {
    "signed_by",
    "signed_at",
    "critic_report_path",
    "dod_count",
    "lock_reason",
    "skip_reason",
    "template_sha",
}


# ===== 错误码 =====

class StateError(Exception):
    """update_state 错误基类,所有错误带 ERR_XXX 编码。"""

    code: str = "ERR_UNKNOWN"

    def __init__(self, msg: str = ""):
        self.msg = msg
        super().__init__(f"[{self.code}] {msg}")


class InvalidTransitionError(StateError):
    code = "ERR_INVALID_TRANSITION"


class StateFileCorruptError(StateError):
    code = "ERR_STATE_FILE_CORRUPT"


class MissingRequiredFieldError(StateError):
    code = "ERR_MISSING_REQUIRED_FIELD"


class ConcurrentWriteError(StateError):
    code = "ERR_CONCURRENT_WRITE"


# ===== STATE.md 解析 / 序列化 =====

STATE_PATH = Path("docs/process/STATE.md")
PHASE_HEADERS = [f"## Phase {i}" for i in range(5)]

# Phase bullet 模式: "- 状态: <status>"
STATUS_RE = re.compile(r"^- 状态:\s*(\[[^\]]*\]|\[x\] LEGACY)\s*$")
BULLET_RE = re.compile(r"^- (.*?):\s*(.*)$")


def find_state_file(start: Path = Path(".")) -> Path:
    """从 start 向上找 docs/process/STATE.md,找不到抛 ERR_STATE_FILE_CORRUPT。"""
    cur = start.resolve()
    for _ in range(10):  # 最多向上 10 层
        candidate = cur / "docs" / "process" / "STATE.md"
        if candidate.exists():
            return candidate
        if cur.parent == cur:
            break
        cur = cur.parent
    raise StateFileCorruptError(
        f"未找到 docs/process/STATE.md(从 {start.resolve()} 向上搜 10 层)"
    )


def parse_state(state_path: Path) -> dict[int, dict[str, str]]:
    """解析 STATE.md 为 {phase: {key: value}}。"""
    if not state_path.exists():
        raise StateFileCorruptError(f"文件不存在: {state_path}")

    text = state_path.read_text(encoding="utf-8")
    result: dict[int, dict[str, str]] = {}
    current_phase: int | None = None

    for line in text.splitlines():
        line_stripped = line.rstrip()
        # 检测 phase 标题
        for i, header in enumerate(PHASE_HEADERS):
            if line_stripped.startswith(header):
                current_phase = i
                result[i] = {}
                break
        else:
            # 检测 bullet
            if current_phase is not None and line_stripped.startswith("- "):
                m = BULLET_RE.match(line_stripped)
                if m:
                    key, value = m.group(1).strip(), m.group(2).strip()
                    result[current_phase][key] = value

    if len(result) != 5:
        raise StateFileCorruptError(
            f"STATE.md 缺少 phase 段(期望 5 段,实际 {len(result)})"
        )

    return result


def serialize_state(state: dict[int, dict[str, str]], template: str) -> str:
    """把 {phase: bullets} 字典填回 STATE.md 模板。

    策略:检测到 phase header 时,写新 bullets,然后消耗原 phase 段所有内容(直到下一个
    phase header 或 EOF),不再追加原 bullets。
    """
    lines = template.splitlines(keepends=True)
    out: list[str] = []
    n = len(lines)
    i = 0

    while i < n:
        line = lines[i]
        line_stripped = line.rstrip()

        # 检测 phase 标题
        phase_idx = None
        for idx, header in enumerate(PHASE_HEADERS):
            if line_stripped.startswith(header):
                phase_idx = idx
                break

        if phase_idx is not None:
            # 在写新 phase header 前,确保前面有空行(保留模板的段间空行)
            if out and out[-1].rstrip() != "":
                out.append("\n")
            # 写 phase header
            out.append(line)
            # 写 header 后的空行(原模板在 header 与 bullets 之间有空行)
            out.append("\n")
            i += 1
            # 写新 bullets(按固定顺序,未在顺序里的 key 放末尾)
            bullets = state[phase_idx]
            ordered_keys = [
                "状态", "artifact", "追溯证据", "签字",
                "lock_reason", "skip_reason", "template_sha",
                "critic_report_path", "dod_count",
            ]
            written: set[str] = set()
            for key in ordered_keys:
                if key in bullets:
                    val = bullets[key].rstrip()
                    out.append(f"- {key}: {val}\n")
                    written.add(key)
            for key, val in bullets.items():
                if key not in written:
                    out.append(f"- {key}: {val.rstrip()}\n")
            # 消耗原 phase 段直到下一个 phase header 或 EOF
            while i < n:
                next_stripped = lines[i].rstrip()
                is_next_phase = any(
                    next_stripped.startswith(h) for h in PHASE_HEADERS
                )
                if is_next_phase:
                    break
                i += 1
            continue

        out.append(line)
        i += 1

    return "".join(out)


def get_current_status(phase_bullets: dict[str, str]) -> str:
    """从 phase bullets 提取当前 status,默认 [ ]。"""
    return phase_bullets.get("状态", "[ ]")


def check_transition(from_status: str, to_status: str) -> None:
    """检查状态转移合法性,非法抛 InvalidTransitionError。"""
    if to_status == "[x] LEGACY":
        raise InvalidTransitionError(
            f"不能用 update_state 写 [x] LEGACY(只允许 migrate_legacy_state.py 写)"
        )
    if from_status not in LEGAL_TRANSITIONS:
        raise InvalidTransitionError(f"未知当前状态: {from_status}")
    allowed = LEGAL_TRANSITIONS[from_status]
    if to_status not in allowed:
        raise InvalidTransitionError(
            f"非法转移: {from_status} → {to_status}(合法: {allowed or '无,终态'})"
        )


def check_required_kwargs(new_status: str, kwargs: dict[str, Any]) -> None:
    """检查目标状态必填 kwargs,缺抛 MissingRequiredFieldError。"""
    required = REQUIRED_KWARGS.get(new_status, set())
    missing = required - set(kwargs.keys())
    if missing:
        raise MissingRequiredFieldError(
            f"状态 {new_status} 缺必填字段: {missing}"
        )
    # date 格式校验
    if "signed_at" in kwargs:
        if not re.match(r"^\d{4}-\d{2}-\d{2}$", kwargs["signed_at"]):
            raise MissingRequiredFieldError(
                f"signed_at 格式错(期望 YYYY-MM-DD): {kwargs['signed_at']}"
            )
    # 未知 kwargs 警告
    unknown = set(kwargs.keys()) - VALID_KWARGS
    if unknown:
        print(f"  warn: 未知 kwargs {unknown}(会被忽略)", file=sys.stderr)


def atomic_write(path: Path, content: str) -> None:
    """原子写文件(.tmp + rename),POSIX 用 flock 防并发,Windows 退化为 no-op。"""
    import tempfile

    try:
        import fcntl  # type: ignore[import-not-found]
        _HAS_FCNTL = True
    except ImportError:  # Windows / 非 POSIX 系统
        _HAS_FCNTL = False

    tmp_fd, tmp_path = tempfile.mkstemp(
        prefix=".STATE.", suffix=".tmp", dir=path.parent
    )
    try:
        with open(tmp_fd, "w", encoding="utf-8") as f:
            f.write(content)
            if _HAS_FCNTL:
                try:
                    fcntl.flock(f, fcntl.LOCK_EX)  # type: ignore[possibly-undefined]
                except (BlockingIOError, OSError) as e:
                    raise ConcurrentWriteError(f"文件锁失败: {e}")
        Path(tmp_path).replace(path)
    except Exception:
        Path(tmp_path).unlink(missing_ok=True)
        raise


# ===== 主入口 =====

def update_state(phase: int, new_status: str, **kwargs: Any) -> str:
    """更新 STATE.md 的某 phase 状态。

    Args:
        phase: 0|1|2|3|4
        new_status: 6 个合法状态之一
        **kwargs: 见 VALID_KWARGS

    Returns:
        写成功的 STATE.md diff 字符串

    Raises:
        InvalidTransitionError / StateFileCorruptError /
        MissingRequiredFieldError / ConcurrentWriteError
    """
    if phase not in range(5):
        raise InvalidTransitionError(f"phase 越界(期望 0-4): {phase}")
    if new_status not in VALID_STATUSES:
        raise InvalidTransitionError(
            f"未知 new_status: {new_status}(合法: {VALID_STATUSES})"
        )

    # 1. 找 STATE.md
    state_path = find_state_file()

    # 2. 解析
    template = state_path.read_text(encoding="utf-8")
    state = parse_state(state_path)

    # 3. 状态机校验
    from_status = get_current_status(state[phase])
    check_transition(from_status, new_status)

    # 4. 必填字段校验
    check_required_kwargs(new_status, kwargs)

    # 5. 把新状态写回 in-memory state(否则 serialize_state 写不出变化)
    state[phase]["状态"] = new_status

    # 5. 合并 kwargs
    today = date.today().isoformat()
    for k, v in kwargs.items():
        if k in VALID_KWARGS:
            state[phase][k] = str(v)
    # 自动填 lock 时间
    if new_status == "[x]" and "signed_at" not in kwargs:
        state[phase]["signed_at"] = today
    # 记录解锁时间
    if new_status == "[UNLOCKED]":
        state[phase]["unlocked_at"] = today

    # 6. Cascade unlock: 解锁 N → 解锁 N+1..4(spec §3.4)
    if new_status == "[UNLOCKED]":
        for downstream in range(phase + 1, 5):
            ds_status = get_current_status(state[downstream])
            if ds_status in ("[x]", "[UNLOCKED]"):
                state[downstream]["状态"] = "[UNLOCKED]"
                # 下游统一标 "upstream re-opened",与原始 unlock_reason 区分
                state[downstream]["lock_reason"] = "upstream re-opened"
                state[downstream]["unlocked_at"] = today

    # 7. 序列化 + 原子写
    new_content = serialize_state(state, template)
    diff = make_diff(template, new_content)
    atomic_write(state_path, new_content)

    return diff


def make_diff(old: str, new: str) -> str:
    """生成 STATE.md 变更 diff(unified diff 格式)。"""
    import difflib

    diff = difflib.unified_diff(
        old.splitlines(keepends=True),
        new.splitlines(keepends=True),
        fromfile="STATE.md (before)",
        tofile="STATE.md (after)",
    )
    return "".join(diff)


# ===== CLI =====

def main() -> int:
    parser = argparse.ArgumentParser(
        description="pm-template STATE.md 写入 helper"
    )
    parser.add_argument("--phase", type=int, help="Phase 0-4")
    parser.add_argument("--status", help='新状态,如 "[x]" 或 "[UNLOCKED]"')
    parser.add_argument("--signed-by", dest="signed_by", help="签字人")
    parser.add_argument("--signed-at", dest="signed_at", help="签字日期 YYYY-MM-DD")
    parser.add_argument(
        "--critic-report", dest="critic_report_path", help="critic 报告路径"
    )
    parser.add_argument("--dod-count", dest="dod_count", help='DoD 计数,如 "12/12"')
    parser.add_argument("--lock-reason", dest="lock_reason", help="unlock 原因")
    parser.add_argument("--skip-reason", dest="skip_reason", help="skip 原因")
    parser.add_argument("--template-sha", dest="template_sha", help="pm-template git SHA")
    parser.add_argument(
        "--check", action="store_true", help="只解析 STATE.md 打印当前状态"
    )
    args = parser.parse_args()

    if args.check:
        try:
            state_path = find_state_file()
            state = parse_state(state_path)
        except StateError as e:
            print(f"✗ {e}", file=sys.stderr)
            return 1
        print(f"STATE.md: {state_path.resolve()}")
        for i in range(5):
            status = get_current_status(state[i])
            extra = ""
            if "signed_by" in state[i]:
                extra = f" by {state[i]['signed_by']} on {state[i].get('signed_at', '?')}"
            print(f"  Phase {i}: {status}{extra}")
        return 0

    if args.phase is None or args.status is None:
        parser.error("--phase 和 --status 必填(除非用 --check)")

    kwargs: dict[str, Any] = {}
    for field in (
        "signed_by",
        "signed_at",
        "critic_report_path",
        "dod_count",
        "lock_reason",
        "skip_reason",
        "template_sha",
    ):
        v = getattr(args, field)
        if v is not None:
            kwargs[field] = v

    try:
        diff = update_state(args.phase, args.status, **kwargs)
    except StateError as e:
        print(f"✗ {e}", file=sys.stderr)
        return 1

    print(f"✓ update_state(phase={args.phase}, status='{args.status}') 成功")
    if diff:
        print("\n--- diff ---")
        print(diff)
    return 0


if __name__ == "__main__":
    sys.exit(main())
