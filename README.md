# Itinerant Tester

[![Open in VS Code](https://open.vscode.dev/badges/open-in-vscode.svg)](https://open.vscode.dev/cclauss/itinerant-tester)

Create a [.travis.yml](.travis.yml) file for running [flake8](http://flake8.pycqa.org/en/latest/) tests on each of the [GitHub Trending Python](https://github.com/trending?l=python) repos.

What about a different approach?  What if I have a local Python command line app that accepts the name of one or more repos and it commits an updated .travis.yml file that tests those repos.  That commit will cause Travis CI to test each of those repos.

Appveyor https://github.com/google/protobuf/pull/4756

```
% bandit --recursive . > bandit.txt
% python3
>>> with open("bandit.txt") as in_file:
...     errors = sorted(set(line[11:15] for line in in_file if line.startswith(">> ")))
...
>>> print(",".join(errors))
B101,B102,B105,B106,B107,B110,B303,B311,B320,B403,B404,B410,B602,B603,B604,B607,B608,B701
```
