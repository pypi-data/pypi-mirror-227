from ..types import GradientType, SequenceUnits, Units
from . import GradientPreparationModule, Register
import numpy as np
import torch

@Register
class SpoilerModule(GradientPreparationModule):
    def __init__(self, dephasingRange, totalDuration, gradientDuration=None, units=None):
        GradientPreparationModule.__init__(self, gradientType=GradientType.SPOILER, units=units) 
        self.dephasingRange = dephasingRange       # Degrees
        self.totalDuration = totalDuration         # Seconds
        if(gradientDuration != None):
            self.gradientDuration = gradientDuration   # Seconds
        else:
            self.gradientDuration = 0

    def __str__(self):
        return GradientPreparationModule.__str__(self) + " || Dephasing Range (degrees): " + f'{self.dephasingRange:7.5f}' + " || Total Duration (s): " + f'{self.totalDuration:7.5f}'  + " || Gradient Duration (s): " + f'{self.gradientDuration:7.5f}'
            
    def __dict__(self):
        moduleDict  = {
            "type": str(self.__class__.__name__),
            "dephasingRange": self.dephasingRange,
            "totalDuration": self.totalDuration,
            "gradientDuration": self.gradientDuration
        }
        return moduleDict
    
    def ConvertUnits(self, targetUnits:SequenceUnits):
        if(self.units != targetUnits):
            self.dephasingRange =  Units.Convert(self.dephasingRange, self.units.angle, targetUnits.angle)
            self.totalDuration =  Units.Convert(self.totalDuration, self.units.time, targetUnits.time)
            self.gradientDuration =  Units.Convert(self.gradientDuration, self.units.time, targetUnits.time)
            self.units = targetUnits

    def CastToIntegers(self):
        self.dephasingRange = int(self.dephasingRange)
        self.totalDuration = int(self.totalDuration)
        self.gradientDuration = int(self.gradientDuration)

    def CastToFloats(self):
        self.dephasingRange = float(self.dephasingRange)
        self.totalDuration = float(self.totalDuration)
        self.gradientDuration = float(self.gradientDuration)

    @staticmethod
    def FromJson(jsonInput):  
        dephasingRange = jsonInput.get("dephasingRange")
        totalDuration = jsonInput.get("totalDuration")
        gradientDuration = jsonInput.get("gradientDuration")
        if totalDuration != None and dephasingRange != None:
            return SpoilerModule(dephasingRange, totalDuration, gradientDuration)
        else:
            print("SpoilerModule requires dephasingRange and totalDuration")
        
    def Simulate(self, dictionaryEntries, numSpins, device=None, inputMx=None, inputMy=None, inputMz=None): 
        if(device==None):
            if torch.cuda.is_available():
                device = torch.device("cuda")
            else:
                device = torch.device("cpu")    
        T1s = torch.tensor(dictionaryEntries['T1']).to(device)
        T2s = torch.tensor(dictionaryEntries['T2']).to(device)
        B1s = torch.tensor(dictionaryEntries['B1']).to(device)

        numDictionaryEntries = len(dictionaryEntries)
        phaseValues = np.linspace(-1*self.dephasingRange/2, self.dephasingRange/2, numSpins)
        spinOffresonances = torch.tensor(phaseValues).to(device)
        spinOffresonances = torch.deg2rad(spinOffresonances)

        Mx0 = torch.zeros((1, numSpins, numDictionaryEntries))
        My0 = torch.zeros((1, numSpins, numDictionaryEntries))
        Mz0 = torch.zeros((1, numSpins, numDictionaryEntries))
        Time = torch.zeros((1))

        Mx = torch.zeros((numSpins, numDictionaryEntries)).to(device)
        My = torch.zeros((numSpins, numDictionaryEntries)).to(device)
        Mz = torch.zeros((numSpins, numDictionaryEntries)).to(device)    
        TR = self.totalDuration - self.gradientDuration # Only allow for relaxation in the wait time after the dephasing is applied
        
        phaseValueCosines = torch.cos(spinOffresonances)
        phaseValueSines = torch.sin(spinOffresonances)

        if(inputMx is not None):
            if(torch.numel(inputMx) == numSpins*numDictionaryEntries and torch.numel(inputMy) == numSpins*numDictionaryEntries and torch.numel(inputMz) == numSpins*numDictionaryEntries):
                Mx = inputMx
                My = inputMy
                Mz = inputMz
            else:
                if(torch.numel(inputMx) == 1 and torch.numel(inputMy) == 1 and torch.numel(inputMz) == 1 ):
                    Mx = torch.ones(numSpins, numDictionaryEntries) * inputMx
                    My = torch.ones(numSpins, numDictionaryEntries) * inputMy
                    Mz = torch.ones(numSpins, numDictionaryEntries) * inputMz
                else: 
                    print("Simulation Failed: Number of input magnetization states doesn't equal number of requested spins to simulate.")
                    return
        else:
            Mx = torch.zeros(numSpins, numDictionaryEntries)
            My = torch.zeros(numSpins, numDictionaryEntries)
            Mz = torch.ones(numSpins, numDictionaryEntries)

        Mx = Mx.to(device);  My = My.to(device); Mz = Mz.to(device); 

        with torch.no_grad():
                tr = TR
                At2tr = torch.exp(-1*tr/T2s)
                At1tr = torch.exp(-1*tr/T1s)
                Bt1tr = 1-At1tr

                # Applying off-resonance to spins
                Mxi = Mx.t()
                Myi = My.t()
                Mx = (torch.multiply(phaseValueCosines,Mxi) - torch.multiply(phaseValueSines,Myi)).t()
                My = (torch.multiply(phaseValueSines,Mxi) + torch.multiply(phaseValueCosines,Myi)).t()

                # Relaxation over prep duration
                Mx = torch.multiply(Mx, At2tr)
                My = torch.multiply(My, At2tr)
                Mz = torch.multiply(Mz, At1tr)+Bt1tr

                # Reading value after TR and before TRE 
                Mx0[0,:,:]=Mx.cpu()
                My0[0,:,:]=My.cpu()
                Mz0[0,:,:]=Mz.cpu()
                Time[0] = self.totalDuration

                del tr, At2tr, At1tr, Bt1tr, Mxi, Myi
        del T1s, T2s, B1s, TR, Mx, My, Mz
        return Time,Mx0,My0,Mz0
