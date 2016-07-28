from datetime import datetime
from .abstractions import *
from .helpers import mytimestamp

class NaiveTester(object):

    def __init__(self, state_estimator, planner, executor,notificator):
        self.next_id =1
        self.curstate = None
        self.test_log =[]

        self.estimator=state_estimator
        self.planner = planner
        self.executor = executor
        self.notificator = notificator

    def log(self,action,startState,endState):
        newlog = Log(id=self.next_id,startState=startState,aciton=action,endState=endState,timestamp=datetime.now())
        self.test_log.append(newlog)
        self.next_id+=1

    def save_log(self,CURRENT_SAMPLE):
        import pickle
        with open("{}_{}_autorun.pickle".format(mytimestamp(),CURRENT_SAMPLE),"wb") as f:
            pickle.dumps(self.log,f,pickle.protocol=HIGHEST_PROTOCOL)


    def run(self,CURRENT_SAMPLE):
        self.curstate=self.planner.estimate_state(None)
        print("StartState",self.curstate)
        next_action= self.planner.get_action(self.curstate)
        print("Action",next_action)
        while next_action is not None:
            new_datum = self.executor.execute(next_action, CURRENT_SAMPLE)
            print("Datum",new_datum)
            new_state = self.estimator.estimate_state(datum)
            self.log(next_action,self.curstate,new_state)
            self.curstate=new_state
            print("NewState",self.curstate)
            next_action= self.get_action(self.curstate)
            print("Action",next_action)
        self.save_log(CURRENT_SAMPLE)
        self.notificator.done()
