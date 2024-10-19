#!/usr/bin/env python3

# ruff: noqa: T201

"""Usage: ruff check --select=ALL --statistics | ./ruff_exclude.py ."""

from __future__ import annotations

from string import digits
from subprocess import run
from sys import stdin


def quoted(s: str) -> str:
    """Return a double-quoted string.

    >>> quoted("s")
    '"s"'
    >>> quoted('s')
    '"s"'
    >>> quoted(None)
    '"None"'
    """
    return f'"{s}"'


def ruff_linters() -> dict[str, str]:
    """Call `ruff linter` and return a dict of {rule_family: description}."""
    lines = run(  # noqa: S603
        ["ruff", "linter"],  # noqa: S607
        capture_output=True,
        check=True,
        text=True,
    ).stdout.splitlines()
    linters = {
        key: value for line in lines for key, value in [line.strip().split(" ", 1)]
    }
    e_w = linters.pop("E/W")
    linters["E"] = f"{e_w} errors"
    linters["W"] = f"{e_w} warnings"
    pylint = linters.pop("PL")
    linters["PLC"] = f"{pylint} conventions"
    linters["PLE"] = f"{pylint} errors"
    linters["PLR"] = f"{pylint} refactorings"
    linters["PLW"] = f"{pylint} warnings"
    return linters


if __name__ == "__main__":
    violations = {line.split()[1].rstrip(digits) for line in stdin}
    lines = [
        f'  {"#" if key in violations else " "} {quoted(key):<7} # {value}'
        for key, value in ruff_linters().items()
    ]
    print("[tools.ruff.lint]\nexclude = [")
    print("\n".join(sorted(lines)))
    print("]")
