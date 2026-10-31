"""Module providing repository management and file manipulation utilities."""

import difflib
from pathlib import Path
import shutil
import time
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


def backup_file(filepath: str | Path, backup_dir: str | Path) -> Path:
    """Create a timestamped backup copy of a file in the backup directory."""
    src = Path(filepath)
    if not src.exists() or not src.is_file():
        raise FileNotFoundError(f"Source file not found: {src}")
    target_dir = Path(backup_dir)
    target_dir.mkdir(parents=True, exist_ok=True)
    timestamp = int(time.time() * 1000)
    backup_path = target_dir / f"{src.stem}_{timestamp}{src.suffix}.bak"
    shutil.copy2(src, backup_path)
    return backup_path


def restore_file(backup_path: str | Path, target_path: str | Path) -> Path:
    """Restore a file from a backup copy to the target path."""
    b_path = Path(backup_path)
    if not b_path.exists() or not b_path.is_file():
        raise FileNotFoundError(f"Backup file not found: {b_path}")
    t_path = Path(target_path)
    t_path.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(b_path, t_path)
    return t_path


def diff_files(file1: str | Path, file2: str | Path) -> str:
    """Generate a unified diff string between two text files."""
    p1 = Path(file1)
    p2 = Path(file2)
    lines1 = p1.read_text(encoding="utf-8").splitlines(keepends=True) if p1.exists() else []
    lines2 = p2.read_text(encoding="utf-8").splitlines(keepends=True) if p2.exists() else []
    diff = difflib.unified_diff(
        lines1,
        lines2,
        fromfile=str(p1),
        tofile=str(p2),
    )
    return "".join(diff)
