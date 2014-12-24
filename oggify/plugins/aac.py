# oggify.plugins.flac - AAC encoder plugin for Oggify
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

import tempfile, os, os.path
from tag_wrapper import tag
from subprocess import Popen, PIPE, STDOUT

quality_conversion = [
        ['-b', '64000'],
        ['-b', '96000'],
        ['-b', '128000'],
        ['-b', '160000'],
        ['-b', '192000'],
        ['-b', '192000'],
        ['-b', '224000'],
        ['-b', '256000'],
        ['-b', '256000'],
        ['-b', '256000'],
        ['-b', '320000'],
    ]

class Codec(object):
    """Oggify AAC (MPEG-2 Part 7) Encoder Plugin. (OS X Onlu)
Encodes AAC files using afconvert. Looks for .m4a files. VBR encoding.

Quality:
    Quality values relate to bitrate as follows:
    --------------------
    | value |  bitrate |
    |   0   |  64000   |
    |   1   |  96000   |
    |   2   |  128000  |
    |   3   |  160000  |
    |  4-5  |  192000  |
    |   6   |  224000  |
    |  7-9  |  256000  |
    |  10   |  320000  |
    --------------------

Requires Leopard (10.5) or afconvert to have been manually built."""

    extension = property(lambda s: "m4a", doc="m4a")

    def encode(self, dest, source, quality, nice, stdout):
        os.unlink(dest)
        quality = quality_conversion[quality]
        args = ["nice", "-n", str(nice), "afconvert", "-f", "m4af", "-d",
                "aac ", "-s", "2"] + quality + [source, dest]
        p =  Popen(args, stdout=stdout, stderr=STDOUT)
        return p

    def get_tags(self, file, tags):
        return tag(file)

    def set_tags(self, file, tags):
        aac_tag = tag(file)
        aac_tag.update(tags)
        aac_tag.save()
