# oggify.plugins.mp3 - MP3 - VBR encoder plugin for Oggify
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
import os

lame_quality_conversion = [
            ['-V', '9'],
            ['-V', '8'],
            ['-V', '7'],
            ['-V', '6'],
            ['-V', '5'],
            ['-V', '4'],
            ['-V', '3'],
            ['-V', '2'],
            ['-V', '1'],
            ['-V', '0'],
            ['-b', '320'],
        ]

class Codec(object):
    """Oggify MP3 Output Plugin, VBR encoding.
This plugin encodes files as MP3's using VBR encoding and writes the corrent ID3v2.4 and ID3v1.1 tags.

Quality:
    Quality relates to lame(1) -V options, but in reverse:
    -q 0 => -V 9
    -q 5 => -V 4
    -q 7 => -V 2
    -q 10 => -b 320

Requires "lame" to be in $PATH. http://lame.sf.net"""

    extension = property(lambda s: "mp3", doc="mp3")

    def decode(self, source, dest, nice, stdout):
        os.unlink(dest)
        args = ['nice', '-n', str(nice), 'lame', '--decode', '--silent',
                source, dest]
        p = Popen(args, stdout=stdout, stderr=STDOUT)
        return p

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
