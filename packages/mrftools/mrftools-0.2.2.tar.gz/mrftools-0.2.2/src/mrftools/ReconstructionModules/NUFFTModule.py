from ..types import ReconstructionModuleIOType, ImageData
from . import ReconstructionModule, Register
import torch
import numpy as np
import torchkbnufft as tkbn

@Register
class NUFFTModule(ReconstructionModule):

    @staticmethod
    def PrepTrajectoryObjects(reconstructionParameters, trajectoryFilepath, densityFilepath, trajectoryDesignMatrixSize, numSpirals, useMeanDCF=True):
        trajectoryBuffer = np.fromfile(trajectoryFilepath, dtype=np.complex64)
        densityBuffer = np.fromfile(densityFilepath, dtype=np.float32)
        trajectoryBuffer.real = trajectoryBuffer.real * (trajectoryDesignMatrixSize[0]/reconstructionParameters.outputMatrixSize[0])
        trajectoryBuffer.imag = trajectoryBuffer.imag * (trajectoryDesignMatrixSize[1]/reconstructionParameters.outputMatrixSize[1])
        trajectorySplit = np.stack((trajectoryBuffer.real, trajectoryBuffer.imag))*2*np.pi
        ktraj = torch.tensor(trajectorySplit, dtype=torch.float32)
        if(useMeanDCF):
            densityBuffer = np.tile(np.mean(np.split(densityBuffer, numSpirals), axis=0), numSpirals)
        dcf = torch.tensor(densityBuffer)
        return ktraj, dcf

    def PerformAdjointNUFFTs(self, input): 
        with torch.no_grad():
            adjoint_nufft = tkbn.KbNufftAdjoint(im_size=(self.matrixX, self.matrixY), grid_size=(self.matrixX, self.matrixY), numpoints=self.numNearestNeighbors).to(self.device)
            input = torch.moveaxis(input,-1,0) 
            numImages = input.shape[0]
            numCoils = input.shape[1]
            numPartitions = input.shape[2]
            output = torch.zeros(numImages, numCoils, numPartitions, self.matrixX, self.matrixY, dtype=input.dtype)
            for partition in torch.arange(0,numPartitions):
                readout_device = torch.swapaxes(input[:, :, partition, :, :], -1,-2).reshape(numImages, numCoils, -1).to(self.device) 
                nufftResult = adjoint_nufft(readout_device * self.dcf, self.ktraj, norm="ortho")
                output[:,:,partition,:,:] = nufftResult
                del readout_device, nufftResult
            return torch.moveaxis(output, 0, -1)
    
    def __init__(self, reconstructionParameters, inputType:ReconstructionModuleIOType=ReconstructionModuleIOType.KSPACE, outputType:ReconstructionModuleIOType=ReconstructionModuleIOType.IMAGE, ktraj=None, dcf=None, numNearestNeighbors=3, device=None):
        ReconstructionModule.__init__(self, reconstructionParameters=reconstructionParameters, inputType=inputType, outputType=outputType) 
        self.numNearestNeighbors = numNearestNeighbors 
        if(device is None):
            self.device = reconstructionParameters.defaultDevice
        else:
            self.device = device
        self.matrixX = reconstructionParameters.outputMatrixSize[0]
        self.matrixY = reconstructionParameters.outputMatrixSize[1]
        self.ktraj = ktraj.to(self.device)
        self.dcf = dcf.to(self.device)
        self.sqrt_dcf = torch.sqrt(self.dcf)

    def __dict__(self):
        moduleDict  = {
            "type": str(self.__class__.__name__),
            "inputType": str(self.inputType.name),
            "outputType": str(self.outputType.name),
            "ktraj": self.ktraj.tolist(),
            "dcf": self.dcf.tolist(),
            "numNearestNeighbors": self.numNearestNeighbors,
            "device": self.device.type
        }
        return moduleDict

    def ProcessKspaceToImage(self, inputData):
        with torch.no_grad():
            outputData = self.PerformAdjointNUFFTs(inputData)
            return ImageData(outputData)

    @staticmethod
    def FromJson(jsonInput, reconstructionParameters, inputType, outputType):  
        ktrajJson = jsonInput.get("ktraj")
        ktraj = torch.tensor(np.array(ktrajJson))
        dcfJson = jsonInput.get("dcf")
        dcf = torch.tensor(np.array(dcfJson))
        numNearestNeighbors = jsonInput.get("numNearestNeighbors")
        device = jsonInput.get("device")
        if ktrajJson != None and dcfJson != None and numNearestNeighbors != None and device != None:
            return NUFFTModule(reconstructionParameters, inputType, outputType, ktraj, dcf, numNearestNeighbors, torch.device(device))
        else:
            print("NUFFTModule requires ktraj, dcf, numNearestNeighbors, and device")