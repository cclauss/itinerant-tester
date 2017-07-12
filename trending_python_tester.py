#!/usr/bin/env python3

import bs4
import requests
"""
    Creates a .travis.yml file for running flake8
    tests on the top 25 GitHub Trending Python repos.
"""

ignore = ['0x4D31/honeyLambda', 'andreiapostoae/dota2-predictor',
          'anishathalye/seashells', 'ansible/ansible',
          'dizballanze/django-eraserhead', 'django/django', 'iogf/crocs',
          'jadore801120/attention-is-all-you-need-pytorch', 'jisungk/RIDDLE',
          'jmathai/elodie', 'jordanpotti/AWSBucketDump', 'lmcinnes/umap',
          'meetshah1995/pytorch-semseg', 'metachris/logzero',
          'pfnet-research/chainer-gan-lib', 'python/cpython', 'rg3/youtube-dl',
          'songrotek/Deep-Learning-Papers-Reading-Roadmap',
          'vinta/awesome-python', 'vividvilla/csvtotable']

fmt = """sudo: false
dist: trusty
language: python
env:
%s
python:
    - 2.7.13
    - 3.6.1
install:
    - pip install flake8  # pytest  # add some test later
script:
    - URL=https://github.com/${REPO}
    - git clone --depth=50 --branch=master ${URL} ~/${REPO}
    - cd ~/${REPO}
    - echo ; echo -n "flake8 testing of ${URL} on " ; python -V
    # stop the build if there are Python syntax errors or undefined names
    - flake8 . --count --select=E901,E999,F821,F822,F823 --show-source --statistics
    # exit-zero treats all errors as warnings.  The GitHub editor is 127 chars wide
    - flake8 . --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics
notifications:
    on_success: change
    on_failure: change  # `always` will be the setting once code changes slow down

"""

url = 'https://github.com/trending?l=Python'
soup = bs4.BeautifulSoup(requests.get(url).content, 'lxml')  # or 'html5lib'
# 'python / cpython'
repos = soup.find('ol', class_="repo-list").find_all('a', href=True)
# 'python/cpython'
repos = (r.text.strip().replace(' ', '') for r in repos if '/' in r.text)
# '    - REPO=python/cpython'
repos = '\n'.join('    - REPO=' + repo for repo in repos if repo not in ignore)
print(fmt % repos)
