from oggify import plugins
from tag_wrapper import tag
from subprocess import Popen, STDOUT

class Codec(plugins.Plugin):

    extension = property(lambda: "ogg", doc="ogg")
    type = property(lambda: "output")

    def encode(self, file, quality, input, stdout):
        args = ["oggenc", "-q", quality, "-o", file, "-"]
        return Popen(args, stding=input, stdout=stdout, stderr=STDOUT)

    def set_tags(self, file, tags):
        ogg_tags = tag(file)
        ogg_tags.update(tags)
        ogg_tags.save()

    def get_tags(self, file):
        return tag(file)
