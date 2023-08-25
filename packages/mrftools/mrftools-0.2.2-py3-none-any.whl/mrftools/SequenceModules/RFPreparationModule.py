from ..types import PreparationType, RFType
from . import PreparationModule

class RFPreparationModule(PreparationModule):
    def __init__(self, rfType:RFType, units=None):
        PreparationModule.__init__(self, preparationType=PreparationType.RF, units=units) 
        self.rfType = rfType
    def __str__(self):
        return PreparationModule.__str__(self) + " || RF Type: " + self.rfType.name
    