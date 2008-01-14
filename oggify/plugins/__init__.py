class OggifyPluginException(Exception):
    pass

class Plugin:
    extension = property(lambda: "foo", doc="File extension")
    type = property(lambda: "foo", doc="'input'/'output'/'both' depending")

    def encode(self, file, input):
        """returns a subprocess.Popen object with stdin=input,
        stdout=PIPE, stderr=PIPE.
        """
        raise OggifyPluginException("This is not an output plugin")
    def decode(self, file):
        """encode returns a subprocess.Popen object with stdout=PIPE,
        stderr=PIPE. The process should route the decoded result through
        stdout.
        """
        raise OggifyPluginException("This is not an input plugin")
    def set_tags(self, file, tags):
        raise NotImplementedError("Plugin is a stub")
    def get_tags(self, file, tags):
        raise NotImplementedError("Plugin is a stub")
