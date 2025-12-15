# cli.py
import argparse
import json
from pathlib import Path

from bug_hunter.scanner import scan_path


def render_text(findings):
    for finding in findings:
        print()
        print(
            f"[{finding.bug_id}] {finding.severity} | "
            f"{finding.file}:{finding.line}"
        )
        print(f"{finding.title}")
        print(f"Rule: {finding.rule_name}")


def render_json(findings):
    data = [
        {
            "bug_id": f.bug_id,
            "title": f.title,
            "description": f.description,
            "file": str(f.file),
            "line": f.line,
            "rule": f.rule_name,
            "severity": f.severity,
        }
        for f in findings
    ]
    print(json.dumps(data, indent=2))


def main():
    parser = argparse.ArgumentParser(
        prog="bug-hunter",
        description="A CLI tool that scans code or logs and reports potential bugs.",
    )

    subparsers = parser.add_subparsers(dest="command", required=True)

    scan_parser = subparsers.add_parser(
        "scan",
        help="Scan a file or directory for potential bugs",
    )
    scan_parser.add_argument(
        "path",
        type=Path,
        help="Path to a file or directory to scan",
    )
    scan_parser.add_argument(
        "--type",
        choices=["code", "log"],
        default="code",
        help="Type of input being scanned",
    )
    scan_parser.add_argument(
        "--language",
        default="python",
        help="Programming language (default: python)",
    )
    scan_parser.add_argument(
        "--python-version",
        dest="python_version",
        help="Python version used by the project",
    )
    scan_parser.add_argument(
        "--os",
        dest="os_name",
        help="Operating system (windows, linux, mac)",
    )
    scan_parser.add_argument(
        "--format",
        choices=["text", "json"],
        default="text",
        help="Output format (default: text)",
    )
    scan_parser.add_argument(
        "--recursive",
        action="store_true",
        default=True,
        help="Recursively scan directories",
    )

    scan_parser.add_argument(
    "--ignore",
    help=(
        "Comma-separated list of directory/file names or glob patterns to ignore. "
        "Supports wildcards like *, **. "
        "Patterns are combined with .bughunterignore."
        ),
    )



    args = parser.parse_args()

    if args.command == "scan":
        findings = scan_path(
            path=args.path,
            source_type=args.type,
            language=args.language,
            python_version=args.python_version,
            os_name=args.os_name,
            recursive=args.recursive,
            ignore=args.ignore.split(",") if args.ignore else None,
        )

        if args.format == "json":
            render_json(findings)
        else:
            render_text(findings)


if __name__ == "__main__":
    main()
