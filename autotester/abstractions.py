from collections import namedtuple
from enum import Enum

class controlState(object):
    def vars(self):
        return self.__slots__

    def __getitem__(self,arg):
        if not arg in self.__slots__:
            raise ValueError("No such variable in "+self.__class__)
        else:
            return getattr(self,arg)

    def adapt(self,arg,factor):
        if not arg in self.__slots__:
            raise ValueError("No such variable in "+self.__class__)
        else:
            temp= getattr(self,arg)
            temp +=factor
            setattr(self,arg,temp)

class sweepControl(controlState):
    __slots__= ["setV","setGateV","resetV","resetGateV"]

    def __init__(self, setV,setGateV,resetV,resetGateV,
            ground_channel=3,inp_channel=101,gate_channel=4,steps=100):
        self.setV = setV
        self.setGateV = setGateV
        self.resetV = resetV
        self.resetGateV = resetGateV

        self.steps

        self.ground_channel = ground_channel
        self.gate_channel = gate_channel
        self.inp_channel = inp_channel

    def getNewSet(self):
        return get_Vsweep(0, self.setV, self.steps, compliance=300e-6,
               measure_range=MeasureRanges_I.full_auto,gate_voltage=self.setGateV, ground=self.ground_channel)[0]
    def getNewReset(self):
        return get_Vsweep(0, self.resetV, self.steps, compliance=300e-6,
               measure_range=MeasureRanges_I.full_auto,gate_voltage=self.resetGateV, ground=self.ground_channel)[0]

class pulseControl(controlState):
    __slots__= ["setV","setGateV","resetV","resetGateV","width","slope"]

    def __init__(self, setV,setGateV,resetV,resetGateV,width,slope,
            ground_channel=3,inp_channel=101,gate_channel=4):
        self.setV = setV
        self.setGateV = setGateV
        self.resetV = resetV
        self.resetGateV = resetGateV
        self.width = width
        self.slope = slope

        self.ground_channel = ground_channel
        self.gate_channel = gate_channel
        self.inp_channel = inp_channel

    def getNewSet(self, oldSetup):
        return get_pulse(0,self.setV,self.width,1,
                self.slope,self.slope,self.setGateV,
                self.ground_channel.inp_channel,self.gate_channel)[0]

    def getNewReset(self, oldSetup):
        return get_pulse(0,self.resetV,self.width,1,
                self.slope,self.slope,self.resetGateV,
                self.ground_channel.inp_channel,self.gate_channel)[0]


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

class Adaptations(Enum):
    """
        Used to communicate a change in control variables from planner to exectuor.
        The exact amplitude of alteration is determined by the executor.
        Later we might add additional fuzzy levels (e.g. strong increase)
        or communicate a desired value. The exact change we can calculate in a separate delegate, IF we need it.
    """
    NOCHANGE = 0

    SET_V_INC = 1
    SET_V_DEC = 2

    RESET_V_INC = 3
    RESET_V_DEC = 4

    SET_PV_INC = 5
    SET_PV_DEC = 6

    RESET_PV_INC = 6
    RESET_PV_DEC = 7

class State( namedtuple("__State",
    ["LRS","HRS",
        "deep","formed",
        "annealed","burnedThrough",
        "burnedOut","untouched",
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

