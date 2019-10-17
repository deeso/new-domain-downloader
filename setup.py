#!/usr/bin/env python
from setuptools import setup, find_packages
import os


data_files = [(d, [os.path.join(d, f) for f in files])
              for d, folders, files in os.walk(os.path.join('src', 'config'))]


setup(name='new-domain-downloader',
      version='1.0',
      description='download new domains from whois newly registered domains',
      author='Adam Pridgen',
      author_email='adpridge@cisco.com',
      install_requires=['requests',],
      packages=find_packages('src'),
      package_dir={'': 'src'},
)
