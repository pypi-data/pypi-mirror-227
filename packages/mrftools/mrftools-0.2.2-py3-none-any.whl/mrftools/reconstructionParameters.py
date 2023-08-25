from __future__ import annotations
import torch
import json as json
from . import Units, SequenceUnits, SimulationParameters
from .ReconstructionModules import ReconstructionModule
from importlib.metadata import version  
    
class ReconstructionParameters:
    def __init__(self, name:str, simulation:SimulationParameters, version="dev", outputMatrixSize=[-1,-1,-1], modules=[], defaultDevice=torch.device("cpu")):
        self.name = name
        self.version = version
        self.simulation = simulation
        self.outputMatrixSize = outputMatrixSize
        self.modules = modules 
        self.defaultDevice = defaultDevice

    def __str__(self):
        moduleDescriptions = ""
        for module in self.modules:
            moduleDescriptions = moduleDescriptions + str(module) + "\n------------------\n"
        return "Reconstruction: " + self.name + "\nModules:\n------------------\n" + moduleDescriptions
    
    def __dict__(self):
        mrftools_version = version("mrftools")
        reconstructionDict  = {
            "name": self.name,
            "version": self.version,
            "outputMatrixSize": self.outputMatrixSize,
            "defaultDevice": self.defaultDevice.type,
            "modules": [],
            "simulation": self.simulation.__dict__().get("simulation")
        }
        for module in self.modules:
            reconstructionDict.get("modules").append(module.__dict__())
        reconstructionParametersDict = {
            "mrftools_version":mrftools_version,
            "reconstruction":reconstructionDict
        }
        return reconstructionParametersDict
    
    ## Cast to integers during export is NOT a lossless process, so that simulations run on the exported data match scanner execution
    def ExportToJson(self, baseFilepath=""):
        reconstructionFilename = baseFilepath+self.name+"_"+self.version+".reconstruction"
        with open(reconstructionFilename, 'w') as outfile:
            json.dump(self.__dict__(), outfile, indent=2)
    
    def Run(self, input):
        with torch.no_grad():
            current = input
            for module in self.modules:
                print(module.__class__.__name__)
                current = module.Process(current)
            return current

    @staticmethod
    def FromJson(inputJson):
        mrftoolsVersion = inputJson.get("mrftools_version")
        #print("Input file mrttools Version:", mrftoolsVersion)

        reconstructionJson = inputJson.get("reconstruction")
        reconstructionName = reconstructionJson.get("name")
        simulationJson = reconstructionJson.get("simulation")
        simulation = SimulationParameters.FromJson(simulationJson)
        reconstructionVersion = reconstructionJson.get("version")
        outputMatrixSize = reconstructionJson.get("outputMatrixSize")
        defaultDevice = reconstructionJson.get("defaultDevice")
        reconstructionParameters = ReconstructionParameters(reconstructionName, simulation, reconstructionVersion, outputMatrixSize, [], torch.device(defaultDevice))
        modulesJson = reconstructionJson.get("modules")
        for moduleJson in modulesJson:
            reconstructionParameters.modules.append(ReconstructionModule.FromJson(moduleJson, reconstructionParameters))
        return reconstructionParameters

    @staticmethod
    def FromFile(path):
        with open(path) as inputFile:
            inputJson = json.load(inputFile)
            return ReconstructionParameters.FromJson(inputJson)

