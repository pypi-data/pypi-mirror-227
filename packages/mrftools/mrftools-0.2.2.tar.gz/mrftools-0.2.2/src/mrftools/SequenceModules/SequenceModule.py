from ..types import SequenceModuleType, Units, SequenceUnits
from . import RegisteredSequenceModules

class SequenceModule:
    def __init__(self, moduleType:SequenceModuleType, units=None):
        self.moduleType = moduleType
        if(units != None):
            self.units = units
        else:
            self.units = SequenceUnits(Units.SECONDS, Units.DEGREES)

    def __str__(self):
        return "Module Type: " + self.moduleType.name
    
    @staticmethod
    def FromJson(jsonInput, units):
        moduleClass = RegisteredSequenceModules[jsonInput.get("type")]
        module = moduleClass.FromJson(jsonInput)
        module.units = units
        return module
