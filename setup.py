#!/usr/bin/python

from setuptools import setup, find_packages

setup(name='dbs-client',
      version='0.1',
      description='Client tool / library for DBuildService',
      author='Honza Horak',
      author_email='hhorak@redhat.com',
      url='https://github.com/DBuildService/dbs-client',
      entry_points={
          'console_scripts': ['dbs-client=dbs_client.client:main'],
      },
      packages=find_packages(),
)

