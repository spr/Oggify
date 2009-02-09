class Codec(object):
    extension = property(lambda s: "ogg")

    def encode(self, dest, source, quality, nice, stdout):
        return 0
    def set_tags(self, file, tags):
        open(file, "w").close()
