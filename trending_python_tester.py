#!/usr/bin/env python3
"""
    Update the repo's '.travis.yml' to trigger Travis CI to run flake8 tests on
    the top 25 GitHub Trending Python repos.

    Requires: pip3 install --update beautifulsoup4 github3.py requests lxml
        If lxml is not available, html5lib should be a workable substitute
"""

import getpass
import webbrowser
from datetime import datetime as dt

# self._put_long_string("%s=%s" % (key, val))  # self, key, val: undefined names
import bs4  # will require lxml or html5lib
import requests
from github3 import login as github3_login

username = getpass.getuser()  # Does local username == GitHub username?
print('Please enter the GitHub password for user: {}'.format(username))
gh = github3_login(username, getpass.getpass())

# url = 'https://github.com/trending/jupyter-notebook'  # GitHub Trending top 25 repos
url = 'https://github.com/trending/python'  # GitHub Trending top 25 repos
# url += '?since=weekly'
# url += '?since=monthly'

# these repos pass tests, have pull requests to pass tests, or are Py3 only
ignore = []

# the boilerplate content of the .travis.yml file
fmt = """group: travis_latest
dist: xenial  # required for Python >= 3.7 (travis-ci/travis-ci#9069)
language: python
cache: pip
python:
  #- 2.7
  #- 3.4
  #- 3.5
  #- 3.6
  - 3.7
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
  - time flake8 . --count --select=E901,E999,F821,F822,F823 --show-source --statistics
  - echo exit-zero treats all errors as warnings.  The GitHub editor is 127 chars wide
  - time flake8 . --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics
  #- true  # pytest --capture=sys
notifications:
  on_success: change
  on_failure: change  # `always` will be the setting once code changes slow down
"""

print(f'{dt.now():%a %b %d %H:%M:%S %Z %Y}')
# extract the repo names of GitHub's Top 25 Trending Python list
soup = bs4.BeautifulSoup(requests.get(url).content, 'lxml')  # or 'html5lib'
# 'python / cpython'
repos = soup.find('ol', class_="repo-list").find_all('a', href=True)
# 'python/cpython'
repos = (repo.text.strip().replace(' ', '') for repo in repos
         if '/' in repo.text and '://' not in repo.text)
repos = list(repos) + ['PythonCharmers/python-future',
    # 'ansible/awx', 'cheshirekow/cmake_format', 'n1nj4sec/pupy',
    # 'ArduPilot/pymavlink', 'dronekit/dronekit-python',
    'ansible/ansible', 'Tribler/tribler', 'vnpy/vnpy', 'oaubert/python-vlc',
    'getsentry/sentry', 'CoreSecurity/impacket', 'ibm-watson-iot/functions',
    'nodejs/node', 'nodejs/node-gyp', 'internetarchive/openlibrary', 'google/ffn',
    'webpy/webpy', 'ibm-watson-iot/connector-cloudant', 'ibm-watson-iot/device-kodi',
    'ArduPilot/ardupilot', 'matplotlib/matplotlib', 'ckan/ckan', 'ggtracker/sc2reader',
    'apache/beam', 'apache/incubator-mxnet', 'apache/spark',
]
    # 'httplib2/httplib2', 'Supervisor/supervisor'
    # 'hyperledger/fabric-sdk-py', 'hyperledger/iroha-python']
# '    - REPO=python/cpython'  also strip out any repos that are in ignore list
repos = '\n'.join('  - REPO=' + repo for repo in repos)
#                 if 'shadowsocks' not in repo and repo not in ignore)
print(repos)
travis_text = fmt % repos

# log into GitHub and commit an update to .travis.yml which will trigger tests
travis = gh.repository(username, 'itinerant-tester').file_contents('/.travis.yml')
print(travis.update('trigger a new build', travis_text.encode('utf-8')))
webbrowser.open('https://travis-ci.org/{}/itinerant-tester'.format(username))
