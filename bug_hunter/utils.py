# utils.py
from pathlib import Path
from typing import Iterable, List

DEFAULT_IGNORES = {
    ".git",
    "__pycache__",
    "venv",
    ".venv",
    "env",
    "node_modules",
    "dist",
    "build",
}


def load_ignore_file(base_path: Path) -> list[str]:
    """
    Load ignore patterns from a .bughunterignore file if it exists.
    Supports glob-style patterns.
    """
    ignore_file = base_path / ".bughunterignore"
    patterns: list[str] = []

    if not ignore_file.exists():
        return patterns

    try:
        for line in ignore_file.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            patterns.append(line)
    except Exception:
        pass

    return patterns


def collect_python_files(
    path: Path,
    recursive: bool = True,
    ignore: Iterable[str] | None = None,
) -> List[Path]:
    """
    Collect .py files from a path, respecting recursion and ignore patterns.
    """
    base_path = path if path.is_dir() else path.parent

    # Merge all ignore patterns
    patterns: list[str] = []
    patterns.extend(DEFAULT_IGNORES)
    patterns.extend(load_ignore_file(base_path))
    if ignore:
        patterns.extend(ignore)

    files: List[Path] = []

    def is_ignored(p: Path) -> bool:
        rel = p.relative_to(base_path)
        # Check each part of the path for default/CLI ignores
        for pattern in patterns:
            if pattern in p.parts:  # directory/file name match
                return True
            if rel.match(pattern):  # glob match
                return True
        return False

    if path.is_file():
        if path.suffix == ".py" and not is_ignored(path):
            return [path]
        return []

    # Directory scanning
    if recursive:
        for p in path.rglob("*.py"):
            if not is_ignored(p):
                files.append(p)
    else:
        for p in path.glob("*.py"):
            if not is_ignored(p):
                files.append(p)

    return files
