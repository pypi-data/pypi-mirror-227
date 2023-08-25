from ..types import ReconstructionModuleIOType, KspaceData, ImageData
from . import ReconstructionModule, Register
import numpy as np


@Register
class ScalingModule(ReconstructionModule):
    def __init__(self, reconstructionParameters, inputType:ReconstructionModuleIOType, outputType:ReconstructionModuleIOType, scalingFactor=1, device=None):
        ReconstructionModule.__init__(self, reconstructionParameters=reconstructionParameters, inputType=inputType, outputType=outputType) 
        self.scalingFactor = scalingFactor
        if(device is None):
            self.device = reconstructionParameters.defaultDevice
        else:
            self.device = device
            
    def __dict__(self):
        moduleDict  = {
            "type": str(self.__class__.__name__),
            "inputType": str(self.inputType.name),
            "outputType": str(self.outputType.name),
            "scalingFactor": self.scalingFactor
        }
        return moduleDict

    def DoScaling(self, inputData, scalingFactor):
        return inputData * scalingFactor

    def ProcessKspaceToKspace(self, inputData):
        return KspaceData(self.DoScaling(inputData, self.scalingFactor))

    def ProcessImageToImage(self, inputData):
        return ImageData(self.DoScaling(inputData, self.scalingFactor))

    @staticmethod
    def FromJson(jsonInput, reconstructionParameters, inputType, outputType):  
        scalingFactor = jsonInput.get("scalingFactor")
        if scalingFactor != None:
            return ScalingModule(reconstructionParameters, inputType, outputType, scalingFactor)
        else:
            print("CoilCombinationModule requires scalingFactor")