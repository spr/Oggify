from oggify import plugins
from tag_wrapper import tag
from subprocess import Popen, STDOUT

lame_quality_conversion = {
        'cbr': [
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
        ],
        'vbr': [
            '--preset medium',
            '--preset medium',
            '--preset medium',
            '--preset standard',
            '--preset standard',
            '--preset standard',
            '--preset extreme',
            '--preset extreme',
            '--preset extreme',
            '--preset extreme',
            '--preset insane',
        ],
        'abr': [
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
}

class Plugin(plugins.Plugin):

    extension = property(lambda: "mp3", doc="mp3")
    type = property(lambda: "output")

    def encode(self, file, quality, input, stdout, stderr):
        actual = lame_quality_conversion['vbr'][quality]
        args = ["lame", actual, "-", file]
        return Popen(args, stdin=input, stdout=stdout, stderr=STDOUT)

    def set_tags(self, file, tags):
        mp3_tags = tag(file)
        mp3_tags.update(tags)
        mp3_tags.save()

    def get_tags(self, file):
        return tag(file)
