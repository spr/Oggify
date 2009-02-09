# oggify.plugins.ogg - Ogg Vorbis encoder plugin
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

from oggify import plugins
from tag_wrapper import tag
from subprocess import Popen, STDOUT

class Codec(object):
    """Oggify Ogg Vorbis Output Plugin. (default)
This plugin encodes files into the Ogg Vorbis format (.ogg) and writes the
correct vorbis tags.

Quality:
    Follows with the oggenc(1) -q option. Only integer values between 0 and 10
    are premitted, unlike oggenc(1).

Requires "oggenc" to be in $PATH. http://xiph.org"""

    extension = property(lambda s: "ogg", doc="ogg")

    def encode(self, dest, source, quality, nice, stdout):
        args = ["nice", "-n", str(nice), "oggenc", "-q", str(quality),
                "-o", file, source]
        p = Popen(args, stdout=stdout, stderr=STDOUT)
        return p.wait()

    def set_tags(self, file, tags):
        ogg_tags = tag(file)
        ogg_tags.update(tags)
        ogg_tags.save()

    def get_tags(self, file):
        return tag(file)
