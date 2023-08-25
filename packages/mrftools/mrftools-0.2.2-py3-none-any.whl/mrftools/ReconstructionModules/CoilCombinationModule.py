from ..types import ReconstructionModuleIOType, ImageData
from . import ReconstructionModule, Register
import torch
import numpy as np
import torchkbnufft as tkbn

# Smooths coil images
## img: Input complex images, ``[y, x] or [z, y, x]``
##  box: Smoothing block size (default ``5``)
## returns simg: Smoothed complex image ``[y,x] or [z,y,x]``
def smooth(img, kernelSize, device=torch.device("cpu")):
    mean_conv = torch.nn.Conv3d(in_channels=1, out_channels=1, kernel_size=kernelSize, bias=False, padding='same')
    kernel_weights = (torch.ones((kernelSize[0], kernelSize[1], kernelSize[2]), dtype=torch.complex64)/(kernelSize[0]*kernelSize[1]*kernelSize[2])).to(device)
    mean_conv.weight.data = kernel_weights.unsqueeze(0).unsqueeze(0)
    output = mean_conv(img.unsqueeze(0).to(device)).squeeze()
    del kernel_weights, mean_conv, img
    return output 


def smooth_conv_3d(img, kernelSize, device=torch.device("cpu")):
    mean_conv = torch.nn.Conv3d(in_channels=1, out_channels=1, kernel_size=kernelSize, bias=False, padding='same')
    kernel_weights = (torch.ones((kernelSize, kernelSize, kernelSize), dtype=torch.complex64)/(kernelSize*kernelSize*kernelSize)).to(device)
    mean_conv.weight.data = kernel_weights.unsqueeze(0).unsqueeze(0)
    output = mean_conv(img.unsqueeze(1)).squeeze()
    del kernel_weights, mean_conv, img
    return output 

# Calculates the coilmaps for 3D data using an iterative version of the Walsh method
## img: Input images, ``[coil, y, x]``
## smoothing: Smoothing block size (default ``5``)
## niter: Number of iterations for the eigenvector power method (default ``3``)
## returns csm: Relative coil sensitivity maps, ``[coil, y, x]``
## returns rho: Total power in the estimated coils maps, ``[y, x]``
def calculateCoilmapsWalsh(img, smoothing=5, niter=3, device=torch.device("cpu")):
    with torch.no_grad():
        ncoils = img.shape[0]
        nx = img.shape[1]
        ny = img.shape[2]
        nz = img.shape[3]

        # Compute the sample covariance pointwise
        Rs = torch.zeros((ncoils,ncoils,nx,ny,nz),dtype=img.dtype)
        for p in range(ncoils):
            for q in range(ncoils):
                Rs[p,q,:,:,:] = img[p,:,:,:] * torch.conj(img[q,:,:,:])

        # Smooth the covariance
        for p in range(ncoils):
            for q in range(ncoils):
                smoothed = smooth(Rs[p,q,:,:,:], smoothing, device)
                Rs[p,q] = smoothed.cpu()
                del smoothed

        # At each point in the image, find the dominant eigenvector
        # and corresponding eigenvalue of the signal covariance
        # matrix using the power method
        rho = torch.zeros((nx, ny, nz)).to(device)
        csm = torch.zeros((ncoils, nx, ny, nz),dtype=torch.complex64).to(device)
        for z in range(nz):
            Rs_dev = Rs[:,:,:,:,z].to(device) 
            v_dev = torch.sum(Rs_dev,axis=0).to(device)
            lam_dev = torch.linalg.norm(v_dev, axis=0)
            v_dev = v_dev/lam_dev
            for iter in range(niter):
                v_dev = torch.sum(Rs_dev * v_dev, axis=1)
                lam_dev = torch.linalg.norm(v_dev, axis=0)
                v_dev = v_dev / lam_dev
            rho[:,:,z] = lam_dev
            csm[:,:,:,z] = v_dev
            del Rs_dev, v_dev, lam_dev
        return (csm, rho)
    

@Register
class CoilCombinationModule(ReconstructionModule):
    def PerformWalshCoilCombination(self, input, kernelSize=(5,5,1), niter=5):
        with torch.no_grad():
            shape = np.shape(input)
            combinedImageData = torch.zeros((shape[1], shape[2], shape[3], shape[4]), dtype=torch.complex64)
            coil_map, rho = calculateCoilmapsWalsh(input[:,:,:,:,0], smoothing=kernelSize, niter=niter, device=self.device)
            for svdComponent in np.arange(0,shape[4]):
                im = (input[:, :, :, :, svdComponent]).to(self.device)
                combinedImageData[:, :, :, svdComponent] = torch.sum((im * torch.conj(coil_map)), axis=0)
                del im
            torch.cuda.empty_cache()
            return torch.moveaxis(combinedImageData, 0,-2)

    def __init__(self, reconstructionParameters, inputType:ReconstructionModuleIOType=ReconstructionModuleIOType.IMAGE, outputType:ReconstructionModuleIOType=ReconstructionModuleIOType.IMAGE, mode="walsh", device=None):
        ReconstructionModule.__init__(self, reconstructionParameters=reconstructionParameters, inputType=inputType, outputType=outputType) 
        self.mode = mode
        if(device is None):
            self.device = reconstructionParameters.defaultDevice
        else:
            self.device = device

    def __dict__(self):
        moduleDict  = {
            "type": str(self.__class__.__name__),
            "inputType": str(self.inputType.name),
            "outputType": str(self.outputType.name),
            "mode": self.mode,
            "device": self.device.type
        }
        return moduleDict

    def ProcessImageToImage(self, inputData):
        with torch.no_grad():
            if(self.mode == "walsh"):
                outputData = self.PerformWalshCoilCombination(inputData)
            else:
                return None
            return ImageData(outputData)
    
    @staticmethod
    def FromJson(jsonInput, reconstructionParameters, inputType, outputType):  
        mode = jsonInput.get("mode")
        device = jsonInput.get("device")
        if mode != None and device != None:
            return CoilCombinationModule(reconstructionParameters, inputType, outputType, mode, torch.device(device))
        else:
            print("CoilCombinationModule requires mode and device")
        

    