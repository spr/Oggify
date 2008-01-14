class OggifyPluginException(Exception):
    pass

class Plugin:
    """Plugin - General parent class of Oggify input/output plugins.

    All children classes need to be named Plugin, but the file name should
    be the expected command-line option. IE flac.py, ogg.py, mp3.py
    """
    extension = property(lambda: "foo", doc="File extension")
    type = property(lambda: "foo", doc="'input'/'output'/'both' depending")

    def encode(self, file, quality, input, stdout, stderr):
        """
        Arguments:
            file - string of the output file name
            quality - A value from 0 to 10 representing the quality of the
                      resulting audio file. See reference plugins for
                      examples.
            input - file handle of the pipe with the raw audio
            stdout - file handle for stdout of the process
            stderr - file handle for stderr of the process

        Returns:
            subprocess.Popen(stdin=input, stdout=stdout,
                stderr=STDOUT)
        """
        raise OggifyPluginException("This is not an output plugin")
    def decode(self, file):
        """
        Arguments:
            file - string of the output file name

        Returns:
            subprocess.Popen(stdout=PIPE)
        """
        raise OggifyPluginException("This is not an input plugin")
    def set_tags(self, file, tags):
        """
        Arguments:
            file - string of the filename to set the tags on
            tags - dictionary of tags. (tag_wrapper.Tag)
        """
        raise NotImplementedError("Plugin is a stub")
    def get_tags(self, file):
        """
        Arguments:
            file - string of the filename to get the tags from

        Returns:
            tags - dictionary of tags. (tag_wrapper.Tag)
        """
        raise NotImplementedError("Plugin is a stub")
