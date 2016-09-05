from .abstractions import *

class AbstractPlanner(object):
    """
    Abstract interface for all planners. Mainly to document the interface and for me to plan.
    """
    def get_adaptation(self,last_action,state,*args,**kwargs):
        raise NotImplemented("This functions needs to take at least the last_action and currently estimated state and return either an Adaptation or Adaptation.NOCHANGE")
    def get_action(self,state,*args,**kwargs):
        raise NotImplemented("This functions needs to take at least the currently estimated state and either return a HighLevelActions or None")

class NaiveAdaptivePlanner(AbstractPlanner):
    """
    Returns the next (very high level) action based on the current state.
    Might want to make some more decisions here later, like selecting strength,
    but that could also be done in executor...
    """
    def __init__(self, adaptationTrigger=1):
        self.adaptationTrigger = adaptationTrigger
        # after this many actions without change, we trigger a request to the 
        # executor to increase the amplitude of the current action

    def _get_pulse_adaptation(self,state):
        if state.LRS:
            return Adaptations.RESET_PV_INC
        elif state.HRS:
            return Adaptations.SET_PV_INC

    def _get_sweep_adaptation(self,state):
        if state.LRS:
            return Adaptations.RESET_V_INC
        elif state.HRS:
            return Adaptations.SET_V_INC

    def get_adaptation(self,last_action,state):
        if state.actionsSinceStateChange >self.adaptationTrigger:
            if last_action in (HighLevelActions.RESET_PULSE, HighLevelActions.SET_PULSE):
                return self._get_pulse_adaptation(state)
            elif last_action in (HighLevelActions.RESET_SWEEP,HighLevelActions.SET_SWEEP):
                return self._get_sweep_adaptation(state)
        else:
            return Adaptations.NOCHANGE

    def get_action(self,state):
        if state.burnedOut or state.burnedThrough:
            return None
        elif not state.formed:
            return HighLevelActions.FORM
        elif not state.annealed:
            if state.LRS:
                return HighLevelActions.RESET_SWEEP
            else:
                return HighLevelActions.SET_SWEEP
        elif state.LRS:
            return HighLevelActions.RESET_PULSE
        elif state.HRS:
            return HighLevelActions.SET_PULSE
        # if state.deep: HighLevelActions.STRONG_RESET/SET?

class NaiveFixedPlanner(AbstractPlanner):
    """
    Returns the next (very high level) action based on the current state.
    Does not provide any adaptations
    """
    def __init__(self):
        pass


    def get_adaptation(self,last_action,state):
        return Adaptations.NOCHANGE

    def get_action(self,state):
        if state.burnedOut or state.burnedThrough:
            return None
        elif not state.formed:
            return HighLevelActions.FORM
        elif not state.annealed:
            if state.LRS:
                return HighLevelActions.RESET_SWEEP
            else:
                return HighLevelActions.SET_SWEEP
        elif state.LRS:
            return HighLevelActions.RESET_PULSE
        elif state.HRS:
            return HighLevelActions.SET_PULSE
        # if state.deep: HighLevelActions.STRONG_RESET/SET?
