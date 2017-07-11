sudo: false
dist: trusty
language: python
env:
    - REPO=DutchGraa/crackcoin
    - REPO=tensorflow/models
    - REPO=probcomp/bayeslite
    - REPO=anishathalye/seashells
    - REPO=AlexiaJM/Deep-learning-with-cats
    - REPO=fchollet/keras
    - REPO=warner/magic-wormhole
    - REPO=josephmisiti/awesome-machine-learning
    - REPO=scikit-learn/scikit-learn
    - REPO=meetshah1995/pytorch-semseg
    - REPO=pallets/flask
    - REPO=mandatoryprogrammer/TrustTrees
    - REPO=tensorflow/tensor2tensor
    - REPO=donnemartin/system-design-primer
    - REPO=astorfi/TensorFlow-World
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
    - flake8 . --count --select=E901,E999,F821,F822,F823 --statistics
    # exit-zero treats all errors as warnings.  The GitHub editor is 127 chars wide
    - flake8 . --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics
notifications:
    on_success: change
    on_failure: change  # `always` will be the setting once code changes slow down
