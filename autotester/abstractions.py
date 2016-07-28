from collections import namedtuple
from enum import Enum


Log = namedtuple("Log",["id","startState","action","endState","timestamp"])

Datum=namedtuple("Datum",["R",
                  "V",
                  "gateV",
                    "timesAnnealed",
                    "formV",
                    "wasPulse",
                    #"meanMaxHistResetAnneal,
                    #"meanMaxHistReSetAnneal,
                    #"meanSetVAnneal,
                    #meanMaxCurResetAnneal,
                  ])
    

class HighLevelActions(Enum):
    FORM =0
    RESET_SWEEP=1
    SET_SWEEP=2
    RESET_PULSE=3
    SET_PULSE=4
    READ = 5

class State( namedtuple("__State",["LRS","HRS","deep","formed","annealed","burnedThrough","burnedOut","untouched",
                    "actionsSinceStateChange"])):
        def __new__(cls,LRS=None,HRS=None,deep=None,formed=None,annealed=None,burnedThrough=None,burnedOut=None,untouched=None,actionsSinceStateChange=None):
           assert not(LRS and HRS) 
           assert not (untouched and(LRS or HRS or formed or annealed))
           return super(State,cls).__new__(cls,LRS,HRS,deep,formed,annealed,burnedThrough,burnedOut,untouched,actionsSinceStateChange)

        @staticmethod
        def get_pristine():
            return State(untouched=True,LRS=False,HRS=False,deep=False,
                formed=False,annealed=False,burnedThrough=False,
                burnedOut=False,actionsSinceStateChange=0)

