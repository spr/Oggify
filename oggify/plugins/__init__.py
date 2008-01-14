"""Package containing available oggify plugins.

Files in the package can be called as encoders and decoders for Oggify.
Plugins all implement the Codec class, and are named as the string that
they will be called as on the command-line.
"""

class OggifyPluginException(Exception):
    """Basic Exception for Oggify plugins"""
    pass

class Codec:
    """General parent class of Oggify input/output plugins.

    All children classes need to be named Codec, but the file name should
    be the expected command-line option. IE flac.py, ogg.py, mp3.py
    """
    extension = property(lambda s: "foo", doc="File extension for the codec")
    type = property(lambda s: "foo", doc="""'input' - if only provides decoding
    'output' - if only provides encoding
    'both' - if provides both encoding and decoding
    """)

    def encode(self, file, quality, nice, input, stdout):
        """Prep the encoding process using stdin as the source.
            file - string of the output file name
            quality - A value from 0 to 10 representing the quality of the
                      resulting audio file. See reference plugins for
                      examples.
            nice - Value for nice in this process.
            input - file handle of the pipe with the raw audio
            stdout - file handle for stdout of the process

        Raises OggifyPluginException if called on a Codec that does not
        support encoding.

        Returns subprocess.Popen(stdin=input, stdout=stdout, stderr=STDOUT)
        """
        raise OggifyPluginException("This is not an output plugin")
    def decode(self, file, nice):
        """Prep the decoding process using stdout for the data.
            file - string of the output file name
            nice - Value for nice in this process

        Raises OggifyPluginException if called on a Codec that does not
        support decoding.

        Returns subprocess.Popen(stdout=PIPE)
        """
        raise OggifyPluginException("This is not an input plugin")
    def set_tags(self, file, tags):
        """Set the tags on a file.
            file - string of the filename to set the tags on
            tags - dictionary of tags. (tag_wrapper.Tag)
        """
        raise NotImplementedError("Plugin is a stub")
    def get_tags(self, file):
        """Get the tags from a file.
            file - string of the filename to get the tags from

        Returns tags - dictionary of tags. (tag_wrapper.Tag)
        """
        raise NotImplementedError("Plugin is a stub")
