from .abstractions import *
from .helpers import mytimestamp
from .analysis_helpers import (add_energy,find_set_V,get_R,add_resistance)
class NaiveExecutor(object):
    """
    Takes a high level action and executes the implementation based on its stored skills
    """

    def __init__(self,tester, form, reset_sweep,set_sweep,set_pulse,reset_pulse,read_setup, read_precon):
        self.formV=None
        self.timesAnnealed=0

        self.read_setup = read_setup
        self.read_precon_closure = read_precon

        self.tester = tester
        self.implementations={HighLevelActions.FORM:form,
                    HighLevelActions.RESET_SWEEP:reset_sweep,
                    HighLevelActions.SET_SWEEP:set_sweep,
                    HighLevelActions.RESET_PULSE:reset_pulse,
                    HighLevelActions.SET_PULSE:set_pulse
                    }

    def execute(self,action,CURRENT_SAMPLE):
        was_pulse=None

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
            out.to_csv("{}_{}_{}.csv".format(mytimestamp(),CURRENT_SAMPLE,action.name))
        R_after=self.checkR(CURRENT_SAMPLE)
        newdatum = Datum(R=R_after,V=V,gateV=gateV,timesAnnealed=self.timesAnnealed,formV=self.formV,wasPulse=was_pulse)
        return newdatum

    def checkR(self, CURRENT_SAMPLE):
        self.read_precon_closure()
        ret,out =self.tester.run_test(self.read_setup,force_wait=True,force_new_setup=True,auto_read=True)
        out,series_dict,raw =out
        out=add_energy(out)
        out.to_csv("{}_{}_{}.csv".format(mytimestamp(),CURRENT_SAMPLE,"read"))
        R= get_R(out)
        return R
