from .abstractions import *
from .helpers import mytimestamp
from .analysis_helpers import (add_energy,find_set_V,get_R,add_resistance)
from collections import namedtuple

class NaiveExecutor(object):
    """
    Takes a high level action and executes the implementation based on its stored skills
    """

    def __init__(self,tester, form, reset_sweep,set_sweep,set_pulse,reset_pulse,read_setup, read_precon):
        self.formV=None
        self.timesAnnealed=0
        self.CURRENT_SAMPLE=None

        self.read_setup = read_setup
        self.read_precon_closure = read_precon

        self.tester = tester

        self.sweepControl = sweepControl()
        self.pulseControl = pulseControl()
        self.adaptation = 0.1

        self.implementations={HighLevelActions.FORM:form,
                    HighLevelActions.RESET_SWEEP:reset_sweep,
                    HighLevelActions.SET_SWEEP:set_sweep,
                    HighLevelActions.RESET_PULSE:reset_pulse,
                    HighLevelActions.SET_PULSE:set_pulse
                    }

    def adapt(self, adaptation):
        if adaptation==Adaptations.NOCHANGE:
            pass
        elif adaptation == Adaptations.RESET_PV_INC:
            self.pulseControl.adapt("resetV",adaptation)
            self.implementations[HighLevelActions.RESET_PULSE]["test_setup"]=self.pulseControl.getNewReset()
        elif adaptation == Adaptations.SET_PV_INC:
            self.pulseControl.adapt("setV",adaptation)
            self.implementations[HighLevelActions.SET_PULSE]["test_setup"]=self.pulseControl.getNewSet()
        elif adaptation == Adaptations.SET_V_INC:
            self.sweepControl.adapt("setV",adaptation)
            self.implementations[HighLevelActions.SET_SWEEP]["test_setup"]=self.sweepControl.getNewSet()
        elif adaptation == Adaptations.RESET_V_INC:
            self.sweepControl.adapt("resetV",-1.0*adaptation)
            self.implementations[HighLevelActions.RESET_SWEEP]["test_setup"]=self.sweepControl.getNewReset()


    def execute(self,adaptation,action):
        was_pulse=None

        self.adapt(adaptation)

        impl = self.implementations[action]["test_setup"]
        V=self.implementations[action]["V"]
        gateV=self.implementations[action]["gateV"]
        precon_closure=self.implementations[action].get("precondition_closure")
        if precon_closure is not None:
            precon_closure()

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
        return newdatum

    def checkR(self ):
        self.read_precon_closure()
        ret,out =self.tester.run_test(self.read_setup,force_wait=True,force_new_setup=True,auto_read=True)
        out,series_dict,raw =out
        out=add_energy(out)
        out.to_csv("{}_{}_{}.csv".format(mytimestamp(),self.CURRENT_SAMPLE,"read"))
        R= get_R(out)
        return R
