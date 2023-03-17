#!/usr/bin/env python3
"""
    Update the repo's '.travis.yml' to trigger Travis CI to run flake8 tests on
    the top 25 GitHub Trending Python repos.

    Requires: pip3 install --upgrade beautifulsoup4 github3.py requests lxml
        If lxml is not available, html5lib should be a workable substitute
"""

import getpass
import webbrowser
from datetime import datetime as dt

# self._put_long_string("%s=%s" % (key, val))  # self, key, val: undefined names
import bs4  # will require lxml or html5lib
import requests
from github3 import login as github3_login

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:60.0)"
    " Gecko/20100101 Firefox/60.0"
}

token = "cf2800ef2802b619a8ca8bf360f68ee4547a38c3"


def my_two_factor_function():
    return input("Enter 2FA code: ").strip() or my_two_factor_function()


username = getpass.getuser()  # Does local username == GitHub username?
print("Please enter the GitHub password for user: {}".format(username))
gh = github3_login(username, token, two_factor_callback=my_two_factor_function)

# url = 'https://github.com/trending/jupyter-notebook'  # GitHub Trending top 25 repos
url = "https://github.com/trending/python"  # GitHub Trending top 25 repos
# url += '?since=weekly'
# url += '?since=monthly'

# these repos pass tests, have pull requests to pass tests, or are Py3 only
ignore = []

# the boilerplate content of the .travis.yml file
fmt = """group: travis_latest
dist: bionic
language: python
cache: pip
python:
  #- 2.7
  #- 3.5
  #- 3.6
  #- 3.7
  - 3.8
matrix:
  allow_failures:
    - python: 2.7
    - python: nightly
    - python: pypy
    - python: pypy3
env:
%s
install:
  #- pip install -r requirements.txt
  - pip install flake8  # pytest  # add other testing frameworks later
before_script:
  - URL=https://github.com/${REPO}
  - echo ; echo -n "flake8 testing of ${URL} on " ; python -V
  - git clone --depth=50 ${URL} ~/${REPO}  # --branch=master
  - cd ~/${REPO}
script:
  - echo stop the build if there are Python syntax errors or undefined names
  - echo ; echo -n "flake8 testing of ${URL} on " ; python -V
  - time flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
  - echo exit-zero treats all errors as warnings.  The GitHub editor is 127 chars wide
  - time flake8 . --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics
  #- true  # pytest --capture=sys
notifications:
  on_success: change
  on_failure: change  # `always` will be the setting once code changes slow down
"""  # noqa: E501

print(f"{dt.now():%a %b %d %H:%M:%S %Z %Y}")
# extract the repo names of GitHub's Top 25 Trending Python list
soup = bs4.BeautifulSoup(
    requests.get(url, headers=HEADERS).content, "lxml"
)  # or 'html5lib'
# 'python / cpython'
# repos = soup.find('ol', class_="repo-list").find_all('a', href=True)
repos = [h3.find("a", href=True) for h3 in soup.find_all(class_="h3 lh-condensed")]
print(repos)
# 'python/cpython'
repos = (
    repo.text.strip().replace(" ", "").replace("\n" * 4, "")
    for repo in repos
    if "/" in repo.text and "://" not in repo.text
)
repos = list(repos) + [
    "n1nj4sec/pupy",
    "PythonCharmers/python-future",
    "ansible/ansible",
    "oaubert/python-vlc",
    "ColdGrub1384/Pyto",
    "CoreSecurity/impacket",
    "internetarchive/openlibrary",
    "google/ffn",
    "apache/beam",
    "apache/incubator-mxnet",
    "hyperledger/iroha-python",
    "Supervisor/supervisor",
    "cheshirekow/cmake_format",
    "ckan/ckan",
    "ibm-watson-iot/connector-cloudant",
    "ibm-watson-iot/device-kodi",
    "ibm-watson-iot/functions",
    "apache/spark",
    "Tribler/tribler",
    "webpy/webpy",
    "nodejs/node",
    "nodejs/node-gyp",
    "ArduPilot/ardupilot",
    "ArduPilot/pymavlink",
    "dronekit/dronekit-python",
    "ansible/awx",
    "matplotlib/matplotlib",
    "ggtracker/sc2reader",
    "httplib2/httplib2",
    "hyperledger/fabric-sdk-py",
    "getsentry/sentry",
    "v8/v8",
]
# '    - REPO=python/cpython'  also strip out any repos that are in ignore list
repos = "\n".join("  - REPO=" + repo for repo in repos)
#                 if 'shadowsocks' not in repo and repo not in ignore)
print(repos)
travis_text = fmt % repos

# log into GitHub and commit an update to .travis.yml which will trigger tests
travis = gh.repository(username, "itinerant-tester").file_contents("/.travis.yml")
print(travis.update("trigger a new build", travis_text.encode("utf-8")))
webbrowser.open("https://travis-ci.com/{}/itinerant-tester".format(username))
