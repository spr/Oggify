# oggify.plugins.alac - Apple Lossless plugin for Oggify
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

import tempfile, os, os.path
from tag_wrapper import tag
from subprocess import Popen, PIPE, STDOUT

class Codec(object):
    """Oggify Apple Lossless Plugin. (OS X Only)
Decodes and encodes Apple Lossless files (alac). Looks for .m4a files.

Requires Leopard (10.5) or afconvert to have been manually built."""

    extension = property(lambda s: "m4a", doc="m4a")

    def decode(self, file, nice):
        args = ["oggify_wrapper", "-d", "-s", ".wav", "--", "nice", "-n",
                str(nice), "afconvert", "-f", "WAVE", "-d", "LEI32@441000", file, "%o"]
        return Popen(args, stdout=PIPE)

    def encode(self, file, quality, nice, input, stdout):
        os.unlink(file)
        args = ["oggify_wrapper", "-e", "-s", ".wav", "--", "nice", "-n",
                str(nice), "afconvert", "-f", "m4af", "-d", "alac", "%i", file]
        return Popen(args, stdin=input, stdout=stdout, stderr=STDOUT)

    def get_tags(self, file):
        return tag(file)

    def set_tags(self, file, tags):
        alac_tag = tag(file)
        alac_tag.update(tags)
        alac_tag.save()
