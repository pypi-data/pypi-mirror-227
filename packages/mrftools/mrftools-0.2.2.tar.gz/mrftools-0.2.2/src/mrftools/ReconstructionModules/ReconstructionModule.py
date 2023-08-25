from ..types import ReconstructionModuleIOType, DataStruct
from . import RegisteredReconstructionModules

class ReconstructionModule:
    def __init__(self, reconstructionParameters, inputType:ReconstructionModuleIOType, outputType: ReconstructionModuleIOType):
        self.reconstructionParameters = reconstructionParameters
        self.inputType = inputType
        self.outputType = outputType

    def __str__(self):
        return "Input: " + self.inputType.name + " | Output: " + self.outputType.name
    
    def Process(self, input:DataStruct):
        if(input.dataType == self.inputType):
            if(self.inputType == ReconstructionModuleIOType.KSPACE and self.outputType == ReconstructionModuleIOType.KSPACE):
                return self.ProcessKspaceToKspace(input.data)
            elif(self.inputType == ReconstructionModuleIOType.KSPACE and self.outputType == ReconstructionModuleIOType.IMAGE):
                return self.ProcessKspaceToImage(input.data)
            elif(self.inputType == ReconstructionModuleIOType.IMAGE and self.outputType == ReconstructionModuleIOType.IMAGE):
                return self.ProcessImageToImage(input.data)
            elif(self.inputType == ReconstructionModuleIOType.IMAGE and self.outputType == ReconstructionModuleIOType.MAP):
                return self.ProcessImageToMap(input.data)
            else:
                return None
        else:
            return None

    def ProcessKspaceToKspace(self, inputData):
        return None
    
    def ProcessKspaceToImage(self, inputData):
        return None
    
    def ProcessImageToImage(self, inputData):
        return None
    
    def ProcessImageToMap(self, inputData):
        return None
    
    @staticmethod
    def FromJson(jsonInput, reconstructionParameters):
        moduleClass = RegisteredReconstructionModules[jsonInput.get("type")]
        inputType = ReconstructionModuleIOType[jsonInput.get("inputType")]
        outputType = ReconstructionModuleIOType[jsonInput.get("outputType")]
        module = moduleClass.FromJson(jsonInput, reconstructionParameters, inputType, outputType)
        return module
