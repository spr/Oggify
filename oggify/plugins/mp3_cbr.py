# oggify.plugins.mp3_cbr - MP3 - CBR encoder plugin for Oggify
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

lame_quality_conversion = [
            ['-b', '48'],
            ['-b', '64'],
            ['-b', '80'],
            ['-b', '96'],
            ['-b', '112'],
            ['-b', '128'],
            ['-b', '160'],
            ['-b', '192'],
            ['-b', '224'],
            ['-b', '256'],
            ['-b', '320'],
        ]

class Codec(object):
    """Oggify MP3 Output Plugin, CBR encoding.
This plugin encodes files as MP3's using CBR encoding and writes the corrent ID3v2.4 and ID3v1.1 tags.

Quality:
    Quality relates to lame(1) options, as follows:
    ------------------------------
    | value |   lame(1) option   |
    |   0   |  -b 48             |
    |   1   |  -b 64             |
    |   2   |  -b 80             |
    |   3   |  -b 96             |
    |   4   |  -b 112            |
    |   5   |  -b 128            |
    |   6   |  -b 160            |
    |   7   |  -b 192            |
    |   8   |  -b 224            |
    |   9   |  -b 256            |
    |  10   |  -b 320            |
    ------------------------------

Requires "lame" to be in $PATH. http://lame.sf.net"""

    extension = property(lambda s: "mp3", doc="mp3")

    def encode(self, dest, source, quality, nice, stdout):
        actual = lame_quality_conversion[quality]
        args = ["nice", "-n", str(nice), "lame"] + actual + [source, dest]
        p = Popen(args, stdout=stdout, stderr=STDOUT)
        return p

    def set_tags(self, file, tags):
        mp3_tags = tag(file)
        mp3_tags.update(tags)
        mp3_tags.save()

    def get_tags(self, file):
        return tag(file)
