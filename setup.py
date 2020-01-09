#!/usr/bin/env python

from distutils.core import setup
from oggify import version
import os, os.path

if os.uname()[0] != 'Darwin':
    aacp = os.path.join('oggify', 'plugins', 'aac.py')
    alacp = os.path.join('oggify', 'plugins', 'alac.py')
    if os.path.exists(aacp):
        os.unlink(aacp)
    if os.path.exists(alacp):
        os.unlink(alacp)

setup(name='oggify',
      version=version,
      description='audio conversion tool for music library conversion',
      long_description="""Oggify provides the tools needed to convert an
      audio library from one format to another. Orginally designed to handle
      the author's need of FLAC -> Ogg Vorbis. It ships with support for FLAC
      as the source format, and Ogg Vorbis, Opus, and MP3 as output formats.
      Requires flac, vorbis-tools, opus-tools and lame for full operation.
      Supports other formats through a plugin system.""",
      author='Scott Paul Robertson',
      author_email='spr@scottr.org',
      url='http://scottr.org/oggify/',
      packages=['oggify', 'oggify.plugins', 'tag_wrapper'],
      requires=['mutagen'],
      provides=['tag_wrapper', 'oggify'],
      scripts=['bin/oggify'],
      data_files=[('share/man/man1', ['man/man1/oggify.1.gz'])],
      license="GNU GPLv2 or later",
      platforms=['linux', 'Apple OS X'],
      classifiers=[
          'Development Status :: 4 - Beta',
          'Environment :: Console',
          'Intended Audience :: End Users/Desktop',
          'License :: OSI Approved :: GNU General Public License (GPL)',
          'Operating System :: MacOS :: MacOS X',
          'Operating System :: POSIX :: Linux',
          'Programming Language :: Python :: 3 :: Only',
          'Topic :: Multimedia :: Sound/Audio :: Conversion',
          ]
     )
