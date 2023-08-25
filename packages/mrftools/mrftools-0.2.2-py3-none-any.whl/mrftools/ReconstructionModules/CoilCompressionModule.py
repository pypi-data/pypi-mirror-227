from ..types import ReconstructionModuleIOType, KspaceData
from . import ReconstructionModule, Register
import torch

def GetTruncationNumberFromDesiredPower(singularValues, desiredSVDPower):
    singularVectorPowers = singularValues/torch.sum(singularValues)
    totalSVDPower=0; numSVDComponents=0
    for singularVectorPower in singularVectorPowers:
        totalSVDPower += singularVectorPower
        numSVDComponents += 1
        if totalSVDPower > desiredSVDPower:
            break
    return numSVDComponents, totalSVDPower

def GetPowerFromDesiredTruncationNumber(singularValues, desiredTruncationNumber):
    singularVectorPowers = singularValues/torch.sum(singularValues)
    totalSVDPower=torch.sum(singularVectorPowers[0:desiredTruncationNumber])
    return totalSVDPower

# rawData = [coil, partition, readout, spiral, spiralTimepoint]
def PerformSVDCoilCompression(rawData, desiredSVDPower=0.99, truncationNumberOverride=-1, device=None):
    print("Calculating SVD Coil Compression")
    input = rawData.moveaxis(-1,0)
    linearizedData = input.swapaxes(0,1).reshape(input.shape[1], -1).t()
    (u,s,v) = torch.linalg.svd(linearizedData, full_matrices=False)
    vt = v.t()
    if truncationNumberOverride == -1:
            (truncationNumber, totalSVDPower) = GetTruncationNumberFromDesiredPower(s, desiredSVDPower)
    else:
        truncationNumber = truncationNumberOverride
        totalSVDPower = GetPowerFromDesiredTruncationNumber(s, truncationNumber)
    truncationMatrix = vt[:,0:truncationNumber]
    print(f"Applying SVD Coil Compression (truncationNumber: {truncationNumber}, svdPower: {totalSVDPower})")
    coilCompressed = torch.matmul(linearizedData,truncationMatrix).t()
    coilCompressedResults= coilCompressed.reshape(truncationNumber, input.shape[0], input.shape[2],input.shape[3],input.shape[4]).swapaxes(0,1).moveaxis(0,-1)
    return coilCompressedResults, truncationNumber, totalSVDPower

@Register
class CoilCompressionModule(ReconstructionModule):
    def __init__(self, reconstructionParameters, inputType:ReconstructionModuleIOType=ReconstructionModuleIOType.KSPACE, outputType:ReconstructionModuleIOType=ReconstructionModuleIOType.KSPACE, svdPower=0.9, truncationNumberOverride=-1, device=None):
        ReconstructionModule.__init__(self, reconstructionParameters=reconstructionParameters, inputType=inputType, outputType=outputType) 
        self.svdPower = svdPower
        self.truncationNumberOverride = truncationNumberOverride 
        if(device is None):
            self.device = reconstructionParameters.defaultDevice
        else:
            self.device = device

    def __dict__(self):
        moduleDict  = {
            "type": str(self.__class__.__name__),
            "inputType": str(self.inputType.name),
            "outputType": str(self.outputType.name),
            "svdPower": self.svdPower,
            "truncationNumberOverride": self.truncationNumberOverride
        }
        return moduleDict

    def ProcessKspaceToKspace(self, inputData):
        outputData,_,_ = PerformSVDCoilCompression(inputData)
        return KspaceData(outputData)

    @staticmethod
    def FromJson(jsonInput, reconstructionParameters, inputType, outputType):  
        svdPower = jsonInput.get("svdPower")
        truncationNumberOverride = jsonInput.get("truncationNumberOverride")
        if svdPower != None and truncationNumberOverride != None:
            return CoilCompressionModule(reconstructionParameters, inputType, outputType, svdPower, truncationNumberOverride)
        else:
            print("CoilCombinationModule requires svdPower and truncationNumberOverride")
        