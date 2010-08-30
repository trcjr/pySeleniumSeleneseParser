#!/usr/bin/env python
# encoding: utf-8

"""
A library for parsing Selenium Selenese HTML Test Suites and Cases.
"""


import BeautifulSoup
import pprint
import re
import os
import sys

sys.setrecursionlimit(50)

# Default number of seconds for test suite timeout.
HTML_TEST_SUITE_DEFAULT_TIMEOUT = 60
import_re = re.compile('^IMPORT:(?P<file_name>.*)')

class BaseHtmlTestObject(object):
    """An HTML Test Case"""
    def __init__(self, file):
        self.__path = os.path.abspath(file)
        self._soup = None
        self.__imported_by = []
        self.__imports = []
        self.testCaseResolver = None
        self._parsed = False
        self._commands = []

    @property
    def fileName(self):
        return os.path.basename(self.path)
    name = fileName

    @property
    def path(self):
        """The path of the HTML Test Case"""
        return self.__path

    @property
    def parsed(self):
        return self._parsed

    @property
    def soup(self):
        if not self._soup:
            self._soup = BeautifulSoup.BeautifulSoup(open(self.path))
        return self._soup

    @soup.setter
    def soup(self, value): #@DuplicatedSignature
        if isinstance(value, BeautifulSoup):
            self._soup = value

    def __repr__(self):
        return "<%(class_name)s: %(name)s>" % {'class_name': self.__class__.__name__, 'name': self.__path}

class HtmlTestCase(BaseHtmlTestObject):
    """An HTML Test Case"""
    def __init__(self, *args, **kwargs):
        super(self.__class__, self).__init__(*args, **kwargs)

    @property
    def commands(self):
        """The parsed commands"""
        if not self.parsed:
            self.parse()
        return self._commands

    @property
    def imported_by(self):
        """Test Cases that import this Test Case."""
        return self.__imported_by

    @property
    def imports(self):
        """Test Cases that this Test Case imports."""
        return self.__imports

    def addImport(self, testCase):
        if testCase not in self.__imports:
            self.__imports.append(testCase)
            testCase.addImportedBy(self)

    def addImportedBy(self, testCase):
        if testCase not in self.__imported_by:
            self.__imported_by.append(testCase)
            testCase.addImport(self)


    def resolveImports(self):
        if not self.parsed:
            self.parse()
        for testCase in self.imports:
            testCase.resolveImports()

            comments = self.soup.findAll(text=lambda text:isinstance(text, BeautifulSoup.Comment))

            for comment in comments:
                s = import_re.match(comment)
                if s:
                    comment_index = self.soup.tbody.contents.index(comment)

            insert_soup = BeautifulSoup.BeautifulSoup(testCase.soup.tbody.renderContents())
            print "---"
            pprint.pprint(insert_soup)
            self.soup.tbody.insert(comment_index + 1, insert_soup)

    def parse(self):
        """Parse the test case"""
        if self._parsed:
            return False
        self._parse_imports()
        self._parse_commands()
        self._parsed = True
        return True


    def _parse_commands(self,):
        """Parse for commands"""
        trs = self.soup.findAll('tr')
        for tr in trs:
            tds = list(tr.findAll('td'))
            if len(tds) == 3:
                v = [x.renderContents() for x in tds]
                c = {}
                c['command'] = v[0]
                c['target'] = v[1]
                c['value'] = v[2]
                self._commands.append(c)


    def _parse_imports(self,):
        """Parse for imports"""
        comments = self.soup.findAll(text=lambda text:isinstance(text, BeautifulSoup.Comment))
        for comment in comments:
            s = import_re.match(comment)
            if s:
#                comment_index = self.soup.tbody.contents.index(comment)
                another_testCase = self.testCaseResolver.testCaseForFile(s.group('file_name'))
                self.addImport(another_testCase)

    def find_commands_by(self, command=None, target=None, value=None):
        """Find a command by command, target or value"""
        if not self.parsed:
            self.parse()
        found_commands = []
        for command in self.commands:
            if command['command'] == command or \
            command['target'] == target or \
            command['value'] == value:
                found_commands.append(command)
        return found_commands

class HtmlTestSuite(BaseHtmlTestObject):
    """An HTML Test Suite"""
    def __init__(self, *args, **kwargs):
        super(self.__class__, self).__init__(*args, **kwargs)
        self.__test_cases = []
        self.__test_sute_timeout = -1

    def parse(self):
        """Parse the suite"""
        if self.parsed:
            return False

        links = self.soup.findAll('a')
        for l in links:
            tc = HtmlTestCase(l['href'])
            self.__test_cases.append(tc)
        return True

    @property
    def test_cases(self):
        """The test cases in the suite"""
        if not self.parsed:
            self.parse()
        return self.__test_cases

    @property
    def test_suite_timeout(self):
        """The timeout for the test suite"""
        if self.__test_sute_timeout == -1:
            found_timeouts = []
            for test_case in self.test_cases:
                found_timeouts.extend(
                      test_case.find_commands_by(value='test_suite_timeout')
                      )
            for timeout in found_timeouts:
                if timeout['target'] > self.__test_sute_timeout:
                    self.__test_sute_timeout = timeout['target']
            if self.__test_sute_timeout == -1:
                self.__test_sute_timeout = HTML_TEST_SUITE_DEFAULT_TIMEOUT
        return self.__test_sute_timeout

class HtmlTestCaseImportResolver(HtmlTestCase):
    def __init__(self, *args, **kwargs):
        HtmlTestCase.__init__(self, *args, **kwargs)
        self.__testCases = {}
        self.testSuiteResolver = None

    @property
    def testCases(self):
        return self.__testCases

    def testCaseForFile(self, file):
        testCase = self.__testCases.get(file, HtmlTestCase(file))
        if testCase not in self.__testCases:
            testCase.testCaseResolver = self
            self.__testCases[testCase.path] = testCase
        return testCase

class HtmlTestSuiteImportResolver(HtmlTestCaseImportResolver):
    def __init__(self, *args, **kwargs):

        HtmlTestCaseImportResolver.__init__(self, *args, **kwargs)
        self.__testCases = []

    @property
    def testCases(self):
        if self.__testCases == []:
            self.__loadTestCases()
        return self.__testCases


    def __loadTestCases(self):
        print self.soup.prettify()
        links = self.soup.findAll('a')
        print links
        for a in links:
            htmlTestCaseResolver = HtmlTestCaseImportResolver(self.name)
            testCase = htmlTestCaseResolver.testCaseForFile(a['href'])
            testCase.parsedFileName = "%s_parsed.html" % testCase.name
            self.__testCases.append(testCase)

    def resolveImports(self):
        for testCase in self.testCases:
            testCase.resolveImports()
