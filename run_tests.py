import unittest
import importlib
test_mod = importlib.import_module("tests.test_v3_temporal_truth")
suite = unittest.TestLoader().loadTestsFromModule(test_mod)
unittest.TextTestRunner(verbosity=2).run(suite)
