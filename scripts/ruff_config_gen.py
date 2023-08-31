#!/usr/bin/env python3
"""Generate ruff TOML config from ruff output."""

from __future__ import annotations

from subprocess import run

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
    for key in ("COM", "DJ", "ERA", "NPY", "PD", "Q", "T20"):
        linters[f"# {key}"] = linters.pop(key)  # Comment out some less useful linters
    linters["# PLR091"] = "Pylint Refactor just for max-args, max-branches, etc."
    return "\n".join(
        f"  {rule_fmt(code)}  # {name}" for code, name in sorted(linters.items())
    )


ruff_header = f"""
[tool.ruff]
select = [
{select_lines()}
]
# ignore = []
target-version = "py37"
"""

ruff_pylint_header = """
[tool.ruff.pylint]"""

ruff_per_file_includes_header = """
[tool.ruff.per-file-ignores]
"__init__.py" = ["E402"]
"test/*" = ["S101"]
"""


def ruff_config_gen(lines: list[str]) -> None:
    """Generate ruff TOML config from ruff output.

    ex. ruff --select=ALL --quiet . | ./ruff_config_gen.py
    line-length = 148
    max-branches = 21
    max-statements = 60
    """
    rules = {
        "E501": "line-length",
        "C901": "\n[tool.ruff.mccabe]\nmax-complexity",
        "PLR2004": 'allow-magic-value-types = ["int", "str"]',
        "PLR0913": "max-args  # Recommended: 5",
        "PLR0912": "max-branches  # Recommended: 12",
        "PLR0911": "max-returns  # Recommended: 6",
        "PLR0915": "max-statements  # Recommended: 50",
    }
    print(ruff_header)
    need_pylint_header = True
    for rule, config in rules.items():
        print(rule, config)
        try:
            if maximum := max(
                (
                    int(_.split("(")[-1].split()[0])
                    for _ in lines
                    if _.split()[1] == rule
                ),
                default=0,
            ):
                if need_pylint_header and rule.startswith("PL"):
                    print(ruff_pylint_header)
                    need_pylint_header = False
                print(f"{config} = {maximum}")  # noqa: T201
        except ValueError as e:
            raise ValueError(_) from e
    print(ruff_per_file_includes_header)


if __name__ == "__main__":
    from sys import stdin

    ruff_config_gen(lines=stdin.readlines()[:-1])
