# Itinerant Tester

Create a [.travis.yml](.travis.yml) file for running [flake8](http://flake8.pycqa.org/en/latest/) tests on each of the [GitHub Trending Python](https://github.com/trending?l=python) repos.

What about a different approach?  What if I hava a local Python command line app that accepts the name of one or more repos and it commits an updated .travis.yml file that tests those repos.  That commit will cause Travis CI to test each of those repos.

Appvayor https://github.com/google/protobuf/pull/4756
