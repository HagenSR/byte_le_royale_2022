# This is a quick example test file to show you the basics.
# Always remember to add the proper details to the __init__.py file in the 'tests' folder
# to insure your tests are run.

import unittest


class TestExample(
    unittest.TestCase):  # Your test class is a subclass of unittest.Testcase, this is important

    # This method is used to set up anything you wish to test prior to every
    # test method below.
    def setUp(self):
        self.d = {  # Here I'm just setting up a quick dictionary for example.
            # Any changes made to anything built in setUp DO NOT carry over to
            # later test methods
            "string": "Hello World!",
            "array": [1, 2, 3, 4, 5],
            "integer": 42,
            "bool": False
        }

    def test_dict_array(self):  # Test methods should always start with the word 'test'
        a = self.d["array"]
        # The heart of a test method are assertions
        self.assertEqual(a, [1, 2, 3, 4, 5])
        # These methods take two arguments and compare them to one another
        self.assertEqual(a[2], 3)
        # There are loads of them, and they're all very useful
        self.assertIn(5, a)

    def test_dict_string(self):
        s = self.d["string"]
        self.assertIn("Hello", s)
        self.assertNotEqual("Walkin' on the Sun", s)

    def test_dict_integer(self):
        i = self.d["integer"]
        self.assertGreater(50, i)
        # Checks within 7 decimal points
        self.assertAlmostEqual(i, 42.00000001)

    def test_dict_bool(self):
        b = self.d["bool"]
        self.assertFalse(b)
        self.assertEqual(b, False)

    # This is just the very basics of how to set up a test file
    # For more info: https://docs.python.org/3/library/unittest.html


if __name__ == '__main__':
    unittest.main
