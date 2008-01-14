#!/usr/bin/env python

from distutils.core import setup

setup(name='Oggify',
      version='2.0.0b1',
      description='audio conversion tool for music library conversion',
      long_description="""Oggify provides the tools needed to convert an
      audio library from one format to another. Orginally designed to handle
      the author's need of FLAC -> Ogg Vorbis. It ships with support for FLAC
      as the source format, and Ogg Vorbis and MP3 as output formats. Requires
      flac, vorbis-tools, and lame for full operation. Supports other formats
      through a plugin system.""",
      author='Scott Paul Robertson',
      author_email='spr@scottr.org',
      url='http://scottr.org/oggify/',
      packages=['oggify', 'oggify.plugins'],
      requires=['tag_wrapper'],
      scripts=['bin/oggify'],
      classifiers=[
          'Development Status :: 4 - Beta',
          'Environment :: Console',
          'Intended Audience :: Advanced End Users',
          'License :: OSI Approved :: GNU General Public License (GPL)',
          'Operating System :: MacOS :: MacOS X',
          'Operating System :: POSIX :: Linux',
          'Programming Language :: Python',
          'Topic :: Multimedia :: Sound/Audio :: Conversion',
          ]
     )
