from pathlib import Path

from bug_hunter.models import Metadata
from bug_hunter.rules.mutable_default import MutableDefaultArgumentRule


def test_detects_mutable_default_argument():
    source = """
def foo(a, b=[]):
    return a
"""
    rule = MutableDefaultArgumentRule()
    file_path = Path("test_file.py")
    metadata = Metadata(language="python", python_version="3.10", os_name="windows")

    findings = rule.apply(source, file_path, metadata)

    assert len(findings) == 1

    bug = findings[0]
    assert bug.bug_id == "BUG-001"
    assert bug.rule_name == "MUTABLE_DEFAULT_ARGUMENT"
    assert bug.severity == "HIGH"
    assert bug.file == file_path
    assert bug.line == 2
    assert "mutable" in bug.title.lower()


def test_ignores_immutable_default_argument():
    source = """
def foo(a, b=10):
    return a
"""
    rule = MutableDefaultArgumentRule()
    file_path = Path("test_file.py")
    metadata = Metadata(language="python", python_version="3.10", os_name="windows")

    findings = rule.apply(source, file_path, metadata)

    assert findings == []


def test_syntax_error_returns_no_findings():
    source = "def foo(:"
    rule = MutableDefaultArgumentRule()
    file_path = Path("bad.py")
    metadata = Metadata(language="python", python_version="3.10", os_name="windows")

    findings = rule.apply(source, file_path, metadata)

    assert findings == []
