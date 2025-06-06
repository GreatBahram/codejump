# CodeJump

A CLI tool that helps you quickly navigate to test functions in pytest files.

## Installation

Install this tool using pip:

```bash
pip install codejump
```

Or using [pipx](https://pipx.pypa.io/stable/):

```bash
pipx install codejump
```

Or using [uv](https://docs.astral.sh/uv/guides/tools/):

```bash
uv tool install codejump
```

## Usage

1. Jump to a test function:

```bash
codejump tests/test_calculator.py::test_addition
```

2. Jump to a test class method:

```bash
codejump tests/test_user.py::TestUser::test_user_creation
```

### Interactive Usage with Multiple Files

You can use it interactively with a file containing multiple jump points:

```bash
for line in $(cat jumppoints.txt); do codejump $line; echo "Press any key to continue..."; read; done
```
### Configuring Your Editor

CodeJump uses VS Code by default, but you can configure your preferred editor by setting the `CODEJUMP_EDITOR` environment variable:

```bash
# For VS Code (default)
export CODEJUMP_EDITOR=vscode

# For Vim
export CODEJUMP_EDITOR=vim

# For IntelliJ IDEA
export CODEJUMP_EDITOR=idea

# For PyCharm
export CODEJUMP_EDITOR=pycharm

# For Neovim
export CODEJUMP_EDITOR=nvim
````

Add this to your `.bashrc` or `.zshrc` to make it permanent.
