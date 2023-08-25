from ..types import ReconstructionModuleIOType, ImageData
from . import ReconstructionModule, Register
import torch
import numpy as np
import torchkbnufft as tkbn


def PerformIFFTs(input, device): 
    input = torch.moveaxis(input,-1,0) 
    sizes = np.shape(input)
    numImages=sizes[0]; numCoils=sizes[1]; numPartitions=sizes[2]; matrixSize=sizes[3:5]
    images = torch.zeros((numImages, numCoils, numPartitions, matrixSize[0], matrixSize[1]), dtype=input.dtype)
    for image in np.arange(0, numImages):
        image_device = input[image,:,:,:,:].to(device)
        images[image,:,:,:,:] = torch.fft.ifftshift(torch.fft.ifft(image_device, dim=1), dim=1)
        del image_device
    torch.cuda.empty_cache()
    return torch.moveaxis(images, 0, -1).cpu()
    

@Register
class IFFTModule(ReconstructionModule):
    def __init__(self, reconstructionParameters, inputType:ReconstructionModuleIOType=ReconstructionModuleIOType.IMAGE, outputType:ReconstructionModuleIOType=ReconstructionModuleIOType.IMAGE, device=None):
        ReconstructionModule.__init__(self, reconstructionParameters=reconstructionParameters, inputType=inputType, outputType=outputType) 
        if(device is None):
            self.device = reconstructionParameters.defaultDevice
        else:
            self.device = device
            
    def __dict__(self):
        moduleDict  = {
            "type": str(self.__class__.__name__),
            "inputType": str(self.inputType.name),
            "outputType": str(self.outputType.name),
            "device": self.device.type,
        }
        return moduleDict

    def ProcessImageToImage(self, inputData):
        outputData = PerformIFFTs(inputData,self.device)
        return ImageData(outputData)

    @staticmethod
    def FromJson(jsonInput, reconstructionParameters, inputType, outputType):  
        device = jsonInput.get("device")
        if device != None:
            return IFFTModule(reconstructionParameters, inputType, outputType, torch.device(device))
        else:
            print("IFFTModule requires device")