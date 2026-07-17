#!/usr/bin/env python3
"""Generate ruff TOML config from ruff output."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from subprocess import run


@dataclass
class NameDefaultMaximum:
    name: str
    default: int
    maximum: int = 0

    def __str__(self) -> str:
        return f"{self.name} = {self.maximum}  # Default is {self.default}"

    def get_maximum(self) -> int:
        """Only return a maximum value if it is greater than the default."""
        return self.maximum if self.maximum > self.default else 0


def ruff_pylint_settings() -> str:
    """
    Generate ruff.toml settings for pylint rules: PLR0911, PLR0912, PLR0913, PLR0915.

    Run the command: `ruff check --quiet --select=PLR091 .`

    Convert the resulting text into output of the form:
    [tool.ruff.lint.pylint]
        PLR0911 = 7  # Default is 6
        PLR0912 = 13  # Default is 12
        PLR0913	= 15  # Default is 5
        PLR0915	= 104  # Default is 50

    The highest value for each rule should be used.
    """
    x = run(
        ["ruff", "check", "--quiet", "--select=PLR091", "../paho.mqtt.python"],
        capture_output=True,
        check=False,
        text=True,
    )
    if x.returncode == 0:  # If there were no PLR091x errors...
        return ""
    rules = {
        "PLR0913": NameDefaultMaximum("max-args", 5),
        "PLR0912": NameDefaultMaximum("max-branches", 12),
        "PLR0911": NameDefaultMaximum("max-returns", 6),
        "PLR0915": NameDefaultMaximum("max-statements", 50),
    }
    for line in x.stdout.splitlines():
        _, rule, *parts = line.split()
        rules[rule].maximum = max(rules[rule].maximum, int(parts[-3].replace("(", "")))
    if not any(ndm.get_maximum() for ndm in rules.values()):  # No PLR091x violations.
        return ""
    return "\n".join(
        ["[tool.ruff.lint.pylint]", 'allow-magic-value-types = ["str"]']
        + [str(ndm) for ndm in rules.values() if ndm.get_maximum()]
    )


linters_as_text = run("ruff linter", capture_output=True, shell=True, text=True).stdout


def rule_fmt(rule_family: str = "PLR") -> str:
    """
    >>> rule_fmt("A")
    '"A",  '
    >>> rule_fmt("AB")
    '"AB", '
    >>> rule_fmt("ABC")
    '"ABC",'
    >>> rule_fmt("# ABC")  # Move the comment (#) before the quote
    '# "ABC",'
    """
    return """{:<8}""".format(f'"{rule_family}",').replace('"# ', '# "')


def select_lines(s: str = linters_as_text) -> str:
    linters = dict(line.strip().split(" ", 1) for line in linters_as_text.splitlines())
    linters["C90"] = "McCabe cyclomatic complexity"
    value = linters.pop("E/W")  # Split E and W into two separate linters
    for key in "EW":
        linters[key] = value
    for key in ("COM", "ERA", "Q", "T20"):
        linters[f"# {key}"] = linters.pop(key)  # Comment out some less useful linters
    linters["# PLR091"] = "Pylint Refactor just for max-args, max-branches, etc."
    return "\n".join(
        f"  {rule_fmt(code)}  # {name}" for code, name in sorted(linters.items())
    )


ruff_header = f"""
[tool.ruff]
target-version = "py310"

[tool.ruff.lint]
select = [
{select_lines()}
]
# ignore = []
target-version = "py310"
"""

ruff_pylint_header = """
[tool.ruff.lint.pylint]"""


def tests_may_assert(dir_name: str = "tests") -> str:
    """If a test directory exists, then add a per-file-ignore to allow `assert`."""
    return f'\n"{dir_name}/*" = ["S101"]' if (Path.cwd() / dir_name).is_dir() else ""


ruff_per_file_includes_header = (
    """
[tool.ruff.lint.per-file-ignores]
"__init__.py" = ["E402"]
"""
    + tests_may_assert("test")
    + tests_may_assert("tests")
)


def ruff_config_gen(lines: list[str]) -> None:
    """Generate ruff TOML config from ruff output.

    ex. ruff --select=ALL --quiet . | ./ruff_config_gen.py
    line-length = 148
    max-branches = 21
    max-statements = 60
    """
    rules = {
        "E501": "line-length",
        "C901": "\n[tool.ruff.lint.mccabe]\nmax-complexity",
    }
    print(ruff_header)
    for rule, config in rules.items():
        # print(rule, config)
        if maximum := max(
            (int(_.split("(")[-1].split()[0]) for _ in lines if _.split()[1] == rule),
            default=0,
        ):
            print(f"{config} = {maximum}")  # noqa: T201
    if s := ruff_pylint_settings():
        print(s)
    # print(ruff_pylint_header)
    print(ruff_per_file_includes_header)


if __name__ == "__main__":
    from sys import stdin

    ruff_config_gen(lines=stdin.readlines()[:-1])
