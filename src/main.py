import re
from pathlib import Path

# Regular expression to match tree-drawing characters in structure files
TREE_CHARS = re.compile(r"[│├└─]+")


def clean_line(line: str) -> str:
    """
    Remove tree characters (│, ├, └, ─) and extra spaces from a line.
    
    Args:
        line (str): A line from a tree structure file.
    
    Returns:
        str: Cleaned line with folder/file name only.
    """
    return TREE_CHARS.sub("", line).strip()


def ask(prompt, default=None):
    """
    Prompt the user for input with an optional default value.
    
    Args:
        prompt (str): Question to show the user.
        default (str, optional): Default value if user presses Enter.
    
    Returns:
        str: User input or default.
    """
    if default:
        value = input(f"{prompt} [{default}]: ").strip()
        return value or default
    return input(f"{prompt}: ").strip()


def parse_tree(tree_file):
    """
    Read a tree structure file and return all non-empty lines.
    
    Args:
        tree_file (Path or str): Path to the structure file.
    
    Returns:
        list[str]: List of cleaned, non-empty lines.
    """
    with open(tree_file, "r", encoding="utf-8") as f:
        return [line.rstrip("\n") for line in f if line.strip()]


def get_level(line: str) -> int:
    """
    Determine the nesting level of a line based on leading '│' characters.
    
    Adjust this function if your tree file uses spaces for indentation.
    
    Args:
        line (str): Line from tree structure file.
    
    Returns:
        int: Nesting level (0 for top-level entries).
    """
    return line.count("│")


def create_from_tree(lines, root_path):
    """
    Create folders and files from a list of tree lines.
    
    Args:
        lines (list[str]): Lines representing folder/file structure.
        root_path (Path): Base path where the structure will be created.
    """
    stack = []  # Tracks the current folder hierarchy

    for raw_line in lines:
        level = get_level(raw_line)  # Determine depth
        name = clean_line(raw_line)  # Clean folder/file name

        # Pop the stack if we're going back up the hierarchy
        while len(stack) > level:
            stack.pop()

        # Determine the full path for this file/folder
        target = root_path / Path(*stack) / name.rstrip("/")

        if name.endswith("/"):
            # Folder: create it and add to the stack
            target.mkdir(parents=True, exist_ok=True)
            stack.append(name.rstrip("/"))
        else:
            # File: ensure parent folder exists, then create file
            target.parent.mkdir(parents=True, exist_ok=True)
            target.touch(exist_ok=True)


def main():
    """Main entry point for the project scaffold tool."""
    print("\n🛠 Project Scaffold Tool\n")

    # Default projects folder: one level above this script
    default_base = Path(__file__).resolve().parent.parent / "projects"
    default_base.mkdir(parents=True, exist_ok=True)

    # Ask user where to create the new project
    base_dir = ask(
        "Where should the project be created?",
        default=str(default_base)
    )

    # Ask for the project name
    project_name = ask("Project name", default="app_new_project")

    # Default structure file location (one level above src/)
    script_dir = Path(__file__).resolve().parent.parent
    structure_file = ask(
        "Path to structure file",
        default=str(script_dir / "structure.txt")
    )
    structure_file = Path(structure_file).expanduser().resolve()

    # Check that the structure file exists
    if not structure_file.exists():
        print("❌ Structure file not found.")
        return

    base_dir = Path(base_dir).expanduser().resolve()
    project_root = base_dir / project_name

    # Show a summary before creating
    print("\n📋 Summary")
    print(f"Location : {project_root}")
    print(f"Structure: {structure_file}")

    confirm = ask("Proceed? (y/n)", "n").lower()
    if confirm != "y":
        print("Aborted.")
        return

    # Create the root project folder and generate structure
    project_root.mkdir(parents=True, exist_ok=True)
    tree_lines = parse_tree(structure_file)
    create_from_tree(tree_lines, project_root)

    print("\n✅ Project created successfully!")


# Run the scaffold tool if executed as a script
if __name__ == "__main__":
    main()
