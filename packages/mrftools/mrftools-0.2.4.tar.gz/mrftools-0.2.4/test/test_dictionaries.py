from mrftools import DictionaryParameters
import tempfile
import unittest
import numpy as np

class test_dictionaries(unittest.TestCase):

    def test(self):
        # Create dictionary parameter definition programmatically
        dictionary = DictionaryParameters.GenerateFixedPercent("Example", t1Range=(10,4000), t2Range=(1,400), percentStepSize=5, version="dev")

        # Export dictionary definition to JSON
        tmpdir = tempfile.TemporaryDirectory()
        dictionary.ExportToJson(baseFilepath=tmpdir.name+"/")

        # Read exported JSON to a DictionaryParameter object
        dictionaryParameters = DictionaryParameters.FromFile(tmpdir.name+"/Example_dev.dictionary")

        # Assert test results
        self.assertTrue(np.array_equal(dictionaryParameters.entries, dictionaryParameters.entries), 'dictionaries: dictionary entries do not match')
        tmpdir.cleanup()

if __name__ == '__main__':
    unittest.main()