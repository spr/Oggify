class Fake(object):
    def wait(self):
        return 0

class Codec(object):
    extension = property(lambda s: "ogg")

    def encode(self, dest, source, quality, nice, stdout):
        return Fake()

    def set_tags(self, file, tags):
        open(file, "w").close()
