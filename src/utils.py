import re
from pathlib import Path

# Regex to clean tree characters (for parsing tree files)
TREE_CHARS = re.compile(r"[│├└─]+")


def clean_line(line: str) -> str:
    """
    Remove tree-drawing characters and extra spaces from a line.

    Example:
        '├── README.md' -> 'README.md'
    """
    return TREE_CHARS.sub("", line).strip()


def get_level(line: str, spaces_per_indent: int = 4) -> int:
    """
    Calculate the nesting level of a line based on leading spaces.

    Example:
        '    src/' -> 1  (assuming 4 spaces per indent)
    """
    stripped = line.lstrip()
    indent = len(line) - len(stripped)
    return indent // spaces_per_indent


def ensure_parent(path: Path):
    """
    Ensure the parent directory of a file exists.
    """
    path.parent.mkdir(parents=True, exist_ok=True)
