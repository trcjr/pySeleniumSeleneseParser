from setuptools import setup, find_packages
from disttest import test
import sys, os

version = '0.1'

setup(name='pySeleniumSeleneseParser',
    version=version,
    description="Parse Selenium Selenese",
    long_description=open("README.txt").read() + '\n\n' + open('CHANGES.txt').read(),
    classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
    keywords='Selenium Selenese',
    author='Theodore R Campbell Jr',
    author_email='trcjr@stupidfoot.com',
    url='',
    license='GPL',
    packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
      ''
    ],
    entry_points="""
    # -*- Entry points: -*-
    """,
    cmdclass={'test': test},
    options={
        'test': {
            'test_dir':['tests'], # will run all .py files in the tests/ directory
        }
    },

    )
