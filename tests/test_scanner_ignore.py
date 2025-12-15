from pathlib import Path

from bug_hunter.scanner import scan_path


def test_default_ignores_are_respected(tmp_path):
    # venv should be ignored by default
    venv_dir = tmp_path / "venv"
    venv_dir.mkdir()
    (venv_dir / "bad.py").write_text(
        "def foo(x, y=[]): pass", encoding="utf-8"
    )

    good_file = tmp_path / "good.py"
    good_file.write_text(
        "def bar(x, y=[]): pass", encoding="utf-8"
    )

    findings = scan_path(
        path=tmp_path,
        source_type="code",
        language="python",
        python_version="3.10",
        os_name="windows",
    )

    assert len(findings) == 1
    assert findings[0].file == good_file


def test_bughunterignore_file_is_respected(tmp_path):
    # Create ignore file
    ignore_file = tmp_path / ".bughunterignore"
    ignore_file.write_text("ignored.py", encoding="utf-8")

    ignored = tmp_path / "ignored.py"
    ignored.write_text(
        "def foo(x, y=[]): pass", encoding="utf-8"
    )

    scanned = tmp_path / "scanned.py"
    scanned.write_text(
        "def bar(x, y=[]): pass", encoding="utf-8"
    )

    findings = scan_path(
        path=tmp_path,
        source_type="code",
        language="python",
        python_version="3.10",
        os_name="windows",
    )

    assert len(findings) == 1
    assert findings[0].file == scanned


def test_cli_ignore_patterns_are_respected(tmp_path):
    ignored_dir = tmp_path / "skipme"
    ignored_dir.mkdir()
    (ignored_dir / "bad.py").write_text(
        "def foo(x, y=[]): pass", encoding="utf-8"
    )

    good_file = tmp_path / "good.py"
    good_file.write_text(
        "def bar(x, y=[]): pass", encoding="utf-8"
    )

    findings = scan_path(
        path=tmp_path,
        source_type="code",
        language="python",
        python_version="3.10",
        os_name="windows",
        ignore=["skipme"],
    )

    assert len(findings) == 1
    assert findings[0].file == good_file


def test_glob_ignore_pattern_works(tmp_path):
    tests_dir = tmp_path / "tests"
    tests_dir.mkdir()
    (tests_dir / "test_bad.py").write_text(
        "def foo(x, y=[]): pass", encoding="utf-8"
    )

    good_file = tmp_path / "main.py"
    good_file.write_text(
        "def bar(x, y=[]): pass", encoding="utf-8"
    )

    findings = scan_path(
        path=tmp_path,
        source_type="code",
        language="python",
        python_version="3.10",
        os_name="windows",
        ignore=["tests/**"],
    )

    assert len(findings) == 1
    assert findings[0].file == good_file
