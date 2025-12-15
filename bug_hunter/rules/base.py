from abc import ABC, abstractmethod
from pathlib import Path
from typing import List

from bug_hunter.models import BugFinding, Metadata


class BugRule(ABC):
    rule_name: str
    bug_id: str
    severity: str

    @abstractmethod
    def apply(
        self,
        source: str,
        file_path: Path,
        metadata: Metadata,
    ) -> List[BugFinding]:
        pass
