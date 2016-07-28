class NaivePlanner(object):
    """
    Returns the next (very high level) action based on the current state.
    Might want to make some more decisions here later, like selecting strength,
    but that could also be done in executor...
    """
    def __init__(self):
        pass

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
