import pytest
from unittest.mock import MagicMock

from autotester.NaiveTester import NaiveTester
from autotester.abstractions import *

@pytest.fixture(scope="function")
def estimator():
    est= MagicMock()
    est.estimate_state=MagicMock(return_value=State.get_pristine())
    yield est

@pytest.fixture(scope="function")
def planner():
    yield MagicMock()

@pytest.fixture(scope="function")
def executor():
    test_exec= MagicMock()
    test_exec.execute=MagicMock(return_value=(State.get_pristine(),None))
    yield test_exec

@pytest.fixture(scope="function")
def memory():
    yield MagicMock()

@pytest.fixture(scope="function")
def notificator():
    yield MagicMock()

@pytest.fixture(scope="function")
def tester(estimator,planner,executor,notificator,memory):
    yield NaiveTester(estimator,planner,executor,notificator,memory)

class Test_NaiveTester:
    def test_init_(self, estimator,planner,executor,notificator,memory):
        assert NaiveTester(estimator,planner,executor,notificator,memory)

    def test_run(self,tester):
        CURRENT_SAMPLE="test_sample"
        assert tester.run(CURRENT_SAMPLE,max_steps=100,startState=None)
