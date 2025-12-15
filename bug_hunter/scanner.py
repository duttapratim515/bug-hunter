from pathlib import Path
from typing import List

from bug_hunter.models import Metadata, BugFinding
from bug_hunter.rules.mutable_default import MutableDefaultArgumentRule
from bug_hunter.rules.bare_except import BareExceptRule
from bug_hunter.utils import collect_python_files


def scan_path(
    path: Path,
    source_type: str,
    language: str,
    python_version: str | None,
    os_name: str | None,
    recursive: bool = True,
    ignore: list[str] | None = None,
) -> List[BugFinding]:
    if not path.exists():
        raise FileNotFoundError(f"Path does not exist: {path}")

    metadata = Metadata(
        language=language,
        python_version=python_version,
        os_name=os_name,
    )

    rules = [
        MutableDefaultArgumentRule(),
        BareExceptRule(),
    ]

    findings: List[BugFinding] = []

    # 👉 THIS is the code you were looking for
    files = collect_python_files(
        path=path,
        recursive=recursive,
        ignore=ignore,
    )

    for file in files:
        findings.extend(_scan_file(file, rules, metadata))

    return findings


def _scan_file(
    file_path: Path,
    rules,
    metadata: Metadata,
) -> List[BugFinding]:
    findings: List[BugFinding] = []

    try:
        source = file_path.read_text(encoding="utf-8")
    except Exception:
        return findings

    for rule in rules:
        findings.extend(rule.apply(source, file_path, metadata))

    return findings
