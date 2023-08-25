from ..types import SequenceModuleType, PreparationType
from . import SequenceModule

class PreparationModule(SequenceModule):
    def __init__(self, preparationType:PreparationType, units=None):
        SequenceModule.__init__(self, moduleType=SequenceModuleType.PREPARATION, units=units) 
        self.preparationType = preparationType
    def __str__(self):
        return SequenceModule.__str__(self) + " || Preparation Type: " + self.preparationType.name
