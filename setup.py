#!/usr/bin/env python

from distutils.core import setup

setup(name='Oggify',
      version='2.0.0b1',
      description='Oggify - audio conversion tool and libraries',
      author='Scott Paul Robertson',
      author_email='spr@scottr.org',
      url='http://scottr.org/oggify/',
      packages=['oggify', 'oggify.plugins'],
      requires=['tag_wrapper'],
      scripts=['bin/oggify'],
     )
