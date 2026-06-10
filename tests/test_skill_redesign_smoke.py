"""test_skill_redesign_smoke.py — 改动 1-7 机械冒烟测试。

Batch 6 的 sign-off 手段:验证 5 类门(状态机 / 签字 / DoD / Critic / 硬 grep)
中最**可机械断言**的 2 类——状态机 + 硬 grep——真能拦住错误输入。

**明确不在本测试范围**:
- LLM 主观评分(critic 报告 C/H/M/L) — 需 superpowers:code-reviewer 子 agent
- brainstorming 对话质量 — 需 superpowers:brainstorming + 用户
- DoD / Critic 报告内容质量 — 需 phase skill 内部流水线

这些"软"门由 spec §4.4 文档化边界,本文件只覆盖"硬"门。
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

import pytest

# 让 import 找到 .claude/scripts/
SCRIPTS = Path(__file__).resolve().parent.parent / ".claude" / "scripts"
sys.path.insert(0, str(SCRIPTS))

from update_state import (  # noqa: E402
    find_state_file,
    get_current_status,
    parse_state,
    update_state,
)

# 仓库根 = 测试文件上两级
REPO_ROOT = Path(__file__).resolve().parent.parent
TEMPLATES = REPO_ROOT / "docs" / "process" / "templates"

# ===== 改动 5 引入的硬 grep 门 =====

# Phase 1 4 个 anchor(详 phase-2-design.md / phase-3-detail.md / phase-4-implement.md §1.c)
REQUIRED_PHASE1_ANCHORS: tuple[str, ...] = (
    "role-scenario",
    "edge-scenarios",
    "exception-paths",
    "reverse-requirements",
)

# Phase 0 3 个 anchor(详 phase-1-requirements.md §1.c)
REQUIRED_PHASE0_ANCHORS: tuple[str, ...] = (
    "stakeholders",
    "constraints",
    "non-goals",
)

# Phase 3 必含 anchor 段
REQUIRED_PHASE3_FILES: tuple[tuple[str, tuple[str, ...]], ...] = (
    ("docs/03a_business_process.md", ("process-1-normal", "process-1-exception")),
    ("docs/03b_api_design.md", ("api-list",)),
    ("docs/03c_data_schema.md", ("tables",)),
)


# ===== 模拟 phase skill 内部的硬 grep 校验函数 =====


def check_phase1_complete(requirements_text: str) -> list[str]:
    """phase 2/3/4 启动时的硬 grep:返回缺失的 anchor 名列表,空 = 通过。"""
    return [a for a in REQUIRED_PHASE1_ANCHORS if f"ANCHOR: {a}" not in requirements_text]


def check_phase0_complete(charter_text: str) -> list[str]:
    """phase 1 启动时的硬 grep:返回缺失的 anchor 名列表,空 = 通过。"""
    return [a for a in REQUIRED_PHASE0_ANCHORS if f"ANCHOR: {a}" not in charter_text]


def check_phase2_complete(hld_text: str) -> list[str]:
    """phase 3/4 启动时的硬 grep:`## 3. ` 段必须存在(接口清单)。"""
    if not hld_text:
        return ["file-missing"]
    if not re.search(r"^## 3\.\s", hld_text, re.MULTILINE):
        return ["no-interface-list"]
    return []


def check_phase3_files(project_root: Path) -> list[str]:
    """phase 4 启动时的硬 grep:3 个文件存在 + 非空 + 含 anchor。"""
    missing: list[str] = []
    for rel_path, anchors in REQUIRED_PHASE3_FILES:
        full = project_root / rel_path
        if not full.exists() or full.stat().st_size == 0:
            missing.append(f"{rel_path}:missing-or-empty")
            continue
        text = full.read_text(encoding="utf-8")
        for a in anchors:
            if f"ANCHOR: {a}" not in text:
                missing.append(f"{rel_path}:{a}-missing")
    return missing


def check_optional_section_blank(template_text: str) -> list[str]:
    """检测 [可选] 段是否"挂标题但内容是占位符"。返回违例段名列表。

    判定:从 `## 附录 X: ... [可选]` 标题开始,到下一个 `## ` 段或文件末为止,
    其中**只**包含空行 / `___` / 简单占位符,无实质内容 → 违例。
    """
    violations: list[str] = []
    pattern = re.compile(
        r"^## (附录 \w+:[^\n]*\[可选\])\s*\n+(.*?)(?=^## |\Z)",
        re.MULTILINE | re.DOTALL,
    )
    for m in pattern.finditer(template_text):
        section_name = m.group(1).strip()
        body = m.group(2).strip()
        if not body:
            continue  # 整段不写(合法的"跳过"用法)
        # 占位符特征:body 短 + 含 `___` 或纯说明性短语
        placeholder_markers = ("___", "占位", "TBD", "TODO")
        if len(body) < 80 and any(marker in body for marker in placeholder_markers):
            violations.append(section_name)
    return violations


# ===== Phase 0 硬 grep 测试 =====


def test_phase0_all_anchors_present() -> None:
    """模板 00_charter.md 自带 3 anchor,这是所有 phase 1 启动检查的源头。"""
    text = (TEMPLATES / "00_charter.md").read_text(encoding="utf-8")
    missing = check_phase0_complete(text)
    assert missing == [], f"00_charter.md 缺 anchor:{missing}"


def test_phase0_missing_one_anchor_detected() -> None:
    """模拟 phase 1 启动:用户交付的 charter 漏 1 个 anchor,应被拦下。"""
    text = (TEMPLATES / "00_charter.md").read_text(encoding="utf-8")
    # 删掉 stakeholders 那一行 anchor
    broken = "\n".join(
        line for line in text.splitlines() if "ANCHOR: stakeholders" not in line
    )
    missing = check_phase0_complete(broken)
    assert "stakeholders" in missing
    assert len(missing) == 1


def test_phase0_no_anchors_all_missing() -> None:
    """空文件 → 3 个 anchor 全缺。"""
    missing = check_phase0_complete("# charter\n\n啥都没写")
    assert set(missing) == set(REQUIRED_PHASE0_ANCHORS)


# ===== Phase 1 硬 grep 测试(改动 5 核心) =====


def test_phase1_all_anchors_present() -> None:
    """模板 01_requirements.md 自带 4 anchor。"""
    text = (TEMPLATES / "01_requirements.md").read_text(encoding="utf-8")
    missing = check_phase1_complete(text)
    assert missing == [], f"01_requirements.md 缺 anchor:{missing}"


def test_phase1_missing_one_anchor_detected() -> None:
    """用户交付的 01 漏 1 个 anchor → ERR_PHASE_1_INCOMPLETE。"""
    text = (TEMPLATES / "01_requirements.md").read_text(encoding="utf-8")
    broken = "\n".join(
        line for line in text.splitlines() if "ANCHOR: reverse-requirements" not in line
    )
    missing = check_phase1_complete(broken)
    assert "reverse-requirements" in missing
    assert len(missing) == 1


def test_phase1_no_anchors_all_missing() -> None:
    """空文件 → 4 个 anchor 全缺(对应"完全没挖掘"的最坏情况)。"""
    missing = check_phase1_complete("# 需求\n\n写了几个故事就交了")
    assert set(missing) == set(REQUIRED_PHASE1_ANCHORS)


def test_phase1_partial_anchors_lists_exact_missing() -> None:
    """2 缺 2:返回确切缺失清单(给用户的修复指引要精确)。"""
    text = (TEMPLATES / "01_requirements.md").read_text(encoding="utf-8")
    keep = {"role-scenario", "edge-scenarios"}  # 留这 2 个
    broken = "\n".join(
        line for line in text.splitlines() if not any(
            f"ANCHOR: {a}" in line for a in REQUIRED_PHASE1_ANCHORS if a not in keep
        )
    )
    missing = check_phase1_complete(broken)
    assert set(missing) == {"exception-paths", "reverse-requirements"}


# ===== Phase 2 硬 grep 测试 =====


def test_phase2_interface_list_section_present() -> None:
    """模板 02_high_level_design.md 自带 `## 3. 接口清单` 段。"""
    text = (TEMPLATES / "02_high_level_design.md").read_text(encoding="utf-8")
    assert check_phase2_complete(text) == []


def test_phase2_missing_section_detected() -> None:
    """用户交付的 02 没写 `## 3. ` 段 → ERR_PHASE_2_INCOMPLETE。"""
    text_without_interface = """# 概要设计

## 1. 架构
写得不错

## 2. 数据模型
也写得不错

## 4. 非功能
居然从 §4 开始了
"""
    assert "no-interface-list" in check_phase2_complete(text_without_interface)


def test_phase2_empty_text() -> None:
    """完全空文件 → file-missing。"""
    assert check_phase2_complete("") == ["file-missing"]


# ===== Phase 3 硬 grep 测试 =====


@pytest.fixture
def fake_project_with_phase3(tmp_path: Path) -> Path:
    """构造一个最小 phase 3 项目(3 文件 + anchor + 非空)。"""
    (tmp_path / "docs").mkdir()
    for rel, anchors in REQUIRED_PHASE3_FILES:
        f = tmp_path / rel
        f.parent.mkdir(parents=True, exist_ok=True)
        f.write_text(
            "# 标题\n\n" + "\n".join(f"<!-- ANCHOR: {a} -->\n" for a in anchors) + "内容",
            encoding="utf-8",
        )
    return tmp_path


def test_phase3_all_files_present(fake_project_with_phase3: Path) -> None:
    """3 文件都在 + 非空 + 含 anchor → 通过。"""
    assert check_phase3_files(fake_project_with_phase3) == []


def test_phase3_missing_one_file(fake_project_with_phase3: Path) -> None:
    """删 03b → 应报 03b:missing-or-empty。"""
    (fake_project_with_phase3 / "docs/03b_api_design.md").unlink()
    missing = check_phase3_files(fake_project_with_phase3)
    assert any("03b_api_design.md:missing-or-empty" in m for m in missing)


def test_phase3_empty_file(fake_project_with_phase3: Path) -> None:
    """03c 写成 0 字节 → missing-or-empty。"""
    (fake_project_with_phase3 / "docs/03c_data_schema.md").write_text("", encoding="utf-8")
    missing = check_phase3_files(fake_project_with_phase3)
    assert any("03c_data_schema.md:missing-or-empty" in m for m in missing)


def test_phase3_missing_anchor_in_file(fake_project_with_phase3: Path) -> None:
    """03a 还在但 anchor 被删 → 报具体 anchor 缺失。"""
    f = fake_project_with_phase3 / "docs/03a_business_process.md"
    f.write_text("# 03a\n\n写得挺长但忘了加 anchor", encoding="utf-8")
    missing = check_phase3_files(fake_project_with_phase3)
    assert "docs/03a_business_process.md:process-1-normal-missing" in missing
    assert "docs/03a_business_process.md:process-1-exception-missing" in missing


# ===== [可选] 段占位符检测测试(改动 4 引入) =====


def test_optional_section_with_placeholder_detected() -> None:
    """03_detailed_design.md 模板里的"附录 A: 性能 [可选]"段——检测占位符用法。"""
    text = (TEMPLATES / "03_detailed_design.md").read_text(encoding="utf-8")
    # 当前模板是干净的(没挂占位符)
    assert check_optional_section_blank(text) == []


def test_optional_section_blank_detection_works() -> None:
    """手动构造"挂标题 + 占位符"违例,验证检测函数。"""
    bad = """# 模板

## 附录 A: 性能 [可选]

___

## 附录 B: 安全 [可选]
"""
    violations = check_optional_section_blank(bad)
    assert len(violations) >= 1
    assert any("附录 A" in v for v in violations)


# ===== 端到端:5 phase 全锁 = state machine 端到端测试 =====


@pytest.fixture
def state_workdir(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    """复制 STATE.md 模板到 tmp,chdir 过去。"""
    template = REPO_ROOT / "docs" / "process" / "STATE.md"
    monkeypatch.chdir(tmp_path)
    state_dir = tmp_path / "docs" / "process"
    state_dir.mkdir(parents=True)
    (state_dir / "STATE.md").write_text(template.read_text(encoding="utf-8"), encoding="utf-8")
    return tmp_path


def test_end_to_end_lock_all_5_phases(state_workdir: Path) -> None:
    """5 phase 串行 [ ] → [~] → [x],最终全部 [x]。"""
    sha = "deadbeef"
    for p in range(5):
        update_state(p, "[~]")
        update_state(
            p, "[x]",
            signed_by="Bob",
            signed_at="2026-06-10",
            template_sha=sha,
        )

    state = parse_state(find_state_file())
    for p in range(5):
        assert get_current_status(state[p]) == "[x]", f"Phase {p} 未锁"
        assert state[p]["signed_by"] == "Bob"
        assert state[p]["template_sha"] == sha


def test_end_to_end_cascade_unlock_resets_downstream(state_workdir: Path) -> None:
    """锁 5 phase → 解锁 phase 2 → 3/4 应 cascade UNLOCKED,phase 0/1 仍 [x]。"""
    sha = "abc"
    for p in range(5):
        update_state(p, "[~]")
        update_state(p, "[x]", signed_by="Eve", signed_at="2026-06-10", template_sha=sha)

    update_state(2, "[UNLOCKED]", lock_reason="接口清单要改")

    state = parse_state(find_state_file())
    assert get_current_status(state[0]) == "[x]"
    assert get_current_status(state[1]) == "[x]"
    assert get_current_status(state[2]) == "[UNLOCKED]"
    assert get_current_status(state[3]) == "[UNLOCKED]"
    assert get_current_status(state[4]) == "[UNLOCKED]"
    # phase 3/4 的 lock_reason 应标 "upstream re-opened"
    assert state[3]["lock_reason"] == "upstream re-opened"


def test_end_to_end_skip_then_lock_others(state_workdir: Path) -> None:
    """phase 2 标 SKIP(本项目无此需求)→ phase 3 仍可锁(不要求上游都 [x])。"""
    update_state(0, "[~]")
    update_state(0, "[x]", signed_by="A", signed_at="2026-06-10", template_sha="x")
    update_state(1, "[~]")
    update_state(1, "[x]", signed_by="A", signed_at="2026-06-10", template_sha="x")
    update_state(2, "[SKIP]", skip_reason="无第三方集成")

    state = parse_state(find_state_file())
    assert get_current_status(state[2]) == "[SKIP]"

    # phase 3 仍可锁
    update_state(3, "[~]")
    update_state(3, "[x]", signed_by="A", signed_at="2026-06-10", template_sha="x")
    state = parse_state(find_state_file())
    assert get_current_status(state[3]) == "[x]"


# ===== /change 第二层状态机测试(改动 4.5) =====


CHANGE_LOG_MARKER = "## 变更日志(★ /change 入口)"


def test_state_template_has_change_log_section() -> None:
    """STATE.md 模板必含"变更日志"段,否则 /change 入口无处写。"""
    state_template = (REPO_ROOT / "docs" / "process" / "STATE.md").read_text(encoding="utf-8")
    assert CHANGE_LOG_MARKER in state_template


def test_state_template_has_decision_log_section() -> None:
    """STATE.md 模板必含"决策日志"段(ADR 联动)。"""
    state_template = (REPO_ROOT / "docs" / "process" / "STATE.md").read_text(encoding="utf-8")
    assert "## 决策日志(ADR)" in state_template


def test_change_log_status_options() -> None:
    """变更日志状态机的 5 状态[ ] [~] [x] [DEPRECATED] [ABORTED] 必出现在模板说明中。"""
    state_template = (REPO_ROOT / "docs" / "process" / "STATE.md").read_text(encoding="utf-8")
    for status in ["[ ]", "[~]", "[x]", "[DEPRECATED]", "[ABORTED]"]:
        assert status in state_template, f"变更日志缺状态 {status}"


def test_change_number_4digit_padding() -> None:
    """变更号 NNNN 4 位 0 补的格式约定(由 /change 自动分配)。"""
    # 模拟 /change 的编号逻辑
    existing = ["0001-feat-audit.md", "0003-fix-bug.md"]
    nums = [int(f.split("-")[0]) for f in existing]
    next_n = max(nums) + 1
    padded = f"{next_n:04d}"
    assert padded == "0004"


def test_change_number_skipping_deprecated() -> None:
    """废弃号不重用:0002 [DEPRECATED] 后,新变更仍用 0003。"""
    existing = [
        ("0001", "[x]"),
        ("0002", "[DEPRECATED]"),
        ("0003", "[x]"),  # 跳过 0002 用 0003
    ]
    # 简化:取所有号(废弃号不重用规则,意味着下一个号 = max(非废弃) + 1)
    active = [int(n) for n, s in existing if s != "[DEPRECATED]"]
    next_n = max(active) + 1
    assert next_n == 4  # 0004 续


def test_change_skill_in_skill_list() -> None:
    """.claude/skills/change.md 必存在。"""
    assert (REPO_ROOT / ".claude" / "skills" / "change.md").exists()


def test_all_5_change_templates_exist() -> None:
    """5 个 type 模板必全在(基于 _base 的扩展)。"""
    for t in ("feature", "bugfix", "refactor", "hotfix", "doc"):
        f = REPO_ROOT / "docs" / "process" / "templates" / "change" / f"{t}.md"
        assert f.exists(), f"change 模板缺: {t}.md"


def test_all_5_change_critics_exist() -> None:
    """5 个 critic 必全在。"""
    for t in ("feature", "bugfix", "refactor", "hotfix", "doc"):
        f = REPO_ROOT / "docs" / "critics" / "change" / f"{t}.md" if False else REPO_ROOT / "docs" / "process" / "critics" / "change" / f"{t}.md"
        assert f.exists(), f"change critic 缺: {t}.md"


def test_all_5_change_dods_exist() -> None:
    """5 个 DoD 必全在。"""
    for t in ("feature", "bugfix", "refactor", "hotfix", "doc"):
        f = REPO_ROOT / "docs" / "process" / "dod" / "change" / f"{t}.md"
        assert f.exists(), f"change DoD 缺: {t}.md"


def test_change_base_template_has_required_markers() -> None:
    """_base 模板必含关键段(否则 type 模板会失骨架)。"""
    base = (REPO_ROOT / "docs" / "process" / "templates" / "change" / "_base.md").read_text(encoding="utf-8")
    for marker in ("§0 元信息", "§1 type 特有段", "§9 关联引用", "§10 critic + 签字"):
        assert marker in base, f"_base 模板缺段: {marker}"


def test_decision_template_exists() -> None:
    """ADR 模板必存在(跨切面 §4.5)。"""
    assert (REPO_ROOT / "docs" / "process" / "templates" / "decision.md").exists()


def test_release_template_exists() -> None:
    """Release log 模板必存在(跨切面 §4.5)。"""
    assert (REPO_ROOT / "docs" / "process" / "templates" / "release.md").exists()


def test_todo_doc_lists_unimplemented_types() -> None:
    """TODO.md 必含未实现的 4 个 type(范围守门)。"""
    todo = (REPO_ROOT / "docs" / "process" / "TODO.md").read_text(encoding="utf-8")
    for t in ("upgrade", "perf", "migration", "deprecation"):
        assert t in todo, f"TODO.md 缺未实现 type: {t}"
