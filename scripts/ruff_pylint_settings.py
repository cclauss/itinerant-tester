from dataclasses import dataclass
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

    Run the command: `ruff --quiet --select=PLR091 .`

    Convert the resulting text into output of the form:
    [tool.ruff.pylint]
        PLR0911 = 7  # Default is 6
        PLR0912 = 13  # Default is 12
        PLR0913	= 15  # Default is 5
        PLR0915	= 104  # Default is 50

    The highest value for each rule should be used.
    """
    x = run(
        ["ruff", "--quiet", "--select=PLR091", "../paho.mqtt.python"],
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
        ["[tool.ruff.pylint]", 'allow-magic-value-types = ["str"]']
        + [str(ndm) for ndm in rules.values() if ndm.get_maximum()]
    )


if __name__ == "__main__":
    print(ruff_pylint_settings())
