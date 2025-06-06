# CodeJump

A CLI tool that opens VS Code (by default) at the line where a function/method is defined.

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
for line in $(cat jumppoints.txt); do codejump $line; echo "Press any key to continue..."; read; done```
