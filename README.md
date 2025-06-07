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

3. Jump using pytest output (supports FAILED prefix):

```bash
tj "FAILED tests/test_user.py::TestUser::test_user_creation - Failed: assertion error"
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
tj tests/test_calculator.py::test_addition -print
# Output: tests/test_calculator.py:42
```

2. JSON output with detailed information:

```bash
tj tests/test_calculator.py::test_addition -json
# Output:
# {
#   "status": "ok",
#   "path": "tests/test_calculator.py",
#   "class_name": null,
#   "function_name": "test_addition",
#   "lineno": 11
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

## Contributing

To contribute to this tool, first checkout the code. Then create a new virtual environment:

```shell
cd testjump
python -m venv .venv
source .venv/bin/activate
```

Now install the dependencies and test dependencies:

```shell
pip install -e '.[dev]'
```

Or if you are using [uv](https://docs.astral.sh/uv/):

```shell
uv sync --extra dev
```

To run the tests:

```
uv run pytest .
```

To help ensure consistent code quality that follows our guidelines, [pre-commit](https://pre-commit.com/install) may be used. We have git hooks defined which will execute before commit. To install the hooks:

```shell
pre-commit install
```
