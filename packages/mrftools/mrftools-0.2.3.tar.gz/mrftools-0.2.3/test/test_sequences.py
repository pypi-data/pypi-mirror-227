from mrftools import SequenceParameters, ScaledRectifiedSinusoid, Perlin, BitReverse, SequenceUnits, Units
from mrftools.SequenceModules import *
import numpy as np
import tempfile
import unittest

class test_sequences(unittest.TestCase):

    def test(self):

        # Create FISP parameters dynamically
        numTimepoints=960
        numLobes=12
        numSpirals=48
        TRs = np.ones(numTimepoints) * 0.010
        TEs = np.ones(numTimepoints) * 0.002
        flipangleLobeAmplitudeList = np.array(Perlin.Generate(numLobes, min=6, max=12, wavelength=1, firstValue=9, seed=5678))
        FAs = ScaledRectifiedSinusoid.Generate(numTimepoints, flipangleLobeAmplitudeList, minimum=4, patternInitialPhase=0)
        PHs = np.zeros(numTimepoints)
        IDs = BitReverse.Generate(numTimepoints, numSpirals)
        acquisitionModule = FISPAcquisitionModule(dephasingRange=360)
        acquisitionModule.Initialize(TRs, TEs, FAs, PHs,IDs)

        # Create sequence parameter definition programmatically
        sequence = SequenceParameters("Example", [], version="dev")
        sequence.modules.append(InversionModule(totalDuration=0.030))
        sequence.modules.append(acquisitionModule)
        sequence.modules.append(DeadtimeRecoveryModule(1.000))

        # Export parameter definition to JSON with units that the scanner expects
        tmpdir = tempfile.TemporaryDirectory()
        sequence.ExportToJson(baseFilepath=tmpdir.name+"/", exportUnits=SequenceUnits(Units.MICROSECONDS, Units.CENTIDEGREES), castToIntegers=False)

        # Read exported JSON to a SequenceParameter object with the units returned to normal
        sequenceParameters = SequenceParameters.FromFile(tmpdir.name+"/Example_dev.sequence")
        sequenceParameters.ConvertUnits(SequenceUnits(Units.SECONDS, Units.DEGREES))

        # Assert test results
        self.assertTrue(np.array_equal(sequenceParameters.modules[1].timepoints, sequence.modules[1].timepoints), 'sequences: acquisition timepoints do not match')
        self.assertTrue(len(sequence.modules) == len(sequenceParameters.modules), 'sequences: modules list lengths do not match')
        tmpdir.cleanup()

if __name__ == '__main__':
    unittest.main()