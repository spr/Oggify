# Copyright (c) 2008 Scott Paul Robertson (spr@scottr.org)
#
# tag_wrapper is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version
# 
# tag_wrapper is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with tag_wrapper; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA

from tag_wrapper import dictionary_reverse, Tag, TagException
from mutagen.id3 import ID3
from mutagen import id3

encodings = {
        'iso-8859-1':   0,
        'utf-16':       1,
        'utf-16be':     2,
        'utf-8':        3,
}

id3_frame_mapping = {
        #'APIC': 'cover image', # Support for images to come
        'TALB': 'album',
        'TBPM': 'bpm',
        'TCOM': 'composer',
        'TCON': 'genre',
        'TCOP': 'copyright',
        'TDRC': 'date',
        'TENC': 'encoder',
        'TEXT': 'lyricist',
        'TLEN': 'length',
        'TPE1': 'artist',
        'TPE2': 'album artist',
        'TPE3': 'conductor',
        'TPOS': 'discnumber',   # x/total
        'TRCK': 'tracknumber',  # x/total
        'TSSE': 'encoder',
        'TIT1': 'grouping',
        'TIT2': 'title',
}

norm_frame_mapping = dictionary_reverse(id3_frame_mapping)

def build_comm_key(key, lang='eng'):
    """Builds key for a COMM tag as found in mutagen.id3.ID3"""
    return unicode(''.join(('COMM:', key, ":'", lang, "'")))

class ID3Tag(Tag):
    """The Tag implementation for ID3 tags"""

    def __init__(self, tag, lang='eng', encoding=encodings['utf-8']):
        super(ID3Tag, self).__init__(tag)
        self.lang = lang
        if encoding in encodings:
            self.encoding = encodings[encoding]
        elif encoding <= 3 and encoding >= 0:
            self.encoding = encoding
        else:
            raise TagException('Encoding %s not supported by ID3' % encoding)

    def _get_new_key(self, key):
        """This returns the key that mutagen.id3.ID3 uses given a "normal"
        value.
        """
        # Note: some keys have an appended ':'. This is bad
        new_key = ''
        if key in norm_frame_mapping:
            new_key = norm_frame_mapping[key]
        # description is synonymous with comment
        elif key == 'comment' or key == 'description':
            new_key = build_comm_key('', self.lang)
        else:
            new_key = build_comm_key(key, self.lang)
        return new_key

    def __getitem__(self, key):
        """ __getitem__: artist = tag['artist']
        Returns a list of values
        """
        id3_tag = self._tag[self._get_new_key(key)]
        return id3_tag.text

    def __setitem__(self, key, value):
        """__setitem__: tag['artist'] = "Guster"
        If a tag supports multiple values, the user must put vales into
        a list themselves. If the tag already exists we overwrite the data.
        """
        # Tag is a supported frame
        nkey = self._get_new_key(key)
        if key in norm_frame_mapping:
            # FYI: Adding support for non-text frames will require more
            # logic here.
            tag_class = getattr(id3, nkey)
            self._tag[nkey] = tag_class(encoding=self.encoding, text=value)
        # Tag is a comment
        else:
            if key == 'comment' or key == 'description':
                desc = ''
            else:
                desc = key
            self._tag[nkey] = id3.COMM(encoding=self.encoding, lang=self.lang,
                        description=desc, text=value)

    def __delitem__(self, key):
        del(self._tag[self._get_new_key(key)])

    def __contains__(self, item):
        return (self._get_new_key(item) in self._tag)

    def keys(self):
        keys = []
        for id3_key in self._tag:
            if id3_key in id3_frame_mapping:
                keys.append(id3_frame_mapping[id3_key])
            elif id3_key.startswith('COMM:'):
                s = id3_key.split(':')[1]
                if s == '':
                    keys.append('comment')
                else:
                    keys.append(s)
        return keys
