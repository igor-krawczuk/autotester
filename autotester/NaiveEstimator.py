from .abstractions import State
class NaiveEstimator(object):

    def __init__(self, LRS_THRESHOLD=10e3, HRS_THRESHOLD=20e3, deep_THRESHOLD=5,annealGoal=10,burned_THRESHOLD=15):
        self.LRS_THRESHOLD = LRS_THRESHOLD
        self.HRS_THRESHOLD = HRS_THRESHOLD
        # after this many  failed transitions, we assume we are in a "deep" state
        self.deep_THRESHOLD = deep_THRESHOLD
        # we want to anneal at least this many times, meaning we want to do this many DC sweeps. divide by half for dc cycles
        self.annealGoal = annealGoal

        # after this many failed transitions, we treat it as a burned sample
        self.burned_THRESHOLD = burned_THRESHOLD

        assert self.LRS_THRESHOLD < self.HRS_THRESHOLD
    
    def estimate_state(self,datum,laststate):
        if datum is None:
            return State.get_pristine()

        newstate = laststate

        newstate =newstate._replace(LRS=datum.R<self.LRS_THRESHOLD)
        newstate =newstate._replace(HRS=datum.R>self.LRS_THRESHOLD)
        newstate =newstate._replace(formed=datum.formV is not None)
        newstate =newstate._replace(annealed=datum.timesAnnealed >= self.annealGoal)

        if (newstate.LRS != laststate.LRS) or (newstate.HRS != laststate.HRS):
            sinceChange=0
        else:
            sinceChange=laststate.actionsSinceStateChange+1

        newstate =newstate._replace(actionsSinceStateChange=sinceChange)
        newstate =newstate._replace(deep=newstate.actionsSinceStateChange > self.deep_THRESHOLD)

        newBurnedThrough = newstate.actionsSinceStateChange > self.burned_THRESHOLD and newstate.LRS
        newBurnedOut = newstate.actionsSinceStateChange > self.burned_THRESHOLD and newstate.HRS

        newstate =newstate._replace(burnedThrough = newBurnedThrough,burnedOut= newBurnedOut)
        return newstate
