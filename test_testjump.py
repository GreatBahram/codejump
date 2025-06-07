from pathlib import Path
from textwrap import dedent

import pytest

import testjump


@pytest.mark.parametrize(
    ("line", "expected"),
    [
        (
            "tests/test_calculator.py::test_addition",
            (Path("tests/test_calculator.py"), None, "test_addition"),
        ),
        (
            "tests/test_user.py::TestUser::test_user_creation",
            (Path("tests/test_user.py"), "TestUser", "test_user_creation"),
        ),
    ],
)
def test_parse_input(line: str, expected: str) -> None:
    assert testjump.parse_input(line) == expected


@pytest.mark.parametrize(
    "invalid_line",
    [
        "tests/test_calculator.py",  # missing function
        "tests/test_calculator.py::",  # empty function
        "tests/test_calculator.py::::test",  # too many colons
    ],
)
def test_parse_input_raises_value_error(invalid_line: str) -> None:
    with pytest.raises(ValueError):
        testjump.parse_input(invalid_line)


@pytest.fixture
def sample_test_file(tmp_path) -> None:
    content = dedent("""
        def test_addition():
            assert 1 + 1 == 2

        class TestCalculator:
            def test_subtraction(self):
                assert 2 - 1 == 1

            def test_multiplication(self):
                assert 2 * 3 == 6


        class TestAdvanced: # TODO: support this later
            class TestNested:
                def test_nested(self):
                    assert True
    """)

    test_file = tmp_path / "test_sample.py"
    test_file.write_text(content)
    return test_file


@pytest.mark.parametrize(
    ("class_name", "func_name", "expected_line"),
    [
        (None, "test_addition", 2),  # Module-level test function
        ("TestCalculator", "test_subtraction", 6),  # Class method
        ("TestCalculator", "test_multiplication", 9),  # Another class method
        (None, "non_existent_function", None),  # Function doesn't exist
        ("NonExistentClass", "test_method", None),  # Class doesn't exist
    ],
)
def test_find_function_line(
    sample_test_file: Path,
    class_name: str | None,
    func_name: str,
    expected_line: int | None,
) -> None:
    result = testjump.find_function_line(sample_test_file, class_name, func_name)
    assert result == expected_line


@pytest.mark.parametrize(
    ("editor", "file_path", "line", "expected_cmd"),
    [
        (
            "vscode",
            "tests/test_file.py",
            42,
            ["code", "-g", "tests/test_file.py:42"],
        ),
        (
            "vim",
            "tests/test_file.py",
            42,
            ["vim", "+42", "tests/test_file.py"],
        ),
        (
            "nvim",
            "tests/test_file.py",
            42,
            ["nvim", "+42", "tests/test_file.py"],
        ),
        (
            "idea",
            "tests/test_file.py",
            42,
            ["idea", "tests/test_file.py:42"],
        ),
        (
            "pycharm",
            "tests/test_file.py",
            42,
            ["pycharm", "tests/test_file.py:42"],
        ),
    ],
)
def test_get_editor_command(
    editor: str,
    file_path: str,
    line: int,
    expected_cmd: list[str],
) -> None:
    result = testjump.get_editor_command(editor, file_path, line)
    assert result == expected_cmd


def test_get_editor_command_invalid_editor() -> None:
    with pytest.raises(KeyError):
        testjump.get_editor_command("invalid_editor", "test.py", 1)
