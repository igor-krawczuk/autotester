import pytest
from unittest.mock import MagicMock

from autotester.Executors import NaiveExecutor
from autotester.abstractions import *

@pytest.fixture(scope="function")
def tester():
    mock_tester = MagicMock()

@pytest.fixture(scope="function")
def sweep():
    mock_sweep_control = MagicMock()
    yield mock_sweep_control

@pytest.fixture(scope="function")
def pulse():
    mock_pulse_control = MagicMock()
    yield mock_pulse_control

@pytest.fixture(scope="function")
def adaptation():
    mock_adaptation = MagicMock()
    yield mock_adaptation

@pytest.fixture(scope="function")
def action():
    mock_action = MagicMock()
    yield mock_action

@pytest.fixture(scope="function")
def read_precon_closure():
    mock_precon_closure= MagicMock()
    yield mock_precon_closure

@pytest.fixture(scope="function")
def mock_executor():
    mock_executor= MagicMock()
    yield mock_executor

@pytest.fixture(scope="function")
def executor(tester, sweep,pulse, read_precon_closure):
    yield NaiveExecutor(tester, sweep,pulse, read_precon_closure)

class Test_NaiveExecutor:
    def test_init(tester, sweep,pulse, read_precon_closure):
        test_exec = NaiveExecutor(tester, sweep,pulse, read_precon_closure)
        assert test_exec

    def test_adapt(self,executor,adaptation):
        with pytest.raises(ValueError):
            executor.adapt(None)
        assert False #add more tests as we start to use adaptive Executor

    def test_checkR(self,executor):
        assert False

    def test_execute(self,executor,action):
        assert False
