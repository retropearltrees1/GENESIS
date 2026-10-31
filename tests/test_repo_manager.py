from pathlib import Path
import pytest
from src.repo_manager import (
    create_file,
    read_file_content,
    list_structure,
    search_files,
    copy_file,
    get_file_metadata,
    backup_file,
    restore_file,
    diff_files,
)


def test_create_file(tmp_path: Path):
    target = tmp_path / "nested" / "file.txt"
    created = create_file(target, "sample data")
    assert created.exists()
    assert target.read_text(encoding="utf-8") == "sample data"


def test_read_file_content(tmp_path: Path):
    target = tmp_path / "hello.txt"
    target.write_text("hello world", encoding="utf-8")
    content = read_file_content(target)
    assert content == "hello world"


def test_list_structure(tmp_path: Path):
    create_file(tmp_path / "file1.txt", "one")
    create_file(tmp_path / "folder" / "file2.txt", "two")
    create_file(tmp_path / ".git" / "HEAD", "ref")

    structure = list_structure(tmp_path)
    assert "file1.txt" in structure
    assert str(Path("folder/file2.txt")) in structure
    assert all(".git" not in item for item in structure)


def test_search_files(tmp_path: Path):
    create_file(tmp_path / "doc1.md", "# Doc 1")
    create_file(tmp_path / "notes" / "doc2.md", "# Doc 2")
    create_file(tmp_path / "script.py", "print(1)")

    md_files = search_files(tmp_path, "*.md")
    assert "doc1.md" in md_files
    assert str(Path("notes/doc2.md")) in md_files
    assert "script.py" not in md_files


def test_copy_file(tmp_path: Path):
    src = tmp_path / "origin.txt"
    dest = tmp_path / "backup" / "copy.txt"
    create_file(src, "important content")

    copied = copy_file(src, dest)
    assert copied.exists()
    assert read_file_content(dest) == "important content"

    with pytest.raises(FileNotFoundError):
        copy_file(tmp_path / "does_not_exist.txt", tmp_path / "out.txt")


def test_get_file_metadata(tmp_path: Path):
    target = tmp_path / "meta_test.txt"
    create_file(target, "12345")

    meta = get_file_metadata(target)
    assert meta["exists"] is True
    assert meta["is_file"] is True
    assert meta["size_bytes"] == 5

    missing_meta = get_file_metadata(tmp_path / "missing.txt")
    assert missing_meta["exists"] is False


def test_backup_and_restore_file(tmp_path: Path):
    original = tmp_path / "doc.txt"
    create_file(original, "Original state v1")
    backup_dir = tmp_path / "backups"

    b_path = backup_file(original, backup_dir)
    assert b_path.exists()
    assert read_file_content(b_path) == "Original state v1"

    # Modify original file
    create_file(original, "Modified state v2")
    assert read_file_content(original) == "Modified state v2"

    # Restore from backup
    restored = restore_file(b_path, original)
    assert restored.exists()
    assert read_file_content(original) == "Original state v1"


def test_backup_missing_file_raises(tmp_path: Path):
    with pytest.raises(FileNotFoundError):
        backup_file(tmp_path / "none.txt", tmp_path / "backups")


def test_restore_missing_file_raises(tmp_path: Path):
    with pytest.raises(FileNotFoundError):
        restore_file(tmp_path / "none.bak", tmp_path / "out.txt")


def test_diff_files(tmp_path: Path):
    f1 = tmp_path / "f1.txt"
    f2 = tmp_path / "f2.txt"
    create_file(f1, "line 1\nline 2\n")
    create_file(f2, "line 1\nline 2 modified\n")

    diff = diff_files(f1, f2)
    assert "-line 2" in diff
    assert "+line 2 modified" in diff
