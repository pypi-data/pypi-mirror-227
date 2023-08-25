from __future__ import annotations
import torch
import json as json
from . import Units, SequenceUnits
from .SequenceModules import SequenceModule
from importlib.metadata import version  

class SequenceParameters:
    def __init__(self, name:str, modules=[], version="dev", sequenceUnits=SequenceUnits(Units.SECONDS,Units.DEGREES)):
        self.name = name
        self.modules = modules 
        self.version = version
        self.units = sequenceUnits
        #if(len(modules) > 0 ):
        #    print("Sequence Parameter set '"+ self.name + "' initialized with " + str(len(self.modules)) + " modules")

    def __str__(self):
        moduleDescriptions = ""
        for module in self.modules:
            moduleDescriptions = moduleDescriptions + str(module) + "\n------------------\n"
        return "Sequence: " + self.name + "\nModules:\n------------------\n" + moduleDescriptions
    
    def __dict__(self):
        mrftools_version = version("mrftools")
        sequenceDict  = {
            "name": self.name,
            "version": self.version,
            "units" : self.units.__dict__(),
            "modules": []
        }
        for module in self.modules:
            sequenceDict.get("modules").append(module.__dict__())
        sequenceParametersDict = {
            "mrftools_version":mrftools_version,
            "sequence":sequenceDict
        }
        return sequenceParametersDict

    def ConvertUnits(self, newUnits):
        if (self.units.time != newUnits.time) or (self.units.angle != newUnits.angle):
            for module in self.modules:
                module.ConvertUnits(newUnits)
            self.units = newUnits

    def CastToIntegers(self):
        for module in self.modules:
            module.CastToIntegers() 

    def CastToFloats(self):
        for module in self.modules:
            module.CastToFloats() 
    
    ## Cast to integers during export is NOT a lossless process, so that simulations run on the exported data match scanner execution
    def ExportToJson(self, baseFilepath="", exportUnits=SequenceUnits(Units.MICROSECONDS, Units.CENTIDEGREES), castToIntegers=True):
        originalUnits = self.units
        self.ConvertUnits(exportUnits)
        if castToIntegers:
            self.CastToIntegers()
        sequenceFilename = baseFilepath+self.name+"_"+self.version+".sequence"
        with open(sequenceFilename, 'w') as outfile:
            json.dump(self.__dict__(), outfile, indent=2)
        if castToIntegers:
            self.CastToFloats()
        self.ConvertUnits(originalUnits)
    
    def Simulate(self, dictionaryEntries, numSpins, device=None):
        from .SequenceModules.AcquisitionModule import AcquisitionModule
        if self.units.time != Units.SECONDS or self.units.angle != Units.DEGREES:
            print("Sequence Units are not the required Seconds/Degrees. Converting before simulation. ")
            self.ConvertUnits(SequenceUnits(Units.SECONDS, Units.DEGREES))
            
        Time = torch.zeros([1]); 
        Mx0 = torch.zeros([1,numSpins, len(dictionaryEntries)]); ReadoutMx0 = torch.zeros([1,numSpins, len(dictionaryEntries)]); 
        My0 = torch.zeros([1,numSpins, len(dictionaryEntries)]); ReadoutMy0 = torch.zeros([1,numSpins, len(dictionaryEntries)]); 
        Mz0 = torch.ones([1,numSpins, len(dictionaryEntries)]);  ReadoutMz0 = torch.ones([1,numSpins, len(dictionaryEntries)])

        for module in self.modules:
            resultTime, resultMx0, resultMy0, resultMz0 = module.Simulate(dictionaryEntries, numSpins, device=device, inputMx=Mx0[-1,:,:], inputMy=My0[-1,:,:], inputMz=Mz0[-1,:,:])
            Time = torch.cat((Time, resultTime+Time[-1])); Mx0 = torch.cat((Mx0, resultMx0)); My0 = torch.cat((My0, resultMy0)); Mz0 = torch.cat((Mz0, resultMz0)); 
            
            if(issubclass(module.__class__, AcquisitionModule)):
                ReadoutMx0 = torch.cat((ReadoutMx0, resultMx0))
                ReadoutMy0 = torch.cat((ReadoutMy0, resultMy0))
                ReadoutMz0 = torch.cat((ReadoutMz0, resultMz0))
        return Time, (Mx0, My0, Mz0), (ReadoutMx0, ReadoutMy0, ReadoutMz0)

    @staticmethod
    def FromJson(inputJson):
        mrftoolsVersion = inputJson.get("mrftools_version")
        
        if(mrftoolsVersion != None):
            #print("Input file mrttools Version:", mrftoolsVersion)
            sequenceJson = inputJson.get("sequence")
        else: 
            sequenceJson = inputJson
        sequenceName = sequenceJson.get("name")
        sequenceVersion = sequenceJson.get("version")
        unitsJson = sequenceJson.get("units")
        modulesJson = sequenceJson.get("modules")

        sequenceUnits = SequenceUnits.FromJson(unitsJson)
        sequenceModules = []
        for moduleJson in modulesJson:
            sequenceModules.append(SequenceModule.FromJson(moduleJson, sequenceUnits))

        return SequenceParameters(sequenceName,sequenceModules, sequenceVersion, sequenceUnits)
    
    @staticmethod
    def FromFile(path):
        with open(path) as inputFile:
            inputJson = json.load(inputFile)
            return SequenceParameters.FromJson(inputJson)
"""
    def Export(self, filename:str, force=False):
        if ".mrf" in filename:
            outfile = h5py.File(filename, "a")
            try:
                outfile.create_group("sequenceParameters")
            except:
                pass
            if (self.name in list(outfile["sequenceParameters"].keys())) and not force:
                print("Sequence Parameter set '" + self.name + "' already exists in .mrf file. Specify 'force' to overwrite")
            else:
                try:
                    del outfile["sequenceParameters"][self.name]
                except:
                    pass
                sequenceParameters = outfile["sequenceParameters"].create_group(self.name)
                sequenceParameters.attrs.create("name", self.name)
                sequenceParameters.attrs.create("type", self.type.name)
                sequenceParameters["timepoints"] = self.timepoints
                outfile.close()
        else:
            print("Input is not a .mrf file")

"""