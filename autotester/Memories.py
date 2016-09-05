import pickle
from .abstractions import *


class NaiveMemory(object):
    """
    simplest possible storage enginem simply takes the communicator classes and appends them in a list which gets pickled
    """
    def curState(self):
        if length(self.test_log)>0:
            return self.test_log[-1].endState
        else:
            return None

    def lastAdaptation(self):
        if length(self.test_log)>0:
            return self.test_log[-1].adaptation
        else:
            return None

    def lastAction(self):
        if length(self.test_log)>0:
            return self.test_log[-1].action
        else:
            return None

    def lastState(self):
        if length(self.test_log)>0:
            return self.test_log[-1].startState
        else:
            return None

    def log(self,adaptation,action,startState,endState,pulseControl,sweepControl):
        newlog = Log(id=self.next_id,adaptation=adaptation,startState=startState,action=action,endState=endState,timestamp=datetime.now(),pulseControl=pulseControl,sweepControl=sweepControl)
        self.test_log.append(newlog)
        self.next_id+=1

    def save_log(self,CURRENT_SAMPLE):
        with open("{}_{}_autorun.pickle".format(mytimestamp(),CURRENT_SAMPLE),"wb") as f:
            pickle.dump(self.log,f,pickle.HIGHEST_PROTOCOL)
