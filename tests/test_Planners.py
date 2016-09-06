import pytest
from unittest.mock import MagicMock

from autotester.Planners import AbstractPlanner,NaiveAdaptivePlanner,NaiveFixedPlanner
from autotester.abstractions import *

@pytest.fixture(scope="function")
def adaptive():
    test_plan = NaiveAdaptivePlanner(adaptationTrigger=2)
    yield test_plan

@pytest.fixture(scope="function")
def fixed():
    test_plan = NaiveFixedPlanner()
    yield test_plan


def Test_AbstractPlanner():
    def test_init_raises(self):
        with pytest.raises(NotImplementedError):
            a = AbstractPlanner()
            a.get_adaptation(None,None)
            a.get_action(None,None)

class Test_NaiveFixedPlanner:
    def test_init(self):
        assert NaiveFixedPlanner()

    def test_get_action(self,fixed):
        state = None
        with pytest.raises(AttributeError):
            fixed.get_action(state)
        state = State.get_pristine()
        assert fixed.get_action(state)==HighLevelActions.FORM

    def test_get_adaptation(self,fixed):
        last_action = None
        state = None
        # TODO this should only ever return NOCHANGE and do nothing else, so no fancy test
        assert fixed.get_adaptation(last_action,state)== Adaptations.NOCHANGE

class Test_NaiveAdaptivePlanner:
    def test_init(self):
        assert NaiveFixedPlanner()

    def test_get_action(self,adaptive):
        state = None
        with pytest.raises(AttributeError):
            adaptive.get_action(state)
        state = State.get_pristine()
        assert adaptive.get_action(state)==HighLevelActions.FORM

    def test_get_adaptation(self,adaptive):
        last_action = None
        state = None
        with pytest.raises(AttributeError):
            adaptive.get_adaptation(last_action,state)
        assert False # TODO: write tests describing the expected choices
