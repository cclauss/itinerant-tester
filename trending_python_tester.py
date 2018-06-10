#!/usr/bin/env python3
"""
    Update the repo's '.travis.yml' to trigger Travis CI to run flake8 tests on
    the top 25 GitHub Trending Python repos.

    Requires: pip3 install --update beautifulsoup4 github3.py requests lxml
        If lxml is not available, html5lib should be a workable substitute
"""

# self._put_long_string("%s=%s" % (key, val))  # self, key, val: undefined names
import bs4  # will require lxml or html5lib
import getpass
import requests
import webbrowser
from datetime import datetime as dt
from github3 import login as github3_login

username = getpass.getuser()  # Does local username == GitHub username?
print('Please enter the GitHub password for user: {}'.format(username))
gh = github3_login(username, getpass.getpass())

url = 'https://github.com/trending/python'  # GitHub Trending top 25 repos
# url += '?since=weekly'
# url += '?since=monthly'

# these repos pass tests, have pull requests to pass tests, or are Py3 only
ignore = sorted([
    '0x4D31/honeyLambda', '521xueweihan/HelloGitHub', 'Cisco-Talos/pyrebox',
    'ExplorerFreda/Structured-Self-Attentive-Sentence-Embedding',
    'Kaixhin/NoisyNet-A3C', 'PyCQA/flake8', 'StevenBlack/hosts',
    'UltimateHackers/Hash-Buster', 'aboul3la/Sublist3r', 'allenai/allennlp',
    'ageitgey/face_recognition', 'airbnb/binaryalert', 'munificent/vigil',
    'andreiapostoae/dota2-predictor', 'anishathalye/seashells',
    'ansible/ansible', 'appsecco/bugcrowd-levelup-subdomain-enumeration',
    'astorfi/pythonic-automatic-email', 'astrofrog/mpl-scatter-density',
    'benjaminp/six', 'bethgelab/foolbox', 'channelcat/sanic', 'scrapy/scrapy',
    'chenjiandongx/pyecharts', 'cloudflare/receipt-printer',
    'csxeba/brainforge', 'dizballanze/django-eraserhead', 'django/django',
    'dmulholland/ivy', 'facebookresearch/DrQA', 'fchollet/keras',
    'friggog/tree-gen', 'home-assistant/home-assistant', 'iogf/crocs',
    'jadore801120/attention-is-all-you-need-pytorch',
    'jaesik817/visual-interaction-networks_tensorflow', 'jakubroztocil/httpie',
    'jisungk/RIDDLE', 'jmathai/elodie', 'jordanpotti/AWSBucketDump',
    'jrg365/gpytorch', 'lanpa/tensorboard-pytorch', 'leesoh/yams',
    'littlecodersh/ItChat', 'lmcinnes/umap', 'maciejkula/spotlight',
    'madeye/sssniff', 'meetshah1995/pytorch-semseg', 'metachris/logzero',
    'mitmproxy/mitmproxy', 'neufv/put-me-on-a-watchlist', 'openai/baselines',
    'pfnet-research/chainer-gan-lib', 'polyaxon/polyaxon', 'python/cpython',
    'quiltdata/quilt', 'reiinakano/xcessiv', 'reinforceio/tensorforce',
    'requests/requests', 'rg3/youtube-dl', 'sensepost/objection',
    'songrotek/Deep-Learning-Papers-Reading-Roadmap', 'cujanovic/SSRF-Testing',
    'strizhechenko/netutils-linux', 'vinta/awesome-python', 'QUVA-Lab/artemis',
    'vividvilla/csvtotable', 'worawit/MS17-010', 'yeleman/py3compat',
    'CQFIO/PhotographicImageSynthesis', 'hylang/hy', 'liangliangyy/DjangoBlog',
    'neozhaoliang/pywonderland', 'warner/magic-wormhole', 'bugcrowdlabs/HUNT',
    'fendouai/FaceRank', 'nottombrown/rl-teacher', 'TailorDev/Watson',
    'OmkarPathak/pygorithm', 'jamesob/tinychain', 'TorchCraft/StarData',
    'aaronduino/asciidots', 'nccgroup/demiguise', 'alexhude/uEmu',
    'codezjx/netease-cloud-music-dl', 'pytorch/pytorch', 'pennsignals/aptos',
    'brendan-rius/jupyter-c-kernel', 'vahidk/EffectiveTensorflow',
    'jiajunhuang/blog', 'apache/incubator-superset', 'lllyasviel/style2paints',
    'josephmisiti/awesome-machine-learning', 'bugcrowd/HUNT', 'taolei87/sru',
    'mil-tokyo/webdnn', 'chrisranderson/beholder', 'chainer/chainercv',
    'encode/apistar', 'Plazmaz/LNKUp', 'miyuchina/mistletoe', 'jtoy/sketchnet',
    'ent1c3d/Python-Synopsis', 'GoogleCloudPlatform/distroless',
    'csurfer/pyheatmagic', 'crazyguitar/pysheeet', 'unsky/focal-loss',
    'theocean154/algo-coin', 'ajbrock/SMASH', 'graphistry/pygraphistry',
    'LewisVo/Awesome-Linux-Software', 'kuangliu/pytorch-retinanet',
    'deibit/cansina', 'salesforce/awd-lstm-lm', 'facebook/codemod',
    'lk-geimfari/mimesis', 'minimaxir/reactionrnn', 'tensorflow/cleverhans',
    'elifesciences/sciencebeam', 'zalandoresearch/fashion-mnist',
    'eldraco/Salamandra', 'woozzu/dong_iccv_2017', 'justdoit0823/pywxclient',
    'jmhessel/fmpytorch', 'kryptxy/torrench', 'beaston02/ChaturbateRecorder',
    'hwalsuklee/tensorflow-generative-model-collections', 'reddit/reddit',
    'lufficc/flask_ishuhui', 'parrt/lolviz', 'nicolargo/glances',
    'sanyam5/arc-pytorch', 'corna/me_cleaner', 'beaston02/MFCRecorder',
    'NoneGG/aredis', 'satwikkansal/wtfpython', 'mli/gluon-tutorials-zh',
    'fendouai/Awesome-Chatbot', 'gavin66/proxy_list', 'chainside/btcpy',
    'pshah123/console-logging', 'postmarketOS/pmbootstrap', 'ofek/hatch',
    'facebookresearch/loop', 'fendouai/Awesome-TensorFlow-Chinese',
    'localstack/localstack', 'Hironsan/anago', 'harleyQu1nn/AggressorScripts',
    'tensorflow/agents', 'NVIDIA/DeepRecommender', 'vulnersCom/api',
    'mazen160/struts-pwn_CVE-2017-9805', 'ablator/ablator', 'soimort/you-get',
    'XX-net/XX-Net', 'ajbouh/tfi', 'facebookresearch/fairseq-py',
    'hannob/optionsbleed', 'eriklindernoren/ML-From-Scratch',
    '1adrianb/face-alignment', 'Lz1y/CVE-2017-8759',
    'laixintao/python-parallel-programming-cookbook-cn'

])
ignore = []

# the boilerplate content of the .travis.yml file
fmt = """group: travis_latest
language: python
env:
%s
cache: pip
python:
    #- 2.7
    - 3.6
    #- nightly
    #- pypy
    #- pypy3
matrix:
    allow_failures:
        - python: nightly
        - python: pypy
        - python: pypy3
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
repos = list(repos) + ['matplotlib/matplotlib', 'ckan/ckan',
    'ggtracker/sc2reader', 'vnpy/vnpy',
    # 'ansible/awx', 'cheshirekow/cmake_format',
    # 'ArduPilot/ardupilot', 'ArduPilot/pymavlink', 'dronekit/dronekit-python',
    'PythonCharmers/python-future', 'ansible/ansible', 'apache/beam',
    'apache/spark', 'gevent/gevent', 'getsentry/sentry', 'hyperledger/fabric']
    # 'httplib2/httplib2', 'Supervisor/supervisor'
    # 'hyperledger/fabric-sdk-py', 'hyperledger/iroha-python']
# '    - REPO=python/cpython'  also strip out any repos that are in ignore list
repos = '\n'.join('    - REPO=' + repo for repo in repos)
#                 if 'shadowsocks' not in repo and repo not in ignore)
print(repos)
travis_text = fmt % repos

# log into GitHub and commit an update to .travis.yml which will trigger tests
travis = gh.repository(username, 'itinerant-tester').file_contents('/.travis.yml')
print(travis.update('trigger a new build', travis_text.encode('utf-8')))
webbrowser.open('https://travis-ci.org/{}/itinerant-tester'.format(username))
