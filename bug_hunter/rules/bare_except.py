import ast
from pathlib import Path
from typing import List

from bug_hunter.models import BugFinding, Metadata
from bug_hunter.rules.base import BugRule


class BareExceptRule(BugRule):
    rule_name = "BARE_EXCEPT"
    bug_id = "BUG-002"
    severity = "MEDIUM"

    def apply(
        self,
        source: str,
        file_path: Path,
        metadata: Metadata,
    ) -> List[BugFinding]:
        findings: List[BugFinding] = []

        try:
            tree = ast.parse(source)
        except SyntaxError:
            return findings

        for node in ast.walk(tree):
            if isinstance(node, ast.ExceptHandler) and node.type is None:
                findings.append(
                    BugFinding(
                        bug_id=self.bug_id,
                        title="Bare except detected",
                        description="Bare except blocks catch all exceptions and hide bugs.",
                        file=file_path,
                        line=node.lineno,
                        rule_name=self.rule_name,
                        severity=self.severity,
                    )
                )

        return findings
