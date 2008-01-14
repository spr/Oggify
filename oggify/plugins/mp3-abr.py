from oggify import plugins
from tag_wrapper import tag
from subprocess import Popen, STDOUT

lame_quality_conversion = [
            '--preset 64',
            '--preset 64',
            '--preset 96',
            '--preset 128',
            '--preset 160',
            '--preset 192',
            '--preset 256',
            '--preset 320',
            '--preset 320',
            '--preset 320',
            '--preset insane',
        ]

class Codec(plugins.Plugin):

    extension = property(lambda: "mp3", doc="mp3")
    type = property(lambda: "output")

    def encode(self, file, quality, input, stdout):
        actual = lame_quality_conversion[quality]
        args = ["lame", actual, "-", file]
        return Popen(args, stdin=input, stdout=stdout, stderr=STDOUT)

    def set_tags(self, file, tags):
        mp3_tags = tag(file)
        mp3_tags.update(tags)
        mp3_tags.save()

    def get_tags(self, file):
        return tag(file)
