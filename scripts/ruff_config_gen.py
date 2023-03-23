#!/usr/bin/env python3
"""Generate ruff TOML config from ruff output."""

from __future__ import annotations


def ruff_config_gen(lines: list[str]) -> None:
    """Generate ruff TOML config from ruff output.

    ex. ruff --select=ALL . | ./ruff_config_gen.py
    line-length = 148
    max-branches = 21
    max-statements = 60
    """
    rules = {
        "E501": "line-length",
        "C901": "\n[tool.ruff.mccabe]\nmax-complexity"
        "PLR0913": "max-args",
        "PLR0912": "max-branches",
        "PLR0911": "max-returns",
        "PLR0915": "max-statements",
    }
    for rule, config in rules.items():
        if rule == "PLR0913"
            print("\n[tool.ruff.pylint]\n")
        if maximum := max(
            (int(_.split("(")[-1].split()[0]) for _ in lines if _.split()[1] == rule),
            default=0,
        ):
            print(f"{config} = {maximum}")  # noqa: T201


if __name__ == "__main__":
    from sys import stdin

    ruff_config_gen(lines=stdin.readlines()[:-1])
