#!usr//bin/env python3
from __future__ import annotations

from subprocess import run  # Requires Python >= 3.7

ruff_out: tuple[str] = tuple(
    line for line in run(
        ["ruff", "--extend-select=C90", "."], capture_output=True, text=True
    ).stdout.splitlines() if not line.startswith("warning:")
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
    violations = set(line.split()[1] for line in ruff_out)
    max_complexity = f"  # --max-complexity={mc}" if (mc := get_max_complexity()) > 10 else ""
    try:
        violations.remove("E501")
        max_line_length = f"--max-line-length={max(get_max_line_length(), 88)} "
    except KeyError:
        max_line_length = ""

    ignore = f"--ignore={','.join(sorted(violations))} " if violations else ""
    ruff_cmd = (
        f"ruff {ignore}{max_line_length}--show-source --statistics .{max_complexity}" 
    )
    print(ruff_cmd)
    run(ruff_cmd.split(), text=True)
