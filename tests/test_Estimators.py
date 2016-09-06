import pytest
from unittest.mock import MagicMock

from autotester.Estimators import NaiveEstimator
from autotester.abstractions import *

@pytest.fixture(scope="function")
def estimator():
    test_est = NaiveEstimator(LRS_THRESHOLD, HRS_THRESHOLD, deep_THRESHOLD,annealGoal,burned_THRESHOLD)
    yield test_est


class Test_NaiveEstimator:
    def test_init(self):
        LRS_THRESHOLD=10e3
        HRS_THRESHOLD=20e3
        deep_THRESHOLD=5
        annealGoal=10
        burned_THRESHOLD=15
        test_est = NaiveEstimator(LRS_THRESHOLD, HRS_THRESHOLD, deep_THRESHOLD,annealGoal,burned_THRESHOLD)
        assert test_est

    def estimate_state(self,estimator):
        assert False

