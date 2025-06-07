# TestJump (TJ)

A CLI tool that helps you quickly navigate to test functions in pytest files.

> When making fundamental changes to a project, multiple test cases often fail.
> Instead of manually opening files and searching for each failing test, TestJump allows you to jump directly to the test location 🤷.

## Installation

Install this tool using pip:

```bash
pip install testjump
```

Or using [pipx](https://pipx.pypa.io/stable/):

```bash
pipx install testjump
```

Or using [uv](https://docs.astral.sh/uv/guides/tools/):

```bash
uv tool install testjump
```

## Usage

1. Jump to a test function:

```bash
tj tests/test_calculator.py::test_addition
```

2. Jump to a test class method:

```bash
tj tests/test_user.py::TestUser::test_user_creation
```

### Interactive Usage with Multiple Files

You can use it interactively with a file containing multiple jump points:

```bash
for line in $(cat jumppoints.txt); do tj $line; echo "Press any key to continue..."; read; done
```

### Output Options

TestJump supports different output formats:

1. Print location only (useful for scripting):

```bash
tj -print tests/test_calculator.py::test_addition
# Output: tests/test_calculator.py:42
```

2. JSON output with detailed information:

```bash
tj -json tests/test_calculator.py::test_addition
# Output:
# {
#   "status": "ok",
#   "path": "tests/test_calculator.py",
#   "class_name": null,
#   "function_name": "test_addition"
# }
```

### Configuring Your Editor

TestJump uses VS Code by default, but you can configure your preferred editor by setting the `TJ_EDITOR` environment variable:

```bash
# For VS Code (default)
export TJ_EDITOR=vscode

# For Vim
export TJ_EDITOR=vim

# For IntelliJ IDEA
export TJ_EDITOR=idea

# For PyCharm
export TJ_EDITOR=pycharm

# For Neovim
export TJ_EDITOR=nvim
```

Add this to your `.bashrc` or `.zshrc` to make it permanent.
