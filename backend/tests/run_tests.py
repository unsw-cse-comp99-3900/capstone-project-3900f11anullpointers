import os
import sys
import unittest
from termcolor import colored

# Set up the project and source paths
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
BACKEND_PATH = os.path.abspath(os.path.join(SCRIPT_DIR, ".."))
SOURCE_PATH = os.path.join(BACKEND_PATH, "src")
TESTS_PATH = os.path.join(BACKEND_PATH, "tests")

# Add the backend path and src to sys.path
sys.path.append(BACKEND_PATH)
sys.path.append(SOURCE_PATH)

# Custom test runner to add color
class ColoredTextTestResult(unittest.TextTestResult):
    def addSuccess(self, test):
        super().addSuccess(test)
        self.stream.write(colored('ok', 'green') + '\n')

    def addFailure(self, test, err):
        super().addFailure(test, err)
        self.stream.write(colored('FAIL', 'red') + '\n')

    def addError(self, test, err):
        super().addError(test, err)
        self.stream.write(colored('ERROR', 'yellow') + '\n')

class ColoredTextTestRunner(unittest.TextTestRunner):
    resultclass = ColoredTextTestResult

# Discover and run all test files matching the pattern 'test*.py'
def run_tests():
    # Discover all test files
    test_loader = unittest.TestLoader()
    test_suite = test_loader.discover("tests", pattern="test_*.py")
    
    # Run the tests
    test_runner = ColoredTextTestRunner(verbosity=2)
    result = test_runner.run(test_suite)
    
    # Return the appropriate exit code
    if result.wasSuccessful():
        return 0
    else:
        return 1

if __name__ == '__main__':
    sys.exit(run_tests())
