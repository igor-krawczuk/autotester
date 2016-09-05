from .abstractions import *
class NaivePlanner(object):
    """
    Returns the next (very high level) action based on the current state.
    Might want to make some more decisions here later, like selecting strength,
    but that could also be done in executor...
    """
    def __init__(self):
        pass

    def _get_pulse_adaptation(state):
        if state.actionsSinceStateChange >1:
            if state.LRS:
                return Adaptations.RESET_PV_INC
            elif state.HRS:
                return Adaptations.SET_PV_INC
        else:
            return Adaptations.NOCHANGE

    def _get_sweep_adaptation(state):
        if state.actionsSinceStateChange >1:
            if state.LRS:
                return Adaptations.RESET_V_INC
            elif state.HRS:
                return Adaptations.SET_V_INC
        else:
            return Adaptations.NOCHANGE

    def get_adaptation(self,last_action,state):
        if last_action in (HighLevelActions.RESET_PULSE, HighLevelActions.SET_PULSE):
            return _get_pulse_adaptation(state)
        elif last_action in (HighLevelActions.RESET_SWEEP,HighLevelActions.SET_SWEEP):
            return _get_pulse_adaptation(state)

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
