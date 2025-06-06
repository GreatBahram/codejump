#!/usr/bin/env python3
"""
A CLI tool that opens VS Code at the line where a function/method is defined.
Usage: codejump path/to/file.py::[ClassName::]function

For interactive usage with multiple files:
    for line in $(cat filename); do codejump $line; read; done
"""

import ast
import sys
import subprocess


def find_function_line(
    file_path: str, class_name: str | None, func_name: str
) -> int | None:
    with open(file_path, "r", encoding="utf-8") as fp:
        tree = ast.parse(fp.read(), filename=file_path)

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


def parse_input(line: str) -> tuple[str, str | None, str]:
    parts = line.strip().split("::")
    if len(parts) == 2:
        return parts[0], None, parts[1]
    elif len(parts) == 3:
        return parts[0], parts[1], parts[2]
    else:
        raise ValueError(f"Invalid input format: {line}")


def main():
    if len(sys.argv) != 2:
        print("Usage: codejump.py path/to/file.py::[ClassName::]function")
        sys.exit(1)

    file_path, class_name, func_name = parse_input(sys.argv[1])
    line = find_function_line(file_path, class_name, func_name)

    if line:
        subprocess.run(["code", "-g", f"{file_path}:{line}"])
    else:
        print(f"❌ Could not find {func_name} in {file_path}", file=sys.stderr)


if __name__ == "__main__":
    main()
