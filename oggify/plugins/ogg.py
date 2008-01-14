from oggify import plugins
from tag_wrapper import tag
from subprocess import Popen, STDOUT

class Codec(plugins.Codec):

    extension = property(lambda s: "ogg", doc="ogg")
    type = property(lambda s: "output")

    def encode(self, file, quality, nice, input, stdout):
        args = ["nice", "-n", str(nice), "oggenc", "-q", str(quality), "-o", file, "-"]
        return Popen(args, stdin=input, stdout=stdout, stderr=STDOUT)

    def set_tags(self, file, tags):
        ogg_tags = tag(file)
        ogg_tags.update(tags)
        ogg_tags.save()

    def get_tags(self, file):
        return tag(file)
