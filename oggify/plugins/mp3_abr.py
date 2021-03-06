# oggify.plugins.mp3_abr - MP3 - ABR encoder plugin for Oggify
# Copyright (c) 2008 Scott Paul Robertson (spr@scottr.org)
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

lame_quality_conversion = [
            ['--abr', '56', '-mm'],
            ['--preset', '64'],
            ['--preset', '96'],
            ['--preset', '128'],
            ['--preset', '160'],
            ['--preset', '192'],
            ['--preset', '256'],
            ['--preset', '320'],
            ['--preset', '320'],
            ['--preset', '320'],
            ['--preset', 'insane'],
        ]

class Codec(object):
    """Oggify MP3 Output Plugin, ABR encoding.
This plugin encodes files as MP3's using ABR encoding and writes the corrent ID3v2.4 and ID3v1.1 tags.

Quality:
    Quality relates to lame(1) options, as follows:
    ------------------------------
    | value |   lame(1) option   |
    |   0   |  --abr 56 -mm      | (mono, voice only)
    |   1   |  --preset 64       |
    |   2   |  --preset 96       |
    |   3   |  --preset 128      |
    |   4   |  --preset 160      |
    |   5   |  --preset 192      |
    |   6   |  --preset 256      |
    |  7-9  |  --preset 320      |
    |  10   |  --preset insane   |
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
