import pytest
import pandas as pd
from unittest.mock import MagicMock

from autotester.abstractions import *

@pytest.fixture()
def adp():
  yield Adaptations.NOCHANGE

@pytest.fixture()
def act():
  yield HighLevelActions.READ

@pytest.fixture()
def state():
  yield State.get_pristine()

@pytest.fixture()
def testd(act):
  yield testerData(act,pd.DataFrame(dict(one=[1,2,3],two=[5,6,7])))

@pytest.fixture()
def datum():
  yield Datum(R=5,V=5,gateV=5,timesAnnealed=5,wasPulse=5)

class Test_State:
  def test_init(self):
    s = State(LRS=False,HRS=True,burnedOut=False,burnedThrough=False,deep=False,annealed=True,untouched=False,actionsSinceStateChange=0)
    assert s

  def test_to_dict(self,state):
    assert state.to_dict(5)["log_id"]==5

class Test_Datum:
  def test_init(self):
    s = Datum(R=5,V=5,gateV=5,timesAnnealed=5,wasPulse=5)
  def test_to_dict(self,datum):
    assert datum.to_dict(5)["log_id"]==5

class Test_TesterData:
  def test_init(self,act):
    td= testerData(act)
    assert td.frame is None

  def test_to_dict(self,testd):
    td= testerData(act)
    assert td.to_dict()
    assert testd.to_dict()

@pytest.fixture()
def pulseC():
    p=pulseControl(tester=None,setV=1.5,setGateV=1,resetV=5,resetGateV=1.0,width=1,slope=0.5)
@pytest.fixture()

def sweepC():
    p=sweepControl(tester=None,setV=1.5,setGateV=1,resetV=5,resetGateV=1.0)

@pytest.fixture()
def log(adp,act,state,pulseC,sweepC,testd):
  yield Log(local_id=0,adaptation=adp,action=act,startState=state,endState=state,pulseControl=pulseC,sweepControl=sweepC,run_id=5,datum=datum,testerData=testd)

class Test_Log:
  def test_init(self,testd,adp,act,datum,state,pulseC,sweepC):
    log = Log(local_id=0,adaptation=adp,action=act,startState=state,endState=state,pulseControl=pulseC,sweepControl=sweepC,run_id=5,datum=datum,testerData=testd)

  def test_to_dicts(self,log):
    d=log.test_to_dicts()
    assert isinstance(d,dict)
    # since we iterate over this to determine tables, we need to be sure that they are all dicts as well
    for k,v in d.items():
      assert isinstance(v,dict)


class Test_PulseControl:
  def test_init(self):
    p=pulseControl(tester=None,setV=1.5,setGateV=1,resetV=5,resetGateV=1.0,width=1,slope=0.5)
    assert p

class Test_SweepControl:
  def test_init(self):
    s=sweepControl(tester=None,setV=1.5,setGateV=1,resetV=5,resetGateV=1.0,width=1,slope=0.5)
    assert p
