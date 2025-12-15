import sys
from pathlib import Path

import pytest

from bug_hunter import cli
from bug_hunter.models import BugFinding


def fake_scan_path(*args, **kwargs):
    return [
        BugFinding(
            bug_id="BUG-001",
            title="Mutable default argument detected",
            description="Test description",
            file=Path("example.py"),
            line=10,
            rule_name="MUTABLE_DEFAULT_ARGUMENT",
            severity="HIGH",
        )
    ]


def test_cli_scan_text_output(monkeypatch, capsys):
    # Replace scan_path with fake implementation
    monkeypatch.setattr(cli, "scan_path", fake_scan_path)

    # Simulate command-line arguments
    monkeypatch.setattr(
        sys,
        "argv",
        ["bug-hunter", "scan", ".", "--format", "text"],
    )

    cli.main()

    captured = capsys.readouterr().out

    assert "BUG-001" in captured
    assert "HIGH" in captured
    assert "example.py" in captured


def test_cli_scan_json_output(monkeypatch, capsys):
    monkeypatch.setattr(cli, "scan_path", fake_scan_path)

    monkeypatch.setattr(
        sys,
        "argv",
        ["bug-hunter", "scan", ".", "--format", "json"],
    )

    cli.main()

    output = capsys.readouterr().out

    assert '"bug_id": "BUG-001"' in output
    assert '"severity": "HIGH"' in output
