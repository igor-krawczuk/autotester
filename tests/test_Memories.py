import pytest
from unittest.mock import MagicMock,patch,Mock

from autotester.Memories import NaiveMemory,PostgresMemory
from autotester.abstractions import *
import pandas as pd

@pytest.fixture()
def state():
  yield State.get_pristine()

@pytest.fixture(scope="function")
def tester_data():
  yield testerData(HighLevelActions.READ,pd.DataFrame(dict(one=[1,2,3],two=[5,6,7])))

@pytest.fixture(scope="class")
def naive_mem():
  yield NaiveMemory()

@pytest.fixture()
def pulseC():
  yield pulseControl(None,0,0,0,0,0,0)

@pytest.fixture()
def sweepC():
  yield sweepControl(None,0,0,0,0)

@pytest.fixture()
def datum():
    yield Datum(0,0,0,0,0,0)

@pytest.fixture(autouse=True)
def no_dataset(monkeypatch):
    dummy_db=MagicMock()
    def getitem(*args,**kwargs):
      dummy_runs=MagicMock(return_value=1,name="insert_runs")
      dummy_runs.insert=Mock(return_value=1)
      dummy_runs.find_one=Mock(return_value=1)
      dummy_table=MagicMock(return_value=1,name="table")
      dummy_table.find_one=Mock(return_value=1)
      dummy_table.insert=Mock(return_value=1)
      if len(args)==1 and args[0]=="run":
        print("runs")
        return dummy_runs
      else:
        print("table")
        return dummy_table

      return dummy_table
    dummy_connection=MagicMock(side_effect=getitem)
    dummy_connection.__getitem__=getitem
    dummy_db=MagicMock(return_value=dummy_connection)
    monkeypatch.setattr("dataset.connect", dummy_db)

@pytest.fixture(autouse=True)
def no_dill(monkeypatch):
    dill=MagicMock()
    monkeypatch.setattr("dill.pickle", MagicMock())
    monkeypatch.setattr("autotester.Memories.dill.pickle", MagicMock())


class Test_NaiveMemory:
  def test_init(self):
    naive_mem = NaiveMemory()
    assert naive_mem.next_id ==1
    assert len(naive_mem.test_log)==0

  def test_log(self,naive_mem,state,tester_data,pulseC,sweepC,datum):
    naive_mem.log(Adaptations.NOCHANGE,
        HighLevelActions.READ,
        state,
        state,
        pulseC,sweepC,tester_data,1,datum)
    assert naive_mem.next_id == 2
    assert len(naive_mem.test_log)==1

  def test_save_log(self,naive_mem):
    naive_mem.save_log("test_sample")

@pytest.fixture(scope="class")
def postgres_mem():
  mem = PostgresMemory("dummy_pg_path")
  yield mem

class Test_PostgresMemory:
  def test_init(self):
    mem = PostgresMemory("dummy_pg_path")
    assert mem.last_id ==1
    assert len(mem.test_log_local)==0
    assert len(mem.test_log_synced)==0

  def test_log(self,postgres_mem,state,tester_data,pulseC,sweepC,datum):
    postgres_mem.log(Adaptations.NOCHANGE,HighLevelActions.READ,
        state,state,
        pulseC,sweepC,tester_data,1,datum)
    assert len(postgres_mem.test_log_local)==1

  def test_sync(self,postgres_mem):
    assert len(postgres_mem.test_log_local)==1
    assert len(postgres_mem.test_log_synced)==0
    postgres_mem.sync(5)
    assert len(postgres_mem.test_log_local)==0
    assert len(postgres_mem.test_log_synced)==1

  def test_save_log(self,postgres_mem):
    postgres_mem.save_log("test_sample")

