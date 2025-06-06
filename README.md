# CodeJump

A CLI tool that opens VS Code (by default) at the line where a function/method is defined.

## Installation

```bash
pip install codejump
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
