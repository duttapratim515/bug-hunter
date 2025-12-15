from pathlib import Path

import pytest

from bug_hunter.scanner import scan_path


def test_scan_path_raises_if_path_does_not_exist():
    fake_path = Path("this/path/does/not/exist")

    with pytest.raises(FileNotFoundError):
        scan_path(
            path=fake_path,
            source_type="path",
            language="python",
            python_version="3.10",
            os_name="windows",
        )


def test_scan_path_detects_bug_in_python_file(tmp_path):
    # Arrange: create a Python file with a mutable default
    code = """
def foo(x, y=[]):
    return x
"""
    file_path = tmp_path / "bad.py"
    file_path.write_text(code, encoding="utf-8")

    # Act
    findings = scan_path(
        path=tmp_path,
        source_type="path",
        language="python",
        python_version="3.10",
        os_name="windows",
        recursive=True,
    )

    # Assert
    assert len(findings) == 1
    bug = findings[0]

    assert bug.file == file_path
    assert bug.bug_id == "BUG-001"


def test_scan_path_ignores_non_python_files(tmp_path):
    # Arrange
    (tmp_path / "notes.txt").write_text("def foo(x, y=[]): pass")
    (tmp_path / "image.png").write_bytes(b"fake")

    # Act
    findings = scan_path(
        path=tmp_path,
        source_type="path",
        language="python",
        python_version="3.10",
        os_name="windows",
    )

    # Assert
    assert findings == []
