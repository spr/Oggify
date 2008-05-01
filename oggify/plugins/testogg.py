class FakeSP(object):
    def __init__(self, file):
        self.file = file
        self.returncode = 0
    def wait(self):
        open(self.file, "w").close()

class Codec(object):
    extension = property(lambda s: "ogg")

    def encode(self, file, quality, nice, input, stdout):
        return FakeSP(file)
    def set_tags(self, file, tags):
        pass
