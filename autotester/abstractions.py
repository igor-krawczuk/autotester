from collections import namedtuple
from datetime import datetime
from enum import Enum
from agilentpyvisa.reram_helpers_B1500.get_setups import get_pulse,get_Vsweep
from agilentpyvisa.B1500.enums import MeasureRanges_I,MeasureRanges_V,MeasureModes,MeasureSides
"""
Enums
"""
class HighLevelActions(Enum):
    FORM =0

    RESET_SWEEP=1
    SET_SWEEP=2

    RESET_PULSE=3
    SET_PULSE=4
    READ = 5  # trigger a readout of the device state

    RE_ANNEAL = 6 # trigger a new anneal cycle as defined in exectutor

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

"""
Muetable States
"""


class controlState(object):
    def __init__(self,tester):
        self.last_change=datetime.now()
        self.tester=tester
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
        self.last_change=datetime.now()

    def to_dict(self,log_id=None):
        d=dict()
        for v in self.__slots__:
            if v=="tester":
              continue
            d[v]=getattr(self,v)
        if log_id is not None:
            d["log_id"]=log_id
        d["last_change"]=self.last_change
        return d
    def getV(self,action):
      raise NotImplementedError("implement a sensinple switch on the given action to access the Voltage")
    def getGateV(self,action):
      raise NotImplementedError("implement a sensinple switch on the given action to access the gateVoltage")

class sweepControl(controlState):
    __slots__= ["setBase","setV","setGateV",
            "resetBase","resetV","resetGateV",
            "readBase","readV","readGateV",
            "formBase","formV","formGateV",
            "steps","ground_channel","inp_channel","tester"
            ]

    # TODO XXX having this many fields is smelly, as is having the read defaults. refactor this
    # probably define a new intermediate state for individual sweeps, and just keep that in a action dict
    def __init__(self,tester, setV,setGateV,resetV,resetGateV,
            setBase=0,resetBase=0,
            formBase=0,formV=3.0,formGateV=1.9,
            readBase=200e-6,readV=250e-6,readGateV=1.9,
            ground_channel=3,inp_channel=101,gate_channel=4,steps=100):

        self.setBase = setBase
        self.setV = setV
        self.setGateV = setGateV

        self.resetBase = resetBase
        self.resetV = resetV
        self.resetGateV = resetGateV


        self.readBase = readBase
        self.readV = readV
        self.readGateV = readGateV

        self.formBase = formBase
        self.formV = formV
        self.formGateV = formGateV

        self.steps=steps

        self.ground_channel = ground_channel
        self.gate_channel = gate_channel
        self.inp_channel = inp_channel
        super().__init__(tester)

    def getV(self,action):
      if action==HighLevelActions.RESET_SWEEP:
        return self.resetV
      elif action==HighLevelActions.SET_SWEEP:
        return self.setV
      elif action==HighLevelActions.FORM:
        return self.formV
      elif action==HighLevelActions.READ:
        return self.readV
      else:
        raise ValueError("No Voltage defined for this action")

    def getGateV(self,action):
      if action==HighLevelActions.RESET_SWEEP:
        return self.resetGateV
      elif action==HighLevelActions.SET_SWEEP:
        return self.setGateV
      elif action==HighLevelActions.FORM:
        return self.formGateV
      elif action==HighLevelActions.READ:
        return self.readGateV
      else:
        raise ValueError("No gate voltage defined for this action")

    def getNewSet(self):
        return get_Vsweep(self.setBase, self.setV, self.steps, compliance=5e-3,
                measure_range=MeasureRanges_I.uA100_limited,
                gate_voltage=self.setGateV, ground=self.ground_channel,b15=self.tester)[0]
    def getNewReset(self):
        return get_Vsweep(self.resetBase, self.resetV, self.steps, compliance=5e-3,
                measure_range=MeasureRanges_I.uA100_limited,gate_voltage=self.resetGateV,
                ground=self.ground_channel,b15=self.tester)[0]
    def getNewForm(self):
        return get_Vsweep(self.formBase,self.formV,51,compliance=5e-3,
                measure_range=MeasureRanges_I.uA100_limited,
                gate_voltage=self.formGateV, ground=self.ground_channel,b15=self.tester)[0]

    def getNewRead(self):
        return get_Vsweep(self.readBase,self.readV,51,compliance=5e-3,
                measure_range=MeasureRanges_I.uA100_limited,gate_voltage=self.readGateV, ground=self.ground_channel,b15=self.tester)[0]

class pulseControl(controlState):
    __slots__= ["setV","setGateV","resetV","resetGateV","width","slope",
            "ground_channel","inp_channel","tester"
            ]

    def __init__(self,tester, setV,setGateV,resetV,resetGateV,width,slope,
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
        super().__init__(tester)

    def getV(self,action):
      if action==HighLevelActions.RESET_PULSE:
        return self.resetV
      elif action==HighLevelActions.SET_PULSE:
        return self.setV
      else:
        raise ValueError("No Voltage defined for this action")

    def getGateV(self,action):
      if action==HighLevelActions.RESET_PULSE:
        return self.resetGateV
      elif action==HighLevelActions.SET_PULSE:
        return self.setGateV
      else:
        raise ValueError("No gate Voltage defined for this action")

    def getNewSet(self ):
        return get_pulse(0,self.setV,self.width,1,
                self.slope,self.slope,self.setGateV,
                ground=self.ground_channel,channel=self.inp_channel,gate=self.gate_channel,b15=self.tester)[0]

    def getNewReset(self ):
        return get_pulse(0,self.resetV,self.width,1,
                self.slope,self.slope,self.resetGateV,
                ground=self.ground_channel,channel=self.inp_channel,gate=self.gate_channel,b15=self.tester)[0]


class Log(namedtuple("_Log",["local_id","adaptation","action","startState","endState","timestamp","pulseControl","sweepControl","testerData","run_id","datum"])):

    def __new__(cls,local_id,adaptation,action,startState,endState,pulseControl,sweepControl,run_id,datum,testerData=None):
       timestamp=datetime.now()
       return super(Log,cls).__new__(cls,local_id,adaptation,action,startState,endState,timestamp,pulseControl,sweepControl,testerData,run_id,datum)

    def to_dicts(self):
       d={}
       log={}
       log["local_id"]=self.local_id
       log["run_id"]=self.run_id
       log["adaptation"]=self.adaptation.name
       log["action"]=self.action.name
       log["timestamp"]=self.timestamp

       d["log"]=log

       d["datum"]=self.datum.to_dict()
       d["pulseControl"]=self.pulseControl.to_dict(self.local_id)
       d["sweepControl"]=self.sweepControl.to_dict(self.local_id)

       d["startState"]=self.startState.to_dict(self.local_id)
       d["testerData"]=self.testerData.to_dict(self.local_id)
       d["endState"]=self.endState.to_dict(self.local_id)

       return d

class testerData(object):
    __slots__ = ["action","frame","timestamp"]
    def __init__(self,action,dataframe=None):
        self.frame = dataframe
        self.timestamp = datetime.now()
        self.action=action

    def to_dict(self, log_id=None):
        d=dict(timestamp=self.timestamp,action=self.action.name,log_id=log_id)
        if self.frame is not None:
            d["frame"]=frame=self.frame.to_json()
        return d

"""
immutable States
"""
class State( namedtuple("__State",
    ["LRS","HRS",
        "deep","formed",
        "annealed","burnedThrough",
        "burnedOut","untouched",
        "actionsSinceStateChange","timestamp"])):
    def __new__(cls,LRS=None,HRS=None,deep=None,formed=None,annealed=None,burnedThrough=None,burnedOut=None,untouched=None,actionsSinceStateChange=None):
           assert not(LRS and HRS)
           assert not (untouched and(LRS or HRS or formed or annealed))
           return super(State,cls).__new__(cls,LRS,HRS,deep,formed,annealed,burnedThrough,burnedOut,untouched,actionsSinceStateChange,timestamp=datetime.now())

    def to_dict(self,log_id=None):
       d=dict(self._asdict())
       d["log_id"]=log_id
       return d

    @staticmethod
    def get_pristine():
        return State(untouched=True,LRS=False,HRS=False,deep=False,
                    formed=False,annealed=False,burnedThrough=False,
                    burnedOut=False,actionsSinceStateChange=0)
class Datum(namedtuple("_Datum",["R",
    "V",
    "gateV",
    "timesAnnealed",
    "formV",
    "wasPulse",
    "timestamp",
    #"meanMaxHistResetAnneal,
    #"meanMaxHistReSetAnneal,
    #"meanSetVAnneal,
    #meanMaxCurResetAnneal,
    ])):
    def __new__(cls,R,
        V,
        gateV,
        timesAnnealed,
        formV,
        wasPulse,
        #meanMaxHistResetAnneal,
        #meanMaxHistReSetAnneal,
        #meanSetVAnneal,
        #meanMaxCurResetAnneal)
        timestamp=datetime.now()):
            return super(Datum,cls).__new__(cls,R,
                V,
                gateV,
                timesAnnealed,
                formV,
                wasPulse,
                timestamp,
                #meanMaxHistResetAnneal,
                #meanMaxHistReSetAnneal,
                #meanSetVAnneal,
                #meanMaxCurResetAnneal
                )
    def to_dict(self,log_id=None):
        d=dict(self._asdict())
        d["log_id"]=log_id
        return d

