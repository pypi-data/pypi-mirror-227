from mrftools import SequenceParameters, DictionaryParameters, SimulationParameters, SequenceUnits, Units, PlotSimulationTimeseries
import tempfile
import unittest
import numpy as np

class test_simulations(unittest.TestCase):

    def test(self):

        # Load existing SequenceParameters and DictionaryParameters from files
        sequenceParameters = SequenceParameters.FromFile("example_data/Example_dev.sequence")
        dictionaryParameters = DictionaryParameters.FromFile("example_data/Example_dev.dictionary")

        # Explicitly convert sequence to simulation's expected units (will be done automatically if missing)
        sequenceParameters.ConvertUnits(SequenceUnits(Units.SECONDS, Units.DEGREES))

        # Create simulation definition programmatically
        simulation = SimulationParameters(sequenceParameters, dictionaryParameters, "Example", numSpins=30)
        simulation.Execute(numBatches=10)
        simulation.CalculateSVD(truncationNumberOverride=8)

        # Export simulation definition to JSON
        tmpdir = tempfile.TemporaryDirectory()
        simulation.ExportToJson(baseFilepath=tmpdir.name+"/")

        # Read exported JSON to a Simulation object
        simulationParameters = SimulationParameters.FromFile(tmpdir.name+"/Example_dev.simulation")

        # Assert test results
        self.assertTrue(np.array_equal(simulationParameters.truncationMatrix, simulation.truncationMatrix), 'scc: truncation matrices do not match')
        self.assertTrue(np.array_equal(simulationParameters.truncatedResults, simulation.truncatedResults), 'scc: truncated results do not match')
        self.assertTrue(np.array_equal(simulationParameters.singularValues, simulation.singularValues), 'scc: singularValues do not match')
        tmpdir.cleanup()

if __name__ == '__main__':
    unittest.main()