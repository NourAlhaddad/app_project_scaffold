# Project Scaffold Tool

**A Python utility to generate project folders and files from a tree-style structure file.**

---

## 🛠 Description

This script allows developers to **quickly create a project structure** by reading a tree-like document that defines folders and files. It is interactive, cross-platform, and lightweight — perfect for scaffolding new projects or standardizing folder layouts.

Key features:

- Reads a **tree-style structure file** (`structure.txt`) with folder and file hierarchy.
- Interactive prompts for:
  - Project location
  - Project name
  - Structure file path
- Confirms actions before creating files/folders.
- Automatically creates directories and empty files based on the structure.

---

## ⚡ Usage

1. Prepare a **structure file** (`structure.txt`) describing the project:



## Clone the repo
git clone https://github.com/yourusername/app_project_scaffold.git
cd app_project_scaffold

# Create a virtual environment
python3 -m venv venv

# Activate the environment
# macOS/Linux
source venv/bin/activate
# Windows
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install development/test dependencies
pip install -r requirements.txt


## Running test
python3 -m pytest -v tests/

