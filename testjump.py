#!/usr/bin/env python3
import argparse
import ast
import json
import os
import subprocess
from enum import Enum
from pathlib import Path
from typing import Literal


class Action(str, Enum):
    PRINT = "print"
    EDITOR = "editor"
    JSON = "json"


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

    if not parts or not all(parts):
        raise ValueError(f"Invalid input format: {line}")

    if len(parts) == 2:  # noqa: PLR2004
        return Path(parts[0]), None, parts[1]
    elif len(parts) == 3:  # noqa: PLR2004
        return Path(parts[0]), parts[1], parts[2]
    else:
        raise ValueError(f"Invalid input format: {line}")


def main() -> None:
    """
    Usage: tj path/to/file.py::[ClassName::]function

    For interactive usage with multiple files:
        for line in $(cat filename); do tj $line; echo "Press any key..."; read; done

    Examples:
        tj tests/test_calculator.py::test_addition
        tj tests/test_user.py::TestUser::test_user_creation
    """
    parser = argparse.ArgumentParser(
        description="Quickly navigate to test functions",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=main.__doc__,
    )
    parser.add_argument(
        "test_path",
        help="Path in format: path/to/file.py::[ClassName::]function",
    )
    parser.add_argument(
        "--editor",
        choices=list(EditorType.__args__),
        default=os.environ.get("TJ_EDITOR", "vscode").lower(),
        help="Editor to use (default: vscode)",
    )

    action_group = parser.add_mutually_exclusive_group()
    action_group.add_argument(
        "-print", action="store_const", const=Action.PRINT, dest="action"
    )
    action_group.add_argument(
        "-editor", action="store_const", const=Action.EDITOR, dest="action"
    )
    action_group.add_argument(
        "-json", action="store_const", const=Action.JSON, dest="action"
    )
    parser.set_defaults(action=Action.EDITOR)  # Default action

    args = parser.parse_args()

    try:
        file_path, class_name, func_name = parse_input(args.test_path)
    except ValueError as e:
        parser.error(str(e))

    if not file_path.exists():
        parser.error("File not found")

    lineno = find_function_line(file_path, class_name, func_name)

    if not lineno:
        parser.error("Function not found")

    match args.action:
        case Action.EDITOR:
            launch_editor(parser, args.editor, file_path, lineno)
        case Action.PRINT:
            print(f"{file_path}:{lineno}")
        case Action.JSON:
            result = {
                "status": "ok",
                "path": str(file_path),
                "class_name": class_name,
                "function_name": func_name,
                "lineno": lineno,
            }
            print(json.dumps(result, indent=2))


def launch_editor(
    parser: argparse.ArgumentParser, editor: str, file_path: Path, line: int
) -> None:
    cmd = get_editor_command(editor, file_path, line)

    try:
        subprocess.run(cmd, check=True)
    except FileNotFoundError:
        parser.error(f"Editor '{editor}' not found. Is it installed and in your PATH?")
    except subprocess.CalledProcessError as e:
        parser.error(f"Editor command failed with exit code {e.returncode}")
    except Exception as e:
        parser.error(f"Unexpected error while running editor: {str(e)}")


if __name__ == "__main__":
    main()
