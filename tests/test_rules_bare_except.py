from pathlib import Path

from bug_hunter.models import Metadata
from bug_hunter.rules.bare_except import BareExceptRule


def test_detects_bare_except():
    source = """
try:
    x = 1 / 0
except:
    print("error")
"""
    rule = BareExceptRule()
    file_path = Path("example.py")
    metadata = Metadata(language="python", python_version="3.10", os_name="windows")

    findings = rule.apply(source, file_path, metadata)

    assert len(findings) == 1
    bug = findings[0]

    assert bug.bug_id == "BUG-002"
    assert bug.rule_name == "BARE_EXCEPT"
    assert bug.file == file_path
    assert bug.line == 4


def test_ignores_specific_exception():
    source = """
try:
    x = 1 / 0
except ZeroDivisionError:
    print("error")
"""
    rule = BareExceptRule()
    file_path = Path("example.py")
    metadata = Metadata(language="python", python_version="3.10", os_name="windows")

    findings = rule.apply(source, file_path, metadata)

    assert findings == []
