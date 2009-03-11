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
from dircache import listdir
from oggify import utils

version = '2.0.3'

class Oggify(object):
    """Class for the oggify object that does all the work for Oggify"""

    def __init__(self, src, dst, options, decoder, encoder, 
            encode_temp_file=None, decode_temp_file=None):
        """Constructor.

        Keyword arguments:
        src -- the root of the directory tree containing the source files
        dst -- the directory root of the tree that will contain the output files
        options -- an object with the following attributes:
            verbose -- boolean
            nice -- int, see nice(1)
            quality -- int, 0 - 10
            follow_symlinks -- boolean
        decoder -- class like oggify.plugins.Codec that handles the source files
        encoder -- class like oggify.plugins.Codec that handles the output files
        temp_file -- file that will be written to during encoding. If passed the
            caller is expected to delete it when finished.

        The constructor calls oggify.utils.diff to fill datastructures with the
        needed information to perform requested actions.
        """
        self._nice = options.nice
        self._quality = options.quality
        self._symlinks = options.follow_symlinks
        self._decoder = decoder
        self._encoder = encoder

        if encode_temp_file == None:
            tmpsuffix = "." + encoder.extension
            (fd, self._encode_temp_file) = tempfile.mkstemp(suffix=tmpsuffix)
            os.close(fd)
            atexit.register(os.unlink, self._encode_temp_file)
        else:
            self._encode_temp_file = encode_temp_file

        if decode_temp_file == None:
            (fd, self._decode_temp_file) = tempfile.mkstemp(suffix=".wav")
            os.close(fd)
            atexit.register(os.unlink, self._decode_temp_file)
        else:
            self._decode_temp_file = decode_temp_file

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
        """Encodes src to dst using the class's decoder and encoder."""
        dir = os.path.dirname(dst)
        if not os.path.exists(dir):
            os.makedirs(dir)

        returncode = self._decoder.decode(src, self._decode_temp_file,
                self._nice, self._output)
        if (returncode != 0):
            raise utils.OggifyError("Decode process failure: %d" % returncode)
        returncode = self._encoder.encode(self._encode_temp_file,
                self._decode_temp_file, self._quality,
                self._nice, self._output)
        if (returncode != 0):
            raise utils.OggifyError("Encode process failure: %d" % returncode)
        
        shutil.copy(self._encode_temp_file, dst)
        self._encoder.set_tags(dst, self._decoder.get_tags(src))

    def encode(self, act=True):
        """Encode all files detected that qualify.
        
        Encodes all files that only exist in the source tree to
        the destination tree.
        """
        for src in self._encode_k:
            dst = self._encode[src]
            print "Encoding %s to %s" % (src, dst)
            if act:
                self.encode_file(src, dst)

    def reencode(self, act=True):
        """Encode all files detected that qualify for re-encoding.
        
        Encodes all files that exist in both trees where the source has
        been modified more recently than the destination.
        """
        for src in self._reencode_k:
            dst = self._reencode[src]
            if os.path.getmtime(src) > os.path.getmtime(dst):
                print "Re-encoding %s to %s" % (src, dst)
                if act:
                    self.encode_file(src, dst)

    def retag(self, act=True):
        """Re-tag all files detected that qualify.
        
        Re-tags all files that exist in both trees where the source has been
        modified more recently than the destination.
        """
        for src in self._reencode_k:
            dst = self._reencode[src]
            if os.path.getmtime(src) > os.path.getmtime(dst):
                print "Retagging %s with %s" % (dst, src)
                if act:
                    self._encoder.set_tags(dst, self._decoder.get_tags(src))

    def _rm_list(self, items, act):
        for item in items:
            print "Removing %s" % item
            if act:
                if os.path.isdir(item):
                    if len(listdir(item)) > 0:
                        continue
                    os.removedirs(item)
                else:
                    os.unlink(item)

    def purge(self, act=True):
        """Deletes all files and directories detected that qualify.
        
        Files and directories that only exist in the destination tree will be
        deleted. Only non-empty directories are removed.
        """
        self._rm_list(self._purge, act)

    def clean(self, act=True):
        """Deletes all files that qualify for cleaning.
        
        Files that exist in the source tree, but are of a different format than
        is found in the destination are deleted.
        """
        self._rm_list(self._limited_purge, act)
