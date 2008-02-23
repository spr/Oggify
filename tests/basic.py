import random, os, re
from os import path
from oggify import Oggify
import unittest

first_src = [
        '/tmp/oggifytest/flac/Guster/Parachute/01 Fall In Two.flac',
        '/tmp/oggifytest/flac/Guster/Parachute/02 Mona Lisa.flac',
        '/tmp/oggifytest/flac/Guster/Parachute/03 Love For Me.flac',
        '/tmp/oggifytest/flac/Guster/Parachute/04 Window.flac',
        '/tmp/oggifytest/flac/Guster/Parachute/05 Eden.flac',
        '/tmp/oggifytest/flac/Guster/Parachute/06 Scars & Stiches.flac',
        '/tmp/oggifytest/flac/Guster/Parachute/07 The Prize.flac',
        '/tmp/oggifytest/flac/Guster/Parachute/08 Dissolve.flac',
        '/tmp/oggifytest/flac/Guster/Parachute/09 Cacoon.flac',
        '/tmp/oggifytest/flac/Guster/Parachute/10 Happy Frappy.flac',
        '/tmp/oggifytest/flac/Guster/Parachute/11 Parachute.flac',
        "/tmp/oggifytest/flac/Jimmy Eat World/Bleed American/01 Bleed American.flac",
        "/tmp/oggifytest/flac/Jimmy Eat World/Bleed American/02 A Praise Chorus.flac",
        "/tmp/oggifytest/flac/Jimmy Eat World/Bleed American/03 The Middle.flac",
        "/tmp/oggifytest/flac/Jimmy Eat World/Bleed American/04 Your House.flac",
        "/tmp/oggifytest/flac/Jimmy Eat World/Bleed American/05 Sweetness.flac",
        "/tmp/oggifytest/flac/Jimmy Eat World/Bleed American/06 Hear You Me.flac",
        "/tmp/oggifytest/flac/Jimmy Eat World/Bleed American/07 If You Don't, Don't.flac",
        "/tmp/oggifytest/flac/Jimmy Eat World/Bleed American/08 Get it Faster.flac",
        "/tmp/oggifytest/flac/Jimmy Eat World/Bleed American/09 Cautioners.flac",
        "/tmp/oggifytest/flac/Jimmy Eat World/Bleed American/10 The Authority Song.flac",
        "/tmp/oggifytest/flac/Jimmy Eat World/Bleed American/11 My Sundown.flac",
        "/tmp/oggifytest/flac/The National/Cherry Tree/01 Wasp Nest.flac",
        "/tmp/oggifytest/flac/The National/Cherry Tree/02 All the Wine.flac",
        "/tmp/oggifytest/flac/The National/Cherry Tree/03 All Dolled-Up in Straps.flac",
        "/tmp/oggifytest/flac/The National/Cherry Tree/04 Cherry Tree.flac",
        "/tmp/oggifytest/flac/The National/Cherry Tree/05 About Today.flac",
        "/tmp/oggifytest/flac/The National/Cherry Tree/06 Murder Me Rachael [Live].flac",
        "/tmp/oggifytest/flac/The National/Cherry Tree/07 A Reasonable Man (I Don't Mind).flac",
        ]

add_src = [
        "/tmp/oggifytest/flac/The Honorary Title/Scream And Light Up The Sky/01 Thin Layer.flac",
        "/tmp/oggifytest/flac/The Honorary Title/Scream And Light Up The Sky/02 Stay Away.flac",
        "/tmp/oggifytest/flac/The Honorary Title/Scream And Light Up The Sky/03 Untouched And Intact.flac",
        "/tmp/oggifytest/flac/The Honorary Title/Scream And Light Up The Sky/04 Stuck At Sea.flac",
        "/tmp/oggifytest/flac/The Honorary Title/Scream And Light Up The Sky/05 Far More.flac",
        "/tmp/oggifytest/flac/The Honorary Title/Scream And Light Up The Sky/06 Radiate.flac",
        "/tmp/oggifytest/flac/The Honorary Title/Scream And Light Up The Sky/07 Along The Way.flac",
        "/tmp/oggifytest/flac/The Honorary Title/Scream And Light Up The Sky/08 Apologize.flac",
        "/tmp/oggifytest/flac/The Honorary Title/Scream And Light Up The Sky/09 The City's Summer.flac",
        "/tmp/oggifytest/flac/The Honorary Title/Scream And Light Up The Sky/10 Only One Week.flac",
        "/tmp/oggifytest/flac/The Honorary Title/Scream And Light Up The Sky/11 Wait Until I'm Gone.flac",
        "/tmp/oggifytest/flac/The Honorary Title/Scream And Light Up The Sky/12 Even If.flac",
        ]


def create_dst_list(src, ext='ogg'):
    dst = []
    for f in src:
        dst.append(re.sub(r'flac', ext, f))
    return dst

def make_files(files):
    for f in files:
        dir = path.dirname(f)
        if not os.path.exists(dir):
            os.makedirs(dir)
        open(f, "w").close()

def del_files(files):
    for f in files:
        if path.exists(f):
            dir = path.dirname(f)
            os.unlink(f)
            try:
                os.removedirs(dir)
            except OSError:
                pass

class AttrHash(object):
    def __init__(self, hash):
        for k,v in hash.items():
            setattr(self, k, v)

class TestOggifyFunctions(unittest.TestCase):

    def setUp(self):
        self.src = list(first_src)
        self.dst = create_dst_list(first_src)
        self.src.sort()
        self.dst.sort()
        self.src_dir = "/tmp/oggifytest/flac"
        self.dst_dir = "/tmp/oggifytest/ogg"
        self.options = AttrHash({
                'verbose': False,
                'nice': 10,
                'quality': 5,
                'follow_symlinks': False,
                'source_plugin': 'flac',
                'output_plugin': 'ogg',
            })
        make_files(self.src)

    def tearDown(self):
        del_files(self.src)
        del_files(self.dst)
        self.src = None
        self.dst = None

    def testencode(self):
        """Validate that on a new dst tree, only encode is present"""
        oggify = Oggify(self.src_dir, self.dst_dir, self.options, '/dev/null')
        sev = oggify._encode.values()
        sev.sort()

        self.assertEqual(oggify._encode_k, self.src)
        self.assertEqual(sev, self.dst)
        self.assertEqual(oggify._reencode, {})
        self.assertEqual(oggify._purge, [])
        self.assertEqual(oggify._limited_purge, [])

    def testnewfileencode(self):
        """Validate that when files are added encode only has new files"""
        self.src += add_src
        make_files(add_src)
        make_files(self.dst)

        add_src.sort()
        add_dst = create_dst_list(add_src)
        add_dst.sort()

        oggify = Oggify(self.src_dir, self.dst_dir, self.options, '/dev/null')
        sev = oggify._encode.values()
        sev.sort()

        self.assertEqual(oggify._encode_k, add_src)
        self.assertEqual(sev, add_dst)

    def testencodewithsymlinks(self):
        pass

    def testreencode(self):
        """Validate that existing files in dst are put in reencode"""
        make_files(self.dst)

        oggify = Oggify(self.src_dir, self.dst_dir, self.options, '/dev/null')
        rev = oggify._reencode.values()
        rev.sort()

        self.assertEqual(oggify._reencode_k, self.src)
        self.assertEqual(rev, self.dst)
    
    def testpurge(self):
        """Validate how purge works"""
        purge = ['/tmp/oggifytest/ogg/bob.ogg',
            '/tmp/oggifytest/ogg/somedirectories']
        self.dst += purge
        make_files(purge)

        oggify = Oggify(self.src_dir, self.dst_dir, self.options, '/dev/null')

        self.assertEqual(oggify._purge, purge)

    def testclean(self):
        """Validate that clean works as expected"""
        clean = [ re.sub(r'mp3', 'ogg', f, count=1)
                for f in create_dst_list(add_src, 'mp3') ]
        self.src += add_src
        make_files(add_src)
        self.dst += clean
        clean.sort()
        make_files(self.dst)

        oggify = Oggify(self.src_dir, self.dst_dir, self.options, '/dev/null')
        ca = oggify._limited_purge
        ca.sort()

        self.assertEqual(ca, clean)

if __name__ == '__main__':
    unittest.main()
