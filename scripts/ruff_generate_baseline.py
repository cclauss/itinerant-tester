#!usr//bin/env python3
from __future__ import annotations

from subprocess import run  # Requires Python >= 3.7

ruff_out: tuple[str] = tuple(
    run(
        ["ruff", "check", "--extend-select=C90", "."], capture_output=True, text=True
    ).stdout.splitlines()[:-2]  # Remove the two summary lines
)


def get_max_complexity(ruff_out: tuple[str] = ruff_out) -> int:
    C901_TAG = " is too complex ("
    c901_lines = [line for line in ruff_out if "C901" in line and C901_TAG in line]
    if not c901_lines:
        return 0
    return max(int(line.split(C901_TAG)[-1].split(")")[0]) for line in c901_lines)


def get_max_line_length(ruff_out: tuple[str] = ruff_out) -> int:
    E501_TAG = ": E501 line too long ("
    e501_lines = [line for line in ruff_out if E501_TAG in line]
    if not e501_lines:
        return 0
    return max(int(line.split(E501_TAG)[-1].split()[0]) for line in e501_lines)


if __name__ == "__main__":
    print(ruff_out)
    violations = set(line.split()[1] for line in ruff_out)
    if (mc := get_max_complexity()) > 10:
        max_complexity = f"  # --max-complexity={mc}"
    else:
        max_complexity = ""
    try:
        violations.remove("E501")
        line_length = f"--line-length={max(get_max_line_length(), 88)} "
    except KeyError:
        line_length = ""

    ignore = f"--ignore={','.join(sorted(violations))} " if violations else ""
    ruff_cmd = f"ruff check {ignore}{line_length}--show-source --statistics .{max_complexity}"
    print(ruff_cmd)
    run(ruff_cmd.split(), text=True)
