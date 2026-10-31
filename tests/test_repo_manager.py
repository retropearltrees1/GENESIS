from pathlib import Path
import pytest
from src.repo_manager import (
    create_file,
    read_file_content,
    list_structure,
    search_files,
    copy_file,
    get_file_metadata,
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

    # Non-existent source should raise FileNotFoundError
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
