import pytest
from unittest.mock import MagicMock

from autotester.Executors import NaiveExecutor
from autotester.abstractions import *

@pytest.fixture(scope="function")
def tester():
    mock_tester = MagicMock()
    dummyout=(MagicMock(),MagicMock(),MagicMock())
    mock_tester.run_test=MagicMock(return_value=("ret",dummyout))
    yield mock_tester

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
    mock_precon_closure[HighLevelActions.READ]=MagicMock()
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
        executor.adapt(Adaptations.NOCHANGE)
        executor.adapt(Adaptations.SET_V_INC)
        executor.adapt(Adaptations.RESET_V_INC)
        executor.adapt(Adaptations.SET_V_DEC)
        executor.adapt(Adaptations.RESET_V_DEC)

        executor.adapt(Adaptations.SET_PV_INC)
        executor.adapt(Adaptations.RESET_PV_INC)
        executor.adapt(Adaptations.SET_PV_DEC)
        executor.adapt(Adaptations.RESET_PV_DEC)

    def test_checkR(self,executor):
      executor.checkR()

    def test_execute(self,executor,action):
      executor.execute(HighLevelActions.SET_PULSE)
      executor.execute(HighLevelActions.RESET_PULSE)

      executor.execute(HighLevelActions.SET_SWEEP)
      executor.execute(HighLevelActions.RESET_SWEEP)

      executor.execute(HighLevelActions.READ)
      executor.execute(HighLevelActions.FORM)
