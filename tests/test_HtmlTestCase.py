'''
Created on Aug 30, 2010

@author: Theodore Campbell
'''
import unittest


class TestHtmlTestCase(unittest.TestCase):


    def setUp(self):
        pass


    def tearDown(self):
        pass


    def test_will_pass(self):
        self.assertTrue(True)

    def test_will_fail(self):
        self.assertTrue(False)

    def test_will_error(self):
        self.assertTrue(1 / 0)


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.test_do_something']
    unittest.main()
