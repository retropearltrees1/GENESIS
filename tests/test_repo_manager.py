from pathlib import Path
from src.repo_manager import create_file, read_file_content, list_structure


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
