import subprocess

class Codec(object):
    extension = property(lambda s: "flac")

    def decode(self, source, dest, nice, stdout):
        return 0

    def get_tags(self, file):
        return None
