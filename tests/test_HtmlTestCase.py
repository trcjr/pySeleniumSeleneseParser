#!/usr/bin/env python
'''
Created on Aug 30, 2010

@author: Theodore Campbell
'''
import unittest
import pySeleniumSeleneseParser

test_case_path = "SeleniumSeleneseTestCase1.html"

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


    def test_create_test_case_object(self):
        test_case = None


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.test_do_something']
    unittest.main()
