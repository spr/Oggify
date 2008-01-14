from oggify import plugins
from tag_wrapper import tag
from subprocess import Popen, STDOUT

lame_quality_conversion = [
            '--preset cbr 64',
            '--preset cbr 64',
            '--preset cbr 96',
            '--preset cbr 128',
            '--preset cbr 160',
            '--preset cbr 192',
            '--preset cbr 256',
            '--preset insane',
            '--preset insane',
            '--preset insane',
            '--preset insane',
        ]

class Codec(plugins.Codec):

    extension = property(lambda s: "mp3", doc="mp3")
    type = property(lambda s: "output")

    def encode(self, file, quality, nice, input, stdout):
        actual = lame_quality_conversion[quality]
        args = ["nice", "-n", str(nice), "lame", actual, "-", file]
        return Popen(args, stdin=input, stdout=stdout, stderr=STDOUT)

    def set_tags(self, file, tags):
        mp3_tags = tag(file)
        mp3_tags.update(tags)
        mp3_tags.save()

    def get_tags(self, file):
        return tag(file)
