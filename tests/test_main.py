import pytest
from pathlib import Path
from main import clean_line, parse_tree, create_from_tree


# Sample project structure using 4-space indentation for levels
SAMPLE_TREE = [
    "my_app/",
    "    src/",
    "        main.py",
    "    tests/",
    "        test_main.py",
    "    README.md"
]

def test_clean_line():
    assert clean_line("├── README.md") == "README.md"
    assert clean_line("│   └── test.py") == "test.py"
    assert clean_line("   main.py") == "main.py"

def test_parse_tree(tmp_path):
    tree_file = tmp_path / "structure.txt"
    tree_file.write_text("\n".join(SAMPLE_TREE))

    lines = parse_tree(tree_file)
    # parse_tree cleans lines, so tree characters are gone
    assert lines[0] == "my_app/"
    assert lines[-1] == "README.md"
    assert len(lines) == len(SAMPLE_TREE)

def test_create_from_tree(tmp_path):
    create_from_tree(SAMPLE_TREE, tmp_path)

    # Check folders
    assert (tmp_path / "my_app").is_dir()
    assert (tmp_path / "my_app" / "src").is_dir()
    assert (tmp_path / "my_app" / "tests").is_dir()

    # Check files
    assert (tmp_path / "my_app" / "src" / "main.py").is_file()
    assert (tmp_path / "my_app" / "tests" / "test_main.py").is_file()
    assert (tmp_path / "my_app" / "README.md").is_file()
