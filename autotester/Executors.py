from .abstractions import *
from .helpers import mytimestamp
from .analysis_helpers import (add_energy,find_set_V,get_R,add_resistance)
from collections import namedtuple

class Executor(object):
    def adapt(self,adaptation):
        raise NotImplemented("All Exectutors must implement a function adapt which takes an adaptation and is used to change the Control Parameters")

    def execute(self,action):
        raise NotImplemented("All Exectutors must implement a function execute which takes an action and implements the tester specific details")

class NaiveExecutor(Executor):
    """
    Takes a high level action and executes the implementation based on its stored skills
    """

    def __init__(self,tester, initSweepControl,initPulseControl,precon_closures ):
        self.formV=None
        self.timesAnnealed=0
        self.CURRENT_SAMPLE=None

        self.read_setup = initSweepControl.getNewRead()
        self.precon_closures=precon_closures

        self.tester = tester

        self.sweepControl = initSweepControl
        self.pulseControl = initPulseControl
        self.stepSize = 0.1

        self.implementations={HighLevelActions.FORM: initSweepControl.getNewForm(),
                    HighLevelActions.RESET_SWEEP: initSweepControl.getNewReset(),
                    HighLevelActions.SET_SWEEP: initSweepControl.getNewSet(),
                    HighLevelActions.RESET_PULSE: initPulseControl.getNewReset(),
                    HighLevelActions.SET_PULSE: initPulseControl.getNewSet(),
                    HighLevelActions.READ: initSweepControl.getNewRead(),
                    HighLevelActions.FORM: initSweepControl.getNewForm(),
                    }

    def reset(self):
        self.timesAnnealed=0
    def adapt(self, adaptation):
        if adaptation==Adaptations.NOCHANGE:
            pass
        elif adaptation == Adaptations.RESET_PV_INC:
            self.pulseControl.adapt("resetV",-1.0*self.stepSize)
            self.implementations[HighLevelActions.RESET_PULSE]["test_setup"]=self.pulseControl.getNewReset()
        elif adaptation == Adaptations.SET_PV_INC:
            self.pulseControl.adapt("setV",self.stepSize)
            self.implementations[HighLevelActions.SET_PULSE]["test_setup"]=self.pulseControl.getNewSet()
        elif adaptation == Adaptations.SET_V_INC:
            self.sweepControl.adapt("setV",self.stepSize)
            self.implementations[HighLevelActions.SET_SWEEP]["test_setup"]=self.sweepControl.getNewSet()
        elif adaptation == Adaptations.RESET_V_INC:
            self.sweepControl.adapt("resetV",-1.0*self.stepSize)
            self.implementations[HighLevelActions.RESET_SWEEP]["test_setup"]=self.sweepControl.getNewReset()
        elif adaptation == Adaptations.RESET_PV_DEC:
            self.pulseControl.adapt("resetV",self.stepSize)
            self.implementations[HighLevelActions.RESET_PULSE]["test_setup"]=self.pulseControl.getNewReset()
        elif adaptation == Adaptations.SET_PV_DEC:
            self.pulseControl.adapt("setV",-1.0*self.stepSize)
            self.implementations[HighLevelActions.SET_PULSE]["test_setup"]=self.pulseControl.getNewSet()
        elif adaptation == Adaptations.SET_V_DEC:
            self.sweepControl.adapt("setV",-1.0*self.stepSize)
            self.implementations[HighLevelActions.SET_SWEEP]["test_setup"]=self.sweepControl.getNewSet()
        elif adaptation == Adaptations.RESET_V_DEC:
            self.sweepControl.adapt("resetV",self.stepSize)
            self.implementations[HighLevelActions.RESET_SWEEP]["test_setup"]=self.sweepControl.getNewReset()
        else:
            raise ValueError("Please pass a valid value from the HighLevelActions Enum")


    def execute(self,action):
        was_pulse=None
        if action == HighLevelActions.RE_ANNEAL:
            self.timesAnnealed=0
            action = HighLevelActions.RESET_SWEEP

        impl = self.implementations[action]
        V=None
        gateV=None
        if action in (HighLevelActions.RESET_SWEEP,HighLevelActions.SET_SWEEP,HighLevelActions.FORM,HighLevelActions.READ):
          V=self.sweepControl.getV(action)
          gateV=self.sweepControl.getGateV(action)
        else:
          V=self.pulseControl.getV(action)
          gateV=self.pulseControl.getGateV(action)

        precon_closure=self.precon_closures.get(action)
        if precon_closure is not None:
            precon_closure()

        out =None
        if action in (HighLevelActions.SET_PULSE,HighLevelActions.RESET_PULSE):
            self.tester.run_test(impl,force_wait=True,force_new_setup=True)
            was_pulse=True
        else:
            ret,out =self.tester.run_test(impl,force_wait=True,force_new_setup=True,auto_read=True)
            out,series_dict,raw =out
            out=add_energy(out)
            was_pulse=False
            if action == HighLevelActions.FORM:
                self.formV = find_set_V(out)
            if action in (HighLevelActions.SET_SWEEP,HighLevelActions.RESET_SWEEP):
                self.timesAnnealed+=1
            out.to_csv("{}_{}_{}.csv".format(mytimestamp(),self.CURRENT_SAMPLE,action.name))
        R_after=self.checkR()
        newdatum = Datum(R=R_after,V=V,gateV=gateV,timesAnnealed=self.timesAnnealed,formV=self.formV,wasPulse=was_pulse)
        newtesterData = testerData(action=action,dataframe=out)
        return newdatum,newtesterData


    def checkR(self ):
        read_precon = self.precon_closures.get(HighLevelActions.READ)
        if read_precon is not None:
          read_precon()
        ret,out =self.tester.run_test(self.read_setup,force_wait=True,force_new_setup=True,auto_read=True)
        out,series_dict,raw =out
        out=add_energy(out)
        out.to_csv("{}_{}_{}.csv".format(mytimestamp(),self.CURRENT_SAMPLE,"read"))
        R= get_R(out)
        return R
