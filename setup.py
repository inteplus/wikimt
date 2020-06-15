#!/usr/bin/env python3

from setuptools import setup, find_packages, find_namespace_packages
from mt.wiki.version import version

setup(name='wikimt',
      version=version,
      description="Minh-Tri Pham's modules for crawling the Wikipedia corpora",
      author=["Minh-Tri Pham"],
      packages=find_namespace_packages(include=['mt.*']),
      install_requires=[
          'basemt',
          'wikipedia',  # obviously
      ],
      url='https://github.com/inteplus/wikimt',
      project_urls={
          'Documentation': 'https://wikimt.readthedocs.io/en/stable/',
          'Source Code': 'https://github.com/inteplus/wikimt',
          }
      )
