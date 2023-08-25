from ..types import SequenceModuleType, RecoveryType, RFType
from . import SequenceModule

class RecoveryModule(SequenceModule):
    def __init__(self, recoveryType:RecoveryType, units=None):
        SequenceModule.__init__(self, moduleType=SequenceModuleType.RECOVERY, units=units) 
        self.recoveryType = recoveryType
    def __str__(self):
        return SequenceModule.__str__(self) + " || Recovery Type: " + self.recoveryType.name
