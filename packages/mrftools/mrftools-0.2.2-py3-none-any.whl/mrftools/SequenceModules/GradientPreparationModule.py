from ..types import PreparationType, GradientType
from . import PreparationModule

class GradientPreparationModule(PreparationModule):
    def __init__(self, gradientType:GradientType, units=None):
        PreparationModule.__init__(self, preparationType=PreparationType.GRADIENT, units=units) 
        self.gradientType = gradientType
    def __str__(self):
        return PreparationModule.__str__(self) + " || Gradient Type: " + self.gradientType.name
    