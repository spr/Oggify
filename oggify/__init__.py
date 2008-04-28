# oggify - main part of Oggify (includes the main class)
# Copyright (c) 2008 Scott Paul Robertson (spr@scottr.org)
#
# This is part of Oggify (http://scottr.org/oggify/)
#
# Oggify is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version
# 
# Oggify is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with Oggify; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA

import os, os.path, sys, re, tempfile, shutil, atexit
from oggify import utils

class Oggify(object):
    """Class for the oggify object that does all the work for Oggify"""

    def __init__(self, src, dst, options, temp_file=None):
        """Created as Oggify(src, dst, options)
        src is the directory of source files
        dst is the directory for output
        options is an object that has the following attributes:
            options.verbose - boolean
            options.nice - int, see nice(1)
            options.quality - int, 0-10
            options.follow_symlinks - boolean
            options.source_plugin - string, matching an oggify.plugins
            options.output_plugin - string, matching an oggify.plugins
        temp_file is the file that will be written to during encoding
        """
        self._nice = options.nice
        self._quality = options.quality
        self._symlinks = options.follow_symlinks
        self._decoder = utils.load_plugin(options.source_plugin, 'decode')
        self._encoder = utils.load_plugin(options.output_plugin, 'encode')

        if temp_file == None:
            self._temp_file = tempfile.mkstemp()[1]
            atexit.register(os.unlink, self._temp_file)
        else:
            self._temp_file = temp_file

        if options.verbose:
            self._output = sys.stdout
        else:
            self._output = open(os.devnull, 'w')
            atexit.register(self._output.close)

        self._encode, self._reencode, self._limited_purge, self._purge = \
                utils.diff(src, dst,
                        self._decoder.extension, self._encoder.extension,
                        self._symlinks)

        self._encode_k = self._encode.keys()
        self._encode_k.sort()
        self._reencode_k = self._reencode.keys()
        self._reencode_k.sort()

    def encode_file(self, src, dst):
        """Encodes src to dst using the proper decoder and encoder"""
        dir = os.path.dirname(dst)
        if not os.path.exists(dir):
            os.makedirs(dir)

        d_process = self._decoder.decode(src, self._nice)
        e_process = self._encoder.encode(self._temp_file, self._quality,
                self._nice, d_process.stdout, self._output)
        e_process.wait()
        if ((e_process.returncode != 0 
                and e_process.returncode != None) 
            or (d_process.returncode != 0 
                and d_process.returncode != None)):
            raise utils.OggifyError("encode/decode process failure")
        
        shutil.copy(self._temp_file, dst)
        self._encoder.set_tags(dst, self._decoder.get_tags(src))

    def encode(self, act=True):
        """Encodes all detected files needing encoding"""
        for src in self._encode_k:
            dst = self._encode[src]
            del self._encode[src]
            print "Encoding %s to %s" % (src, dst)
            if act:
                self.encode_file(src, dst)

    def reencode(self, act=True):
        """Encodes all detected files needing re-encoding"""
        for src in self._reencode_k:
            dst = self._reencode[src]
            del self._reencode[src]
            if os.path.getmtime(src) > os.path.getmtime(dst):
                print "Re-encoding %s to %s" % (src, dst)
                if act:
                    self.encode_file(src, dst)

    def _rm_list(self, items, act):
        for item in items:
            print "Removing %s" % item
            if act:
                if os.path.isdir(item):
                    os.removedirs(item)
                else:
                    os.unlink(item)

    def purge(self, act=True):
        """Purges all files needing purging"""
        self._rm_list(self._purge, act)

    def clean(self, act=True):
        """Cleans all files needing cleaning"""
        self._rm_list(self._limited_purge, act)
