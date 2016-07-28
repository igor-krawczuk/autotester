from .abstractions import *
from .helpers import mytimestamp
class NaiveExecutor(object):
    """
    Takes a high level action and executes the implementation based on its stored skills
    """

    def __init__(self,tester, form, reset_sweep,set_sweep,set_pulse,reset_pulse,read_setup):
        self.formV=None
        self.timesAnnealed=0

        self.read_setup = read_setup

        self.tester = tester
        self.implementations={HighLevelActions.FORM:form,
                    HighLevelActions.RESET_SWEEP:reset_sweep,
                    HighLevelActions.SET_SWEEP:set_sweep,
                    HighLevelActions.RESET_PULSE:set_pulse,
                    HighLevelActions.SET_PULSE:reset_pulse
                    }

    def execute(self,action,CURRENT_SAMPLE):
        was_pulse=None

        impl = self.implementations[action]["test_setup"]
        V=self.implementations[action]["V"]
        gateV=self.implementations[action]["gateV"]

        if action in (HighLevelActions.SET_PULSE,HighLevelActions.RESET_PULSE):
            b15.set_SMUSPGU_selector(SMU_SPGU_port.Module_1_Output_1,SMU_SPGU_state.connect_relay_SPGU)
            self.tester.run_test(impl,force_wait=True,force_new_setup=True)
            was_pulse=True
        else:
            self.tester.set_SMUSPGU_selector(SMU_SPGU_port.Module_1_Output_1,SMU_SPGU_state.connect_relay_SMU)
            ret,out =self.tester.run_test(impl,force_wait=True,force_new_setup=True)
            out,series_dict,raw =out
            out=add_energy(out)
            was_pulse=False
            if action == HighLevelActions.FORM:
                self.formV = find_setV(out)
            if action in (HighLevelActions.SET_SWEEP,HighLevelActions.RESET_SWEEP):
                self.timesAnnealed+=1
            out.to_csv("{}_{}_{}".format(mytimestamp(),CURRENT_SAMPLE,action.name))
        R_after=self.checkR(CURRENT_SAMPLE)
        newdatum = Datum(R=R_after,V=V,gateV=gateV,timesAnnealed=self.timesAnnealed,formV=self.formV,wasPulse=was_pulse)
        return newdatum

    def checkR(self, CURRENT_SAMPLE):
        self.tester.set_SMUSPGU_selector(SMU_SPGU_port.Module_1_Output_1,SMU_SPGU_state.connect_relay_SMU)
        ret,out =self.tester.run_test(self.read_setup,force_wait=True,force_new_setup=True)
        out,series_dict,raw =out
        out=add_energy(out)
        out.to_csv("{}_{}_{}".format(mytimestamp(),CURRENT_SAMPLE,"read"))
        R= get_R(out)
        return R
