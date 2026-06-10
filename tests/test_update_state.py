"""test_update_state.py — update_state() 的 8 个 pytest 用例(详 spec §8)。

5 种合法转移 + 3 种非法转移 + cascade unlock 验证。
每个 test 用 tmp_path 隔离 STATE.md,不污染仓库根的 STATE.md。
"""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

# 让 import 找到 scripts/
SCRIPTS = Path(__file__).resolve().parent.parent / "scripts"
sys.path.insert(0, str(SCRIPTS))

from update_state import (  # noqa: E402
    InvalidTransitionError,
    MissingRequiredFieldError,
    StateFileCorruptError,
    find_state_file,
    get_current_status,
    parse_state,
    update_state,
)

# 仓库内已有的 STATE.md 模板(只读基线)
TEMPLATE_PATH = Path(__file__).resolve().parent.parent / "docs" / "process" / "STATE.md"
TEMPLATE_TEXT = TEMPLATE_PATH.read_text(encoding="utf-8")


@pytest.fixture
def work_dir(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    """每个 test 一个 tmp 目录,内含 docs/process/STATE.md(从模板复制)。"""
    monkeypatch.chdir(tmp_path)
    state_dir = tmp_path / "docs" / "process"
    state_dir.mkdir(parents=True)
    (state_dir / "STATE.md").write_text(TEMPLATE_TEXT, encoding="utf-8")
    return tmp_path


# ===== 5 种合法转移 =====


def test_legal_blank_to_in_progress(work_dir: Path) -> None:
    """合法:[ ] → [~]"""
    diff = update_state(0, "[~]")
    assert "[~]" in diff
    state = parse_state(find_state_file())
    assert get_current_status(state[0]) == "[~]"


def test_legal_in_progress_to_done(work_dir: Path) -> None:
    """合法:[~] → [x](需 signed_by / signed_at / template_sha)"""
    update_state(0, "[~]")
    diff = update_state(
        0,
        "[x]",
        signed_by="Alice",
        signed_at="2026-06-10",
        template_sha="abc1234",
    )
    assert "[x]" in diff
    state = parse_state(find_state_file())
    assert get_current_status(state[0]) == "[x]"
    assert state[0]["signed_by"] == "Alice"
    assert state[0]["signed_at"] == "2026-06-10"
    assert state[0]["template_sha"] == "abc1234"


def test_legal_done_to_unlocked(work_dir: Path) -> None:
    """合法:[x] → [UNLOCKED](需 lock_reason)+ cascade 解锁下游"""
    # 先把 phase 0/1/2 锁到 [x]
    for p in range(3):
        update_state(p, "[~]")
        update_state(
            p,
            "[x]",
            signed_by="Alice",
            signed_at="2026-06-10",
            template_sha="abc1234",
        )
    # 解锁 phase 1
    diff = update_state(1, "[UNLOCKED]", lock_reason="接口清单要改")
    assert "[UNLOCKED]" in diff
    state = parse_state(find_state_file())
    assert get_current_status(state[1]) == "[UNLOCKED]"
    # cascade:phase 2 也得是 [UNLOCKED]
    assert get_current_status(state[2]) == "[UNLOCKED]"
    assert state[2]["lock_reason"] == "upstream re-opened"


def test_legal_unlocked_back_to_in_progress(work_dir: Path) -> None:
    """合法:[UNLOCKED] → [~]"""
    # 先把 phase 0 锁 → 解锁 → 回到 [~]
    update_state(0, "[~]")
    update_state(
        0, "[x]", signed_by="Alice", signed_at="2026-06-10", template_sha="abc"
    )
    update_state(0, "[UNLOCKED]", lock_reason="改")
    diff = update_state(0, "[~]")
    assert "[~]" in diff
    state = parse_state(find_state_file())
    assert get_current_status(state[0]) == "[~]"


def test_legal_blank_to_skip(work_dir: Path) -> None:
    """合法:[ ] → [SKIP](需 skip_reason)"""
    diff = update_state(2, "[SKIP]", skip_reason="本项目无第三方集成需求")
    assert "[SKIP]" in diff
    state = parse_state(find_state_file())
    assert get_current_status(state[2]) == "[SKIP]"
    assert state[2]["skip_reason"] == "本项目无第三方集成需求"


# ===== 3 种非法转移 =====


def test_illegal_done_to_in_progress(work_dir: Path) -> None:
    """非法:[x] → [~](必须先 [UNLOCKED])"""
    update_state(0, "[~]")
    update_state(
        0, "[x]", signed_by="Alice", signed_at="2026-06-10", template_sha="abc"
    )
    with pytest.raises(InvalidTransitionError) as exc:
        update_state(0, "[~]")
    assert "ERR_INVALID_TRANSITION" in str(exc.value)
    assert "[x]" in str(exc.value)


def test_illegal_blank_to_done(work_dir: Path) -> None:
    """非法:[ ] → [x](必须经过 [~])"""
    with pytest.raises(InvalidTransitionError) as exc:
        update_state(
            0, "[x]", signed_by="Alice", signed_at="2026-06-10", template_sha="abc"
        )
    assert "ERR_INVALID_TRANSITION" in str(exc.value)


def test_illegal_legacy_terminal(work_dir: Path) -> None:
    """非法:[x] LEGACY → 任何状态(终态,即使 migrate_legacy_state.py 写完后也不能改)"""
    # 手动把 phase 3 改成 [x] LEGACY 模拟历史包袱
    state = parse_state(find_state_file())
    state[3]["状态"] = "[x] LEGACY"
    from update_state import serialize_state, atomic_write

    new_content = serialize_state(state, TEMPLATE_TEXT)
    atomic_write(find_state_file(), new_content)

    with pytest.raises(InvalidTransitionError) as exc:
        update_state(3, "[UNLOCKED]", lock_reason="试图解锁历史")
    assert "ERR_INVALID_TRANSITION" in str(exc.value)


# ===== 必填字段校验(额外护栏) =====


def test_missing_required_fields_for_done(work_dir: Path) -> None:
    """[x] 缺 signed_by / signed_at / template_sha 应抛 MissingRequiredFieldError。"""
    update_state(0, "[~]")
    with pytest.raises(MissingRequiredFieldError) as exc:
        update_state(0, "[x]")  # 缺 3 个必填
    assert "ERR_MISSING_REQUIRED_FIELD" in str(exc.value)
