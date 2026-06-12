"""audit.py — 对已实现功能做 5 项机械审查,生成报告。

唯一合法读 `docs/STATE.md` 之外的产物文档(01/03b/代码/tests)的入口,
目标项目用 `/audit` 触发。报告写 `docs/audit/reports/audit_<DATE>.md`。

5 项检查(全 grep/diff,无 LLM):
1. AC 覆盖率:01_requirements.md 的 AC 编号 → 必在 tests/ e2e_*.sh 出现
2. 范围蔓延:app/ 的 @router 装饰器 → 必在 03b_api_design.md 出现
3. 反向需求真没做:01 §5 关键词 → 代码中 0 命中
4. 接口一致性:03b path/method → 必与代码 100% 一致
5. 单测覆盖:tests/ test_*.py → 必覆盖 03b 每个接口

注:tests/ 缺失时,1 + 5 自动 N/A(目标项目尚未引入测试,不算 fail)。

CLI 用法:
    python .claude/skills/_lib/audit.py                       # 跑全 5 项
    python .claude/skills/_lib/audit.py --ac-only             # 只 AC 覆盖
    python .claude/skills/_lib/audit.py --scope-creep         # 只范围蔓延
    python .claude/skills/_lib/audit.py --report-path X      # 写自定义报告路径
    python .claude/skills/_lib/audit.py --check               # 只跑不写报告(返回 exit code)
"""

from __future__ import annotations

import argparse
import re
import sys
from datetime import date
from pathlib import Path
from typing import Any

# ===== 路径配置 =====

REPO_ROOT = Path(".")
PHASE1_REQUIREMENTS = REPO_ROOT / "docs" / "01_requirements.md"
PHASE3B_API_DESIGN = REPO_ROOT / "docs" / "03b_api_design.md"
CODE_DIRS = ["app", "src", "backend"]  # 至少一个存在
TEST_DIRS = ["tests"]
E2E_SCRIPTS = REPO_ROOT / "scripts"
REPORT_DIR = REPO_ROOT / "docs" / "audit" / "reports"

# ===== 错误码 =====

ERR_NO_ARTIFACT = 1
ERR_PHASE_MISSING = 2


# ===== 5 项检查 =====


def extract_ac_numbers(text: str) -> list[str]:
    """从 01_requirements.md 提取所有 AC-NNN 编号。"""
    return sorted(set(re.findall(r"\bAC-\d+\b", text)))


def extract_section5_keywords(text: str) -> list[str]:
    """从 01_requirements.md §5 反向需求提取关键能力词。

    §5 格式通常是: "❌ 不做 X" / "❌ 不做 Y"
    提取 "X" / "Y" 部分作为关键词。
    """
    keywords: list[str] = []
    # 找 §5 段(到下一个 §X 或文件末)
    m = re.search(r"##\s*5\..*?(?=\n##\s|\Z)", text, re.DOTALL)
    if not m:
        return keywords
    section5 = m.group(0)
    # 提取 ❌ 不做 X 模式
    for line in section5.splitlines():
        line = line.strip()
        # 模式: "❌ 不做 X" / "❌ 不做 X(原因: ...)"
        m2 = re.match(r"[❌\-*]\s*不做\s*(.+?)(?:\(|（|$)", line)
        if m2:
            keyword = m2.group(1).strip()
            if keyword and len(keyword) <= 50:  # 排除过长
                keywords.append(keyword)
    return keywords


def extract_03b_interfaces(text: str) -> list[dict[str, str]]:
    """从 03b_api_design.md 提取接口清单。

    返回 [{"path": "/api/v1/xxx", "method": "POST", "id": "B.1"}, ...]
    """
    interfaces: list[dict[str, str]] = []
    # 找接口清单段(简化:扫整个文件,匹配 "B.X 路径 方法")
    pattern = re.compile(
        r"\|\s*(B\.\d+)\s*\|\s*[`']?(GET|POST|PATCH|DELETE|PUT)\s+([^\s`'|<]+)[`']?\s*\|",
        re.IGNORECASE,
    )
    for m in pattern.finditer(text):
        interfaces.append({
            "id": m.group(1),
            "method": m.group(2).upper(),
            "path": m.group(3),
        })
    return interfaces


def extract_code_routes() -> list[dict[str, str]]:
    """从 app/ src/ 提取 @router 装饰器的 path + method。

    支持 FastAPI(@router.get/post/...)与 Flask(@app.route)。
    """
    routes: list[dict[str, str]] = []
    # 扫 code 目录
    for code_dir in CODE_DIRS:
        cd = REPO_ROOT / code_dir
        if not cd.exists():
            continue
        for py in cd.rglob("*.py"):
            try:
                text = py.read_text(encoding="utf-8", errors="ignore")
            except Exception:
                continue
            # @router.get("/path") / @app.route("/path", methods=["POST"])
            for m in re.finditer(
                r"@(?:router|app)\.(get|post|put|patch|delete)\(\s*['\"]([^'\"]+)['\"]",
                text,
                re.IGNORECASE,
            ):
                routes.append({
                    "method": m.group(1).upper(),
                    "path": m.group(2),
                    "file": str(py),
                })
            # Flask: @app.route("/path", methods=["POST"])
            for m in re.finditer(
                r"@\w+\.route\(\s*['\"]([^'\"]+)['\"].*?methods\s*=\s*\[([^\]]+)\]",
                text,
                re.IGNORECASE,
            ):
                methods = re.findall(r"['\"]([A-Z]+)['\"]", m.group(2), re.IGNORECASE)
                for method in methods:
                    if method.upper() != "GET":  # GET 是 Flask 默认
                        routes.append({
                            "method": method.upper(),
                            "path": m.group(1),
                            "file": str(py),
                        })
    return routes


def find_e2e_and_test_files() -> list[Path]:
    """找所有 e2e 脚本 + 测试文件。"""
    files: list[Path] = []
    for test_dir in TEST_DIRS:
        td = REPO_ROOT / test_dir
        if td.exists():
            files.extend(td.rglob("*.py"))
    if E2E_SCRIPTS.exists():
        files.extend(E2E_SCRIPTS.rglob("e2e_*.sh"))
    return files


def tests_present() -> bool:
    """tests/ 目录(或 e2e 脚本)是否存在。缺失时,AC 覆盖 + 单测覆盖项 N/A。"""
    for test_dir in TEST_DIRS:
        if (REPO_ROOT / test_dir).exists():
            return True
    if E2E_SCRIPTS.exists():
        return True
    return False


# ===== 单项检查 =====


def check_ac_coverage(ph1_text: str) -> dict[str, Any]:
    """检查 1: AC 覆盖率。每个 AC-NNN 必在 tests/ e2e_*.sh 出现至少 1 次。

    tests/ 缺失 → N/A(不报错,提示用户补 tests/ 后再跑)。
    """
    if not tests_present():
        return {
            "name": "AC 覆盖率",
            "level": "N/A",
            "total": 0,
            "covered": 0,
            "missing": [],
            "note": "tests/ 与 scripts/e2e_*.sh 均不存在,跳过此项(目标项目尚未引入测试?)",
        }
    ac_list = extract_ac_numbers(ph1_text)
    test_files = find_e2e_and_test_files()
    test_texts: list[str] = []
    for f in test_files:
        try:
            test_texts.append(f.read_text(encoding="utf-8", errors="ignore"))
        except Exception:
            pass
    combined = "\n".join(test_texts)

    missing = [ac for ac in ac_list if ac not in combined]
    return {
        "name": "AC 覆盖率",
        "level": "CRITICAL" if missing else "PASS",
        "total": len(ac_list),
        "covered": len(ac_list) - len(missing),
        "missing": missing,
    }


def check_scope_creep(ph3b_text: str) -> dict[str, Any]:
    """检查 2: 范围蔓延。app/ 的 @router 必在 03b 出现。"""
    interfaces = extract_03b_interfaces(ph3b_text)
    code_routes = extract_code_routes()
    defined = {(i["method"], i["path"]) for i in interfaces}
    defined_paths = {i["path"] for i in interfaces}

    # 多出 = code 有但 03b 没记
    creep = [r for r in code_routes if (r["method"], r["path"]) not in defined]
    return {
        "name": "范围蔓延",
        "level": "CRITICAL" if creep else "PASS",
        "code_routes_count": len(code_routes),
        "defined_count": len(defined),
        "creep": creep[:20],  # 最多报 20 条
    }


def check_reverse_requirements(ph1_text: str) -> dict[str, Any]:
    """检查 3: 反向需求真没做。§5 关键词在代码中 0 命中。"""
    keywords = extract_section5_keywords(ph1_text)
    hits: list[dict[str, str]] = []
    for code_dir in CODE_DIRS:
        cd = REPO_ROOT / code_dir
        if not cd.exists():
            continue
        for py in cd.rglob("*.py"):
            try:
                text = py.read_text(encoding="utf-8", errors="ignore")
            except Exception:
                continue
            for kw in keywords:
                if kw and kw in text:
                    hits.append({"keyword": kw, "file": str(py)})
    return {
        "name": "反向需求真没做",
        "level": "CRITICAL" if hits else "PASS",
        "keywords_count": len(keywords),
        "hits": hits[:20],
    }


def check_interface_consistency(ph3b_text: str) -> dict[str, Any]:
    """检查 4: 接口一致性。03b 必与代码 100% 一致。"""
    interfaces = extract_03b_interfaces(ph3b_text)
    code_routes = extract_code_routes()
    code_set = {(r["method"], r["path"]) for r in code_routes}
    defined_set = {(i["method"], i["path"]) for i in interfaces}

    # 03b 写了但代码无
    missing_in_code = sorted(defined_set - code_set)
    return {
        "name": "接口一致性",
        "level": "HIGH" if missing_in_code else "PASS",
        "defined_count": len(defined_set),
        "coded_count": len(code_set),
        "missing_in_code": [
            {"method": m, "path": p} for m, p in missing_in_code
        ][:20],
    }


def check_test_coverage(ph3b_text: str) -> dict[str, Any]:
    """检查 5: 单测覆盖。tests/ 必覆盖 03b 每个接口。

    tests/ 缺失 → N/A(不报错)。
    """
    if not tests_present():
        return {
            "name": "单测覆盖",
            "level": "N/A",
            "interfaces_count": 0,
            "uncovered": [],
            "note": "tests/ 与 scripts/e2e_*.sh 均不存在,跳过此项",
        }
    interfaces = extract_03b_interfaces(ph3b_text)
    test_files = find_e2e_and_test_files()
    test_texts: list[str] = []
    for f in test_files:
        try:
            test_texts.append(f.read_text(encoding="utf-8", errors="ignore"))
        except Exception:
            pass
    combined = "\n".join(test_texts)

    uncovered = []
    for iface in interfaces:
        # 找 path 关键词(去掉 /api/v1/ 前缀)
        path_key = iface["path"].rstrip("/").split("/")[-1]
        if not path_key or path_key not in combined:
            uncovered.append(iface)
    return {
        "name": "单测覆盖",
        "level": "MEDIUM" if uncovered else "PASS",
        "interfaces_count": len(interfaces),
        "uncovered": uncovered[:20],
    }


# ===== 主流程 =====


def run_audit(checks: list[str] | None = None) -> dict[str, Any]:
    """跑审计检查,返回结果字典。

    Args:
        checks: None = 跑全 5 项;否则只跑指定的(ac-coverage / scope-creep /
                reverse-req / interface / test-coverage)
    """
    all_checks = {
        "ac-coverage": check_ac_coverage,
        "scope-creep": check_scope_creep,
        "reverse-req": check_reverse_requirements,
        "interface": check_interface_consistency,
        "test-coverage": check_test_coverage,
    }
    if checks is None:
        checks = list(all_checks.keys())

    # 读产物
    artifacts = {}
    if not PHASE1_REQUIREMENTS.exists():
        return {"error": f"未找到 {PHASE1_REQUIREMENTS}(phase 1 产物未生成?)", "code": ERR_NO_ARTIFACT}
    if not PHASE3B_API_DESIGN.exists():
        return {"error": f"未找到 {PHASE3B_API_DESIGN}(phase 3b 产物未生成?)", "code": ERR_NO_ARTIFACT}

    artifacts["ph1"] = PHASE1_REQUIREMENTS.read_text(encoding="utf-8")
    artifacts["ph3b"] = PHASE3B_API_DESIGN.read_text(encoding="utf-8")

    results = {}
    for check_name in checks:
        fn = all_checks[check_name]
        results[check_name] = fn(artifacts["ph1"] if check_name in ("ac-coverage", "reverse-req") else artifacts["ph3b"])

    # 决定 overall 等级(N/A 视同 PASS,不污染 overall)
    level_priority = {"N/A": 0, "PASS": 0, "MEDIUM": 1, "HIGH": 2, "CRITICAL": 3}
    overall = "PASS"
    for r in results.values():
        if level_priority.get(r["level"], 0) > level_priority[overall]:
            overall = r["level"]

    return {"overall": overall, "results": results, "code": 0 if overall == "PASS" else 1}


def render_report(audit: dict[str, Any]) -> str:
    """渲染审计报告(markdown)。"""
    today = date.today().isoformat()
    lines = [f"# Audit Report — {today}\n"]
    lines.append(f"**Overall**: {audit['overall']}\n")
    lines.append("**检查项**:\n")
    for name, r in audit["results"].items():
        lines.append(f"- **{r['name']}**({name}): `{r['level']}`")
    lines.append("\n---\n")
    for name, r in audit["results"].items():
        lines.append(f"\n## {r['name']} — `{r['level']}`\n")
        if r["level"] == "N/A" and "note" in r:
            lines.append(f"> {r['note']}\n")
        if name == "ac-coverage":
            lines.append(f"- AC 总数: {r['total']}")
            lines.append(f"- 覆盖: {r['covered']}")
            if r["missing"]:
                lines.append(f"- **未覆盖 AC**:")
                for ac in r["missing"]:
                    lines.append(f"  - {ac}")
        elif name == "scope-creep":
            lines.append(f"- 代码 routes: {r['code_routes_count']}")
            lines.append(f"- 03b 定义: {r['defined_count']}")
            if r["creep"]:
                lines.append(f"- **范围蔓延**(代码有 / 03b 无):")
                for c in r["creep"]:
                    lines.append(f"  - `{c['method']} {c['path']}` ({c['file']})")
        elif name == "reverse-req":
            lines.append(f"- 关键词数: {r['keywords_count']}")
            if r["hits"]:
                lines.append(f"- **反向需求命中**(应 0):")
                for h in r["hits"]:
                    lines.append(f"  - `{h['keyword']}` in {h['file']}")
        elif name == "interface":
            lines.append(f"- 03b 定义: {r['defined_count']}")
            lines.append(f"- 代码已实现: {r['coded_count']}")
            if r["missing_in_code"]:
                lines.append(f"- **03b 写了但代码无**:")
                for m in r["missing_in_code"]:
                    lines.append(f"  - `{m['method']} {m['path']}`")
        elif name == "test-coverage":
            lines.append(f"- 03b 接口数: {r['interfaces_count']}")
            if r["uncovered"]:
                lines.append(f"- **未测接口**:")
                for u in r["uncovered"]:
                    lines.append(f"  - `{u['method']} {u['path']}`")
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="pm-template /audit — 已实现功能审查")
    parser.add_argument(
        "--ac-only", action="store_true", help="只跑 AC 覆盖率",
    )
    parser.add_argument(
        "--scope-creep", action="store_true", help="只跑范围蔓延",
    )
    parser.add_argument(
        "--reverse-req", action="store_true", help="只跑反向需求",
    )
    parser.add_argument(
        "--interface", action="store_true", help="只跑接口一致性",
    )
    parser.add_argument(
        "--test-coverage", action="store_true", help="只跑单测覆盖",
    )
    parser.add_argument(
        "--check", action="store_true", help="只跑不写报告(返回 exit code)",
    )
    parser.add_argument(
        "--report-path", help="自定义报告路径(默认 docs/audit/reports/audit_<DATE>.md)",
    )
    args = parser.parse_args()

    checks: list[str] | None = None
    if args.ac_only:
        checks = ["ac-coverage"]
    elif args.scope_creep:
        checks = ["scope-creep"]
    elif args.reverse_req:
        checks = ["reverse-req"]
    elif args.interface:
        checks = ["interface"]
    elif args.test_coverage:
        checks = ["test-coverage"]

    audit = run_audit(checks)

    if "error" in audit:
        print(f"✗ {audit['error']}", file=sys.stderr)
        return audit.get("code", ERR_PHASE_MISSING)

    if args.check:
        # 只打印 overall + exit code
        print(f"Overall: {audit['overall']}")
        for name, r in audit["results"].items():
            print(f"  {r['name']}: {r['level']}")
        return 0 if audit["overall"] == "PASS" else 1

    # 写报告
    if args.report_path:
        report_path = Path(args.report_path)
    else:
        REPORT_DIR.mkdir(parents=True, exist_ok=True)
        report_path = REPORT_DIR / f"audit_{date.today().isoformat()}.md"

    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(render_report(audit), encoding="utf-8")

    print(f"✓ 审计完成,overall: {audit['overall']}")
    print(f"  报告: {report_path}")
    for name, r in audit["results"].items():
        print(f"  {r['name']}: {r['level']}")

    return 0 if audit["overall"] == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
