# oggify.plugins.opus - Ogg Opus encoder plugin
# Copyright (c) 2018 Ferdinand Blomqvist
#
# This file was created by copying the mp3.py plugin by Scott Paul 
# Robinson (spr@scottr.org), and modifying it as needed.
#
# This is part of Oggify (http://scottr.org/oggify/)
# 
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.

from oggify import plugins
from tag_wrapper import tag
from subprocess import Popen, STDOUT
import os

opus_quality_conversion = [
            48,
            64,
            80,
            96,
            112,
            128,
            160,
            192,
            224,
            256,
            320,
        ]

class Codec(object):
    """Oggify Ogg Opus Output Plugin.
This plugin encodes files into the Ogg Opus format (.opus) and writes the
correct opus tags.

Quality:
    Quality relates to opusenc(1) --bitrate options as follows:
    -q 0 => --bitrate 48
    -q 1 => --bitrate 64
    -q 2 => --bitrate 80
    -q 3 => --bitrate 96
    -q 4 => --bitrate 112
    -q 5 => --bitrate 128
    -q 6 => --bitrate 160
    -q 7 => --bitrate 192
    -q 8 => --bitrate 224
    -q 9 => --bitrate 256
    -q 10 => --bitrate 320

Requires "opusenc" and "opusdec" to be in $PATH. http://xiph.org"""

    extension = property(lambda s: "opus", doc="opus")

    def decode(self, source, dest, nice, stdout):
        os.unlink(dest)
        args = ["nice", "-n", str(nice), 'opusdec', '--quiet', source, dest]
        p = Popen(args, stdout=stdout, stderr=STDOUT)
        return p

    def encode(self, dest, source, quality, nice, stdout):
        bitrate = opus_quality_conversion[quality]
        args = ["nice", "-n", str(nice), "opusenc", "--bitrate", str(bitrate),
                source, dest]
        p = Popen(args, stdout=stdout, stderr=STDOUT)
        return p

    def set_tags(self, file, tags):
        ogg_tags = tag(file)
        ogg_tags.update(tags)
        ogg_tags.save()

    def get_tags(self, file):
        return tag(file)
