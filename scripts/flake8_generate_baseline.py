#!usr//bin/env python3

from subprocess import run  # Requires Python >= 3.7
from typing import Tuple

flake8_out: Tuple[str] = tuple(
    run(
        ["flake8", "--max-complexity=1", "."], capture_output=True, text=True
    ).stdout.splitlines()
)


def get_max_complexity(flake8_out: Tuple[str] = flake8_out) -> int:
    C901_TAG = " is too complex ("
    c901_lines = [line for line in flake8_out if "C901" in line and C901_TAG in line]
    return max(int(line.split(C901_TAG)[-1].split(")")[0]) for line in c901_lines)


def get_max_line_length(flake8_out: Tuple[str] = flake8_out) -> int:
    E501_TAG = ": E501 line too long ("
    e501_lines = [line for line in flake8_out if E501_TAG in line]
    return max(int(line.split(E501_TAG)[-1].split()[0]) for line in e501_lines)


if __name__ == "__main__":
    violations = set(line.split()[1] for line in flake8_out)

    try:
        violations.remove("C901")
        max_complexity = f"--max-complexity={max(get_max_complexity(), 10)} "
    except KeyError:
        max_complexity = ""

    try:
        violations.remove("E501")
        max_line_length = f"--max-line-length={max(get_max_line_length(), 88)} "
    except KeyError:
        max_line_length = ""

    ignore = f"--ignore={','.join(sorted(violations))} " if violations else ""
    flake8_cmd = (
        f"flake8 {ignore}{max_complexity}{max_line_length}--show-source --statistics ."
    )
    print(flake8_cmd)
    run(flake8_cmd.split(), text=True)
