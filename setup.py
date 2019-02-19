# coding: utf-8

# !/usr/bin/env python

from distutils.core import setup

setup(
      name='JSON Schema OOP',
      version='2.5.2',
      description='OOP JSON Schema lets you write JSON-Schema classes and inherits them',
      author='Trung Phan',
      author_email='info@level96.de',
      url='https://github.com/level96/json-schema-oop',
      packages=['jsonschemaoop'],
      install_requires=[
            'jsonschema==2.6.0',
      ],
)
