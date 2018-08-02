Oggify v2.0
===========

Oggify is a tool designed to ease the conversion of audio files from lossless
formats to lossy formats. It is designed to work on a directory of lossless
files and then creates a similar directory structure, and converts the lossless
files to lossy files. Subsequent runs will only cause new files to be encoded,
if no other options are passed.

Prerequisites
-------------

 * [Python](http://www.python.org)
 * [FLAC](http://flac.sourceforge.net) - For FLAC Support
 * [LAME](http://lame.sourceforge.net) - For MP3 Support
 * [Ogg Vorbis](http://www.vorbis.com) - For Ogg Support
 * [Opus](http://www.opus-codec.org) - For Opus Support
 * [Mutagen](http://code.google.com/p/mutagen/) - For Tag Support

OS X users can use MP3 out of the box, as well ALAC, and M4A. At a minimum OS X users just need to install Mutagen.

All formats supported by Oggify:

 * FLAC
 * ALAC (OS X only)
 * MP3
 * OGG
 * OPUS
 * M4A/MP4 (OS X only)

Example
-------

A common usage follows:

You have your audio files stored in a meticulously organized directory,
`~/music/flacs`. You want to convert these to MP3 so they will work on the music
player you got for Christmas. So you run:

    oggify -o mp3 ~/music/flacs ~/music/mp3s

Which then mirrors your directory, but with MP3 files instead of FLAC.

You later get some new music, and rip it into `~/music/flacs`. You then run:

    oggify -o mp3 ~/music/flacs ~/music/mp3s

You discover a file has been ripped badly and you re-rip it. Now you want to
get that update in your MP3 files. So you run:

    oggify -o mp3 -r ~/music/flacs ~/music/mp3s

You've downloaded some MP3's and are afraid that the RIAA is coming to get you,
so you want your MP3 directory to be identical to your FLAC directory. You run:

    oggify -o mp3 -P ~/music/flacs ~/music/mp3s

You decide you want things to be in the Ogg Vorbis since you're a true FOSS
person. You run:

    oggify ~/music/flacs ~/music/ogg

You decide that the oggenc's quality level of 5 just isn't enough. So you
delete your ogg directory and run:

    oggify -q 8 ~/music/flacs ~/music/ogg

Further switches can be found by running oggify -h.

Ignoring parts of the source directory tree
-------------------------------------------

By default Oggify ignores subtrees of the source directory tree whose root
contains a file named '.oggifyignore'. Thus any part of the source directory
tree can be ignored by adding a file named '.oggifyignore' in the directory
that should be ignored. Oggify will ignore this directory and all its
subdirectories. This behaviour can be changed with the \-\-no-ignore-subtrees
option.

Submitting Plugins
------------------

The programmer can simply write a plugin look at the class
oggify.plugins.Plugin as an example (found in oggify/plugins/__init__.py).

The non-programmer can email the author certain information:

For a new source format:

 1. A command-line that suppresses output and decodes the file to stdout.

For a new destination format:

 1. A command-line that encodes a file from stdin

 2. A way to relate a quality switch on the scale of 0-10 to something
    meaningful for this program. With VBR based MP3's with lame this is: 5 =>
    --preset medium


Installing From Source
----------------------

 * Be sure to run `git submodule update --init`
 * Install the prerequisites.
 * `sudo python setup.py install`


Reporting Bugs
--------------

Report issues via github. Please run oggify with -v and send the output starting with the previous "encoding ... to ..." line and down through the Python error.

Legal Stuff
-----------

Oggify is Copyright 2008-2013 Scott Paul Robertson and is licensed under the
GNU General Public License, version 2.
