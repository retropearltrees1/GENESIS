"""Module providing repository management and file manipulation utilities."""

from pathlib import Path
import shutil
from typing import Any, Dict, List


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


def search_files(base_dir: str | Path, pattern: str) -> List[str]:
    """Search for files matching a glob pattern relative to base_dir."""
    dir_path = Path(base_dir)
    if not dir_path.exists():
        return []
    matches: List[str] = []
    for match in dir_path.rglob(pattern):
        if match.is_file() and not any(part.startswith(".") for part in match.parts):
            matches.append(str(match.relative_to(dir_path)))
    return sorted(matches)


def copy_file(src_path: str | Path, dest_path: str | Path) -> Path:
    """Copy a file from src_path to dest_path, creating target directories if needed."""
    src = Path(src_path)
    dest = Path(dest_path)
    if not src.exists() or not src.is_file():
        raise FileNotFoundError(f"Source file not found: {src}")
    dest.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dest)
    return dest


def get_file_metadata(filepath: str | Path) -> Dict[str, Any]:
    """Retrieve file metadata including size in bytes and file existence."""
    path = Path(filepath)
    if not path.exists():
        return {"exists": False}
    stat = path.stat()
    return {
        "exists": True,
        "size_bytes": stat.st_size,
        "is_file": path.is_file(),
        "is_dir": path.is_dir(),
    }
