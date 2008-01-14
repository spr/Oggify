from oggify import plugins
from tag_wrapper import tag
from subprocess import Popen, PIPE

class Codec(plugins.Codec):

    extension = property(lambda s: "flac", doc="flac")
    type = property(lambda s: "input")

    def decode(self, file, nice):
        args = ["nice", "-n", nice, "flac", "--totally-silent", "-d", "-c", "file"]
        return Popen(args, stdout=PIPE)

    def set_tags(self, file, tags):
        flac_tag = tag(file)
        flac_tag.update(tags)
        flac_tag.save()

    def get_tags(self, file):
        return tag(file)
