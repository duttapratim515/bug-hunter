import ast
from pathlib import Path
from typing import List

from bug_hunter.models import BugFinding, Metadata
from bug_hunter.rules.base import BugRule


class MutableDefaultArgumentRule(BugRule):
    rule_name = "MUTABLE_DEFAULT_ARGUMENT"
    bug_id = "BUG-001"
    severity = "HIGH"

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
            if isinstance(node, ast.FunctionDef):
                for default in node.args.defaults:
                    if isinstance(default, (ast.List, ast.Dict, ast.Set)):
                        findings.append(
                            BugFinding(
                                bug_id=self.bug_id,
                                title="Mutable default argument detected",
                                description=(
                                    f"Function '{node.name}' uses a mutable "
                                    "object as a default argument."
                                ),
                                file=file_path,
                                line=node.lineno,
                                rule_name=self.rule_name,
                                severity=self.severity,
                            )
                        )

        return findings
