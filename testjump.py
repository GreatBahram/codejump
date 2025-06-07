#!/usr/bin/env python3
import ast
import os
import subprocess
import sys
from pathlib import Path
from typing import Literal

EditorType = Literal["vscode", "idea", "pycharm", "vim", "nvim"]


def get_editor_command(editor: EditorType, file_path: str, line: int) -> list[str]:
    editor_commands = {
        "vscode": ["code", "-g", f"{file_path}:{line}"],
        "idea": ["idea", f"{file_path}:{line}"],
        "pycharm": ["pycharm", f"{file_path}:{line}"],
        "vim": ["vim", f"+{line}", file_path],
        "nvim": ["nvim", f"+{line}", file_path],
    }
    return editor_commands[editor]


def find_function_line(
    file_path: Path, class_name: str | None, func_name: str
) -> int | None:
    tree = ast.parse(file_path.read_text(encoding="utf-8"), filename=file_path)

    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef) and node.name == class_name:
            for item in node.body:
                if isinstance(item, ast.FunctionDef) and item.name == func_name:
                    return item.lineno
        elif (
            class_name is None
            and isinstance(node, ast.FunctionDef)
            and node.name == func_name
        ):
            return node.lineno

    return None


def parse_input(line: str) -> tuple[Path, str | None, str]:
    parts = line.strip().split("::")
    if len(parts) == 2:
        return Path(parts[0]), None, parts[1]
    elif len(parts) == 3:
        return Path(parts[0]), parts[1], parts[2]
    else:
        raise ValueError(f"Invalid input format: {line}")


def main() -> None:
    """A CLI tool that helps you quickly navigate to test functions in pytest files.

    Usage: tj path/to/file.py::[ClassName::]function

    For interactive usage with multiple files:
        for line in $(cat filename); do tj $line; echo "Press any key..."; read; done

    Examples:
        tj tests/test_calculator.py::test_addition
        tj tests/test_user.py::TestUser::test_user_creation
    """
    if len(sys.argv) != 2:
        print(main.__doc__)
        sys.exit(1)

    file_path, class_name, func_name = parse_input(sys.argv[1])

    if not file_path.exists():
        print(f"File not found: {file_path}", file=sys.stderr)
        sys.exit(1)

    line = find_function_line(file_path, class_name, func_name)

    if not line:
        print(f"Could not find '{func_name}' in '{file_path}'", file=sys.stderr)
        sys.exit(1)

    editor = os.environ.get("TJ_EDITOR", "vscode").lower()
    valid_editors = list(EditorType.__args__)

    if editor not in valid_editors:
        print(
            f"Invalid editor '{editor}'. Valid options are: {', '.join(valid_editors)}",
            file=sys.stderr,
        )
        sys.exit(1)

    cmd = get_editor_command(editor, file_path, line)

    try:
        subprocess.run(cmd, check=True)
    except FileNotFoundError:
        print(
            f"Editor '{editor}' not found. Is it installed and in your PATH?",
            file=sys.stderr,
        )
        sys.exit(1)
    except subprocess.CalledProcessError as e:
        print(f"Editor command failed with exit code {e.returncode}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error while running editor: {str(e)}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
