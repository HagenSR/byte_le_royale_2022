import unittest
import game.test_suite.tests
import sys


def main():
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    runner = unittest.TextTestRunner(verbosity=3)

    suite.addTests(loader.loadTestsFromModule(game.test_suite.tests))

    sys.exit(not runner.run(suite).wasSuccessful())


if __name__ == '__main__':
    main()

# To run the test suite, make sure your terminal is in the root directory of the project (the 'byte_le_royale_2022 folder)
# Then, in your terminal, run 'python -m game.test_suite.runner'. This
# runs this file as a module of the entire project, allowing imports to
# function properly
