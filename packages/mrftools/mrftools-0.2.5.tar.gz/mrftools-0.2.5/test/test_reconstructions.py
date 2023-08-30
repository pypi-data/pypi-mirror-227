from mrftools import SimulationParameters, ReconstructionParameters
from mrftools.ReconstructionModules import *
import torch 
import tempfile
import unittest
import numpy as np

class test_reconstructions(unittest.TestCase):

    def test(self):

        # Load existing Simulation from file
        simulation = SimulationParameters.FromFile("example_data/Example_dev.simulation")

        # Initialize a reconstruction parameter definition
        reconstruction = ReconstructionParameters("Example", simulation, version="dev", outputMatrixSize=[256,256,120], defaultDevice=torch.device("cpu"))

        # Set up NUFFT parameters 
        trajectoryFilepath = "example_data/mrf_dependencies/trajectories/SpiralTraj_FOV300_256_uplimit2020_norm.bin"
        densityFilepath = "example_data/mrf_dependencies/trajectories/DCW_FOV300_256_uplimit2020.bin"
        trajectoryDesignMatrixSize = [256,256]
        numSpirals = 48
        ktraj, dcf = NUFFTModule.PrepTrajectoryObjects(reconstruction, trajectoryFilepath, densityFilepath, trajectoryDesignMatrixSize, numSpirals, useMeanDCF=True)

        # Create reconstruction parameter definition programmatically
        reconstruction.modules.append(SVDCompressionModule(reconstruction))
        reconstruction.modules.append(NUFFTModule(reconstruction, ktraj=ktraj, dcf=dcf))
        reconstruction.modules.append(IFFTModule(reconstruction))
        reconstruction.modules.append(CoilCombinationModule(reconstruction, device=torch.device("cpu"))) # Note that you can choose different devices for different modules
        reconstruction.modules.append(PatternMatchingModule(reconstruction))

        # Export reconstruction definition to JSON
        tmpdir = tempfile.TemporaryDirectory()
        reconstruction.ExportToJson(baseFilepath=tmpdir.name+"/")

        # Read exported JSON to a Simulation object
        reconstructionParameters = ReconstructionParameters.FromFile(tmpdir.name+"/Example_dev.reconstruction")

        # Assert test results
        self.assertTrue(len(reconstructionParameters.modules) == len(reconstruction.modules), 'reconstructions: module array lengths do not match')
        #self.assertTrue(np.array_equal(reconstructionParameters.truncationMatrix, simulation.truncationMatrix), 'scc: truncation matrices do not match')
        #self.assertTrue(np.array_equal(simulationParameters.truncatedResults, simulation.truncatedResults), 'scc: truncated results do not match')
        #self.assertTrue(np.array_equal(simulationParameters.singularValues, simulation.singularValues), 'scc: singularValues do not match')
        tmpdir.cleanup()

if __name__ == '__main__':
    unittest.main()