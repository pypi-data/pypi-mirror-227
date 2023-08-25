from ..types import RFType, SequenceUnits, Units
from . import RFPreparationModule, Register
import torch

@Register
class T2PreparationModule(RFPreparationModule):
    def __init__(self, echoTime, rfDuration=0, units=None):
        RFPreparationModule.__init__(self, rfType=RFType.COMPOSITE, units=units) 
        self.echoTime = echoTime         # Seconds
        if rfDuration != None:
            self.rfDuration = rfDuration         # Seconds
        else: 
            self.rfDuration = 0

    def __str__(self):
        return RFPreparationModule.__str__(self) + " || Echo Time (s): " + f'{self.echoTime:7.5f}' + " || RF Duration (s): " + f'{self.rfDuration:7.5f}'
        
    def __dict__(self):
        moduleDict  = {
            "type": str(self.__class__.__name__),
            "echoTime": self.echoTime,
            "rfDuration": self.rfDuration
        }
        return moduleDict
    
    def ConvertUnits(self, targetUnits:SequenceUnits):
        if(self.units != targetUnits):
            self.echoTime =  Units.Convert(self.echoTime, self.units.time, targetUnits.time)
            self.rfDuration =  Units.Convert(self.rfDuration, self.units.time, targetUnits.time)
            self.units = targetUnits

    def CastToIntegers(self):
        self.echoTime = int(self.echoTime)
        self.rfDuration = int(self.rfDuration)

    def CastToFloats(self):
        self.echoTime = float(self.echoTime)
        self.rfDuration = float(self.rfDuration)

    @staticmethod
    def FromJson(jsonInput):  
        echoTime = jsonInput.get("echoTime")
        rfDuration = jsonInput.get("rfDuration")
        if echoTime != None:
            return T2PreparationModule(echoTime, rfDuration)
        else:
            print("SpoilerModule requires echoTime")
            
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

        Mx = torch.zeros((numSpins, numDictionaryEntries)).to(device)
        My = torch.zeros((numSpins, numDictionaryEntries)).to(device)
        Mz = torch.zeros((numSpins, numDictionaryEntries)).to(device) 

        TR = torch.tensor([self.echoTime/4, self.echoTime/2, self.echoTime/4, 0])
        FA = torch.deg2rad(torch.tensor([90, 180, 180, 90]))
        PH = torch.deg2rad(torch.tensor([90,   0, 180,270]))

        Mx0 = torch.zeros((len(TR), numSpins, numDictionaryEntries))
        My0 = torch.zeros((len(TR), numSpins, numDictionaryEntries))
        Mz0 = torch.zeros((len(TR), numSpins, numDictionaryEntries))
        Time = torch.zeros((len(TR)))
        #TR = self.totalDuration - self.rfDuration # Only allow for relaxation in the wait time after the RF is applied
            
        if(inputMx is not None):
            if(torch.numel(inputMx) == numSpins*numDictionaryEntries and torch.numel(inputMy) == numSpins*numDictionaryEntries and torch.numel(inputMz) == numSpins*numDictionaryEntries):
                Mx = inputMx
                My = inputMy
                Mz = inputMz
            else:
                if(torch.numel(inputMx) == 1 and torch.numel(inputMy) == 1 and torch.numel(inputMz) == 1 ):
                    Mx = (torch.ones(numSpins, numDictionaryEntries) * inputMx)
                    My = (torch.ones(numSpins, numDictionaryEntries) * inputMy)
                    Mz = (torch.ones(numSpins, numDictionaryEntries) * inputMz)
                else: 
                    print("Simulation Failed: Number of input magnetization states doesn't equal number of requested spins to simulate.")
                    return
        else:
            Mx = torch.zeros(numSpins, numDictionaryEntries)
            My = torch.zeros(numSpins, numDictionaryEntries)
            Mz = torch.ones(numSpins, numDictionaryEntries)

        Mx = Mx.to(device);  My = My.to(device); Mz = Mz.to(device); 

        with torch.no_grad():
            accumulatedTime = 0
            for iFlip in range(len(FA)):
                fa = FA[iFlip]
                tr = TR[iFlip]
                ph = PH[iFlip]
                
                Time[iFlip] = accumulatedTime
                accumulatedTime = accumulatedTime + tr

                At2tr = torch.exp(-1*tr/T2s)
                At1tr = torch.exp(-1*tr/T1s)
                Bt1tr = 1-At1tr

                # M2 = Rphasep*Rflip*Rphasem*M1;       % RF effect  
                # Applying Rphasem = [cos(-iph) -sin(-iph) 0; sin(-iph) cos(-iph) 0; 0 0 1];  
                Mxi = Mx; Myi = My; Mzi = Mz
                Mx = torch.multiply(torch.cos(-ph),Mxi) - torch.multiply(torch.sin(-ph), Myi)
                My = torch.multiply(torch.sin(-ph),Mxi) + torch.multiply(torch.cos(-ph), Myi)
                Mz = Mzi

                # Applying flip angle = [1 0 0; 0 cos(randflip(ii)) -sin(randflip(ii)); 0 sin(randflip(ii)) cos(randflip(ii))];
                Mxi = Mx; Myi = My; Mzi = Mz
                Mx = Mxi
                My = torch.multiply(torch.cos(fa),Myi)-torch.multiply(torch.sin(fa),Mzi)
                Mz = torch.multiply(torch.sin(fa),Myi)+torch.multiply(torch.cos(fa),Mzi)

                # Applying Rphasep = [cos(iph) -sin(iph) 0; sin(iph) cos(iph) 0; 0 0 1];  
                Mxi = Mx; Myi = My; Mzi = Mz
                Mx = torch.multiply(torch.cos(ph),Mxi) - torch.multiply(torch.sin(ph), Myi)
                My = torch.multiply(torch.sin(ph),Mxi) + torch.multiply(torch.cos(ph), Myi)
                Mz = Mzi

                # Relaxation over delay duration
                Mx = torch.multiply(Mx, At2tr)
                My = torch.multiply(My, At2tr)
                Mz = torch.multiply(Mz, At1tr)+Bt1tr

                Mx0[iFlip,:,:]=Mx.cpu()
                My0[iFlip,:,:]=My.cpu()
                Mz0[iFlip,:,:]=Mz.cpu()

                #Spoil at end

                del fa, tr, At2tr, At1tr, Bt1tr, Mxi, Myi, Mzi
        del T1s, T2s, B1s, FA, TR, PH, Mx, My, Mz
        return Time,Mx0,My0,Mz0
