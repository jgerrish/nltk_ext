import os
import unittest


def suite() -> unittest.suite.TestSuite:
    import unittest

    this_dir = os.path.dirname(__file__)
    loader = unittest.defaultTestLoader
    standard_tests = unittest.TestSuite()
    package_tests = loader.discover(start_dir=this_dir, pattern="*_test.py")
    standard_tests.addTests(package_tests)
    return standard_tests


def load_tests(
    loader: unittest.TestLoader,
    standard_tests: unittest.suite.TestSuite,
    pattern: str,
) -> unittest.suite.TestSuite:
    # top level directory cached on loader instance
    this_dir = os.path.dirname(__file__)
    package_tests = loader.discover(start_dir=this_dir)
    standard_tests.addTests(package_tests)
    return standard_tests


if __name__ == "__main__":
    import unittest

    loader = unittest.defaultTestLoader
    standard_tests = unittest.TestSuite()
    unittest.TextTestRunner(verbosity=2).run(standard_tests)
