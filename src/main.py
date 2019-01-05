import re
from pathlib import Path

TREE_CHARS = re.compile(r"[│├└─]+")


def clean_line(line: str) -> str:
    """Remove tree characters and extra spaces from a line."""
    return TREE_CHARS.sub("", line).strip()


def ask(prompt, default=None):
    """Prompt the user with an optional default value."""
    if default:
        value = input(f"{prompt} [{default}]: ").strip()
        return value or default
    return input(f"{prompt}: ").strip()


def parse_tree(tree_file):
    """Read a tree structure file and return all non-empty lines."""
    with open(tree_file, "r", encoding="utf-8") as f:
        return [line.rstrip("\n") for line in f if line.strip()]


def get_level(line: str) -> int:
    """
    Determine nesting level based on the count of leading '│' characters.
    Adjust this function if your tree file uses indentation spaces instead.
    """
    return line.count("│")


def create_from_tree(lines, root_path):
    """Create folders and files from a list of tree lines."""
    stack = []

    for raw_line in lines:
        level = get_level(raw_line)
        name = clean_line(raw_line)

        while len(stack) > level:
            stack.pop()

        target = root_path / Path(*stack) / name.rstrip("/")

        if name.endswith("/"):
            target.mkdir(parents=True, exist_ok=True)
            stack.append(name.rstrip("/"))
        else:
            target.parent.mkdir(parents=True, exist_ok=True)
            target.touch(exist_ok=True)


def main():
    print("\n🛠 Project Scaffold Tool\n")

    # Default projects folder: parent directory of this script
    default_base = Path(__file__).resolve().parent.parent / "projects"
    default_base.mkdir(parents=True, exist_ok=True)

    base_dir = ask(
        "Where should the project be created?",
        default=str(default_base)
    )

    project_name = ask("Project name", default="app_new_project")

    # Default structure file in the root of the project (one level up from src/)
    script_dir = Path(__file__).resolve().parent.parent
    structure_file = ask(
        "Path to structure file",
        default=str(script_dir / "structure.txt")
)

    structure_file = Path(structure_file).expanduser().resolve()

    if not structure_file.exists():
        print("❌ Structure file not found.")
        return

    base_dir = Path(base_dir).expanduser().resolve()
    project_root = base_dir / project_name

    print("\n📋 Summary")
    print(f"Location : {project_root}")
    print(f"Structure: {structure_file}")

    confirm = ask("Proceed? (y/n)", "n").lower()
    if confirm != "y":
        print("Aborted.")
        return

    project_root.mkdir(parents=True, exist_ok=True)
    tree_lines = parse_tree(structure_file)
    create_from_tree(tree_lines, project_root)

    print("\n✅ Project created successfully!")


if __name__ == "__main__":
    main()
