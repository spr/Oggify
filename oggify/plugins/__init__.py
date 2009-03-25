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

"""Package containing available oggify plugins.

Files in the package can be called as encoders and decoders for Oggify.
Plugins all implement a Codec class, and are named as the string that
they will be called as on the command-line.
"""

class Codec:
    """Example class of Oggify input/output plugins.

    All plugins need to have a class named Codec, and the file name should
    be the command-line option. IE flac.py, ogg.py, mp3.py

    What the plugin can be used for is determined by checking for the
    existence of the encode and decode methods.
    """
    extension = property(lambda s: "foo", doc="File extension for the codec")

    def encode(self, dest, source, quality, nice, stdout):
        """Prepare to take a given WAVE file and encode it to the given format
        located at dest.
            dest - string of the output file name
            source - string of the input file name
            quality - A value from 0 to 10 representing the quality of the
                      resulting audio file. See reference plugins for
                      examples.
            nice - Value for nice in this process.

        Function only exists in Codecs that support encoding.

        Returns subprocess.Popen(stdout=stdout, stderr=STDOUT)
        """
        raise NotImplementedError("Example Codec")

    def decode(self, source, dest, nice, stdout):
        """Prepare to take a given file of the format and decode it to a WAVE
        file at dest.
            source - string of the input file name
            dest - string of the output file name
            nice - Value for nice in this process

        Function only exists in Codecs that support decoding.

        Returns subprocess.Popen(stdout=stdout, stderr=STDOUT)
        """
        raise NotImplementedError("Example Codec")
    
    def set_tags(self, file, tags):
        """Set the tags on a file.
            file - string of the filename to set the tags on
            tags - dictionary of tags. (e.g. tag_wrapper.Tag)

        Only needed on encoding Codecs.
        """
        raise NotImplementedError("Example Codec")
    def get_tags(self, file):
        """Get the tags from a file.
            file - string of the filename to get the tags from

        Only needed on decoding Codecs.

        Returns tags - dictionary of tags. (e.g. tag_wrapper.Tag)
        """
        raise NotImplementedError("Example Codec")
