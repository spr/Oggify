class Fake(object):
    def wait(self):
        return 0

class Codec(object):
    extension = property(lambda s: "flac")

    def decode(self, source, dest, nice, stdout):
        return Fake()

    def get_tags(self, file):
        return None
