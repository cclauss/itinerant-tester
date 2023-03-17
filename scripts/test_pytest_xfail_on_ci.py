import os

import pytest


@pytest.mark.xfail("CI" in os.environ, reason="May fail on continuous integration")
def test_ci_upper():
    raise ValueError("This is only a test...")


# @pytest.mark.xfail("ci" in os.environ, reason="May fail on continuous integration")
# def test_ci_lower():
#    raise ValueError("This is only a test...")
