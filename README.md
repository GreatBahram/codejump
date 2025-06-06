# TestJump (TJ)

A CLI tool that helps you quickly navigate to test functions in pytest files.

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
### Configuring Your Editor

TestJump uses VS Code by default, but you can configure your preferred editor by setting the `TESTJUMP_EDITOR` environment variable:

```bash
# For VS Code (default)
export TESTJUMP_EDITOR=vscode

# For Vim
export TESTJUMP_EDITOR=vim

# For IntelliJ IDEA
export TESTJUMP_EDITOR=idea

# For PyCharm
export TESTJUMP_EDITOR=pycharm

# For Neovim
export TESTJUMP_EDITOR=nvim
````

Add this to your `.bashrc` or `.zshrc` to make it permanent.
