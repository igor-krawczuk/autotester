import dill
from .abstractions import *
import dataset
from collections import deque
from .helpers import mytimestamp

class DillSave(object):
  """
  Mixin class providing boilerplate for saving to dill
  """
  def dill_save(self,obj,name):
    with open(name,"wb") as f:
      dill.dump(obj,f)

class NaiveMemory(DillSave):
    """
    simplest possible storage enginem simply takes the communicator classes and appends them in a list which gets dilld
    """
    def __init__(self):
        self.next_id =1
        self.test_log =[]
    def curState(self):
        if len(self.test_log)>0:
            return self.test_log[-1].endState
        else:
            return None

    def lastAdaptation(self):
        if len(self.test_log)>0:
            return self.test_log[-1].adaptation
        else:
            return None

    def lastAction(self):
        if len(self.test_log)>0:
            return self.test_log[-1].action
        else:
            return None

    def lastState(self):
        if len(self.test_log)>0:
            return self.test_log[-1].startState
        else:
            return None

    def log(self,adaptation,action,startState,endState,pulseControl,sweepControl, testerData,run_id,datum):
        newlog = Log(id=self.next_id,adaptation=adaptation,startState=startState,action=action,endState=endState,pulseControl=pulseControl,sweepControl=sweepControl,testerData=testerData,run_id=run_id,datum=datum)
        self.test_log.append(newlog)
        self.next_id+=1

    def save_log(self,CURRENT_SAMPLE):
      temp_log = [l.to_dicts() for l in self.test_log]
      self.dill_save(temp_log,"{}_{}_autorun.dill".format(mytimestamp(),CURRENT_SAMPLE))

class PostgresMemory(DillSave):
    """
    Like NaiveMemory, but stays in sync with postgres remote
    """
    def __init__(self, pg_path, sync_every=10):
        self.db = dataset.connect(pg_path)
        self.last_id =self.db["run"].find_one(order_by=["-id"],_limit=1).get(["id"])
        if self.last_id is None:
          self.last_id=0

        self.sync_every=sync_every
        self.since_last_sync=0

        self.test_log_local =deque()
        self.test_log_synced=[]

    def curState(self):
        if len(self.test_log)>0:
            return self.test_log[-1].endState
        else:
            return None

    def lastAdaptation(self):
        if len(self.test_log)>0:
            return self.test_log[-1].adaptation
        else:
            return None

    def lastAction(self):
        if len(self.test_log)>0:
            return self.test_log[-1].action
        else:
            return None

    def lastState(self):
        if len(self.test_log)>0:
            return self.test_log[-1].startState
        else:
            return None

    def log(self,adaptation,action,startState,endState,pulseControl,sweepControl,testerData,run_id,datum):
        self.last_id+=1
        newlog = Log(id=self.last_id,adaptation=adaptation,startState=startState,action=action,endState=endState,pulseControl=pulseControl,sweepControl=sweepControl,testerData=testerData,run_id=run_id,datum=datum)
        self.test_log_local.append(newlog)
        self.since_last_sync+=1
        if self.since_last_sync>=self.sync_every:
            self.sync(self.sync_every)

    def sync(self,chunk_size):
        while len(self.test_log_local)>0:
            temp_log = self.test_log_local.popleft()
            # TODO figure out how to do this in batches using chunk_size

            log_dict=temp_log.to_dicts()
            #### TODO HACK just so we save the sample information now
            if hasattr(self,"CURRENT_SAMPLE"):
              log_dict["sample"]={"id":self.CURRENT_SAMPLE}
            self.last_id=self.db["log"].insert(log_dict["log"],ensure=True)
            for k,v in log_dict.items(): # serialize the log + all members into a dict of dicts, every member gets their own table, and internally the same
                if k!="log":
                  self.db[k].insert(v,ensure=True)

            self.test_log_synced.append(temp_log)
        self.since_last_sync=0

    def save_log(self,CURRENT_SAMPLE):
      temp_log = [l.to_dicts() for l in self.test_log_local]
      local_name="{}_{}_autorun_unsynced.dill".format(mytimestamp(),CURRENT_SAMPLE)
      self.dill_save(temp_log,local_name)
      temp_log = [l.to_dicts() for l in self.test_log_synced]
      sync_name= "{}_{}_autorun_synced.dill".format(mytimestamp(),CURRENT_SAMPLE)
      self.dill_save(temp_log,sync_name)
      self.sync(self.sync_every)

    def save_log_raw(self,CURRENT_SAMPLE):
      temp_log = self.test_log_local
      local_name="{}_{}_autorun_unsynced.dill".format(mytimestamp(),CURRENT_SAMPLE)
      self.dill_save(temp_log,local_name)
      temp_log = self.test_log_synced
      sync_name= "{}_{}_autorun_synced.dill".format(mytimestamp(),CURRENT_SAMPLE)
      self.dill_save(temp_log,sync_name)
