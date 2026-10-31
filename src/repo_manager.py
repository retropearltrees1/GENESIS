"""Module providing repository management and file manipulation utilities."""

from pathlib import Path
from typing import List


def create_file(filepath: str | Path, content: str) -> Path:
    """Create a file with given content, ensuring parent directories exist."""
    path = Path(filepath)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    return path


def read_file_content(filepath: str | Path) -> str:
    """Read and return content from a file."""
    path = Path(filepath)
    return path.read_text(encoding="utf-8")


def list_structure(base_dir: str | Path) -> List[str]:
    """List relative file paths within base_dir, excluding hidden items."""
    dir_path = Path(base_dir)
    if not dir_path.exists():
        return []
    results: List[str] = []
    for item in dir_path.rglob("*"):
        if item.is_file() and not any(part.startswith(".") for part in item.parts):
            results.append(str(item.relative_to(dir_path)))
    return sorted(results)
