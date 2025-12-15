#models.py
from dataclasses import dataclass
from pathlib import Path
from typing import Optional


@dataclass
class Metadata:
    language: str
    python_version: Optional[str]
    os_name: Optional[str]


@dataclass
class BugFinding:
    bug_id: str
    title: str
    description: str
    file: Path
    line: int
    rule_name: str
    severity: str  # LOW | MEDIUM | HIGH

