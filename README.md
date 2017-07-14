# Itinerant Tester

Create a [.travis.yml](.travis.yml) file for running [flake8](http://flake8.pycqa.org/en/latest/) tests on the [GitHub Trending Python](https://github.com/trending?l=python) repos.

What about a different approach?  What if I hava a local Python command line app that accepts the that of a repo or repos and commits a new .travis.yml file to this repo that contains the command line repos.  That commit will cause this repo to run tests on the command line repos.
