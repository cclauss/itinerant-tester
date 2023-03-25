name: type_hint_test
on: [push]
jobs:
  type_hint_test:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/setup-python@v4
        with:
          python-version: |
            3.7
            3.8
            3.9
            3.10
            3.11
    - run: python3.11 -c "def func(x: str | None) -> None; pass
    - run: python3.10 -c "def func(x: str | None) -> None; pass
    - run: python3.9 -c "def func(x: str | None) -> None; pass
    - run: python3.8 -c "def func(x: str | None) -> None; pass
    - run: python3.7 -c "def func(x: str | None) -> None; pass
