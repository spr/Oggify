from oggify import plugins
from tag_wrapper import tag
from subprocess import Popen, PIPE

class Plugin(plugins.Plugin):

    extension = property(lambda: "flac", doc="flac")
    type = property(lambda: "input")

    def decode(self, file):
        args = ["flac", "--totally-silent", "-d", "-c", "file"]
        return Popen(args, stdout=PIPE)

    def set_tags(self, file, tags):
        flac_tag = tag(file)
        flac_tag.update(tags)
        flac_tag.save()

    def get_tags(self, file):
        return tag(file)
