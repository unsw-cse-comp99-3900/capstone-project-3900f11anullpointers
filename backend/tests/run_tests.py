# USAGE
# Run individual test files
# python3 run_tests.py test1.py test2.py ...

# Run all tests
# python3 run_tests.py 

import os
import sys
import unittest
import sys

# Set up the project and source paths
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
BACKEND_PATH = os.path.abspath(os.path.join(SCRIPT_DIR, ".."))
SOURCE_PATH = os.path.join(BACKEND_PATH, "src")
TESTS_PATH = os.path.join(BACKEND_PATH, "tests")

# Add the backend path and src to sys.path
sys.path.append(BACKEND_PATH)
sys.path.append(SOURCE_PATH)


# Add test file to test suite
def add_to_suite(file, test_loader, test_suite):
    if file.startswith("test") and file.endswith(".py"):
        test_path = os.path.join(TESTS_PATH, file)
        test_name = test_path.replace(TESTS_PATH + os.sep, '').replace(os.sep, '.')[:-3]
        print(f"Running {test_name}")
        tests = test_loader.loadTestsFromName(test_name)
        test_suite.addTests(tests)

# Discover and run all test files matching the pattern 'test*.py'
def run_tests():
    # Discover all test files
    test_loader = unittest.TestLoader()
    test_suite = unittest.TestSuite()
    
    if len(sys.argv) > 1:
        for file in sys.argv[1:]:
            add_to_suite(file, test_loader, test_suite)
    else: 
        for root, dirs, files in os.walk(TESTS_PATH):
            for file in files:
                add_to_suite(file, test_loader, test_suite)

    # Run the tests
    test_runner = unittest.TextTestRunner(verbosity=2)  
    result = test_runner.run(test_suite)
    
    # Return the appropriate exit code
    if result.wasSuccessful():
        return 0
    else:
        return 1

if __name__ == '__main__':
    sys.exit(run_tests())