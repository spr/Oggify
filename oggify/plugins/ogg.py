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

class Codec(plugins.Codec):

    extension = property(lambda s: "ogg", doc="ogg")
    type = property(lambda s: "output")

    def encode(self, file, quality, nice, input, stdout):
        args = ["nice", "-n", str(nice), "oggenc", "-q", str(quality), "-o", file, "-"]
        return Popen(args, stdin=input, stdout=stdout, stderr=STDOUT)

    def set_tags(self, file, tags):
        ogg_tags = tag(file)
        ogg_tags.update(tags)
        ogg_tags.save()

    def get_tags(self, file):
        return tag(file)
