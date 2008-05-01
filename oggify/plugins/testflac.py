class FakeSP(object):
    def __init__(self):
        self.stdout = None
        self.returncode = 0

class Codec(object):
    extension = property(lambda s: "flac")

    def decode(self, file, nice):
        return FakeSP()
    def get_tags(self, file):
        return None
