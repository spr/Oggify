# Copyright (c) 2007 Scott Paul Robertson (spr@scottr.org)
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
from mutagen.mp4 import MP4

mp4_frame_mapping = {
        'trkn':     'tracknumber',  # tuple (x, total)
        'tvsh':     'show',
        'disk':     'discnumber',   # tuple (x, total)
        '\xa9cmt':  'comment',
        '\xa9wrt':  'composer',
        'purd':     'purchased',    # TODO: figure this out
        '\xa9alb':  'album',
        'tmpo':     'bpm',
        '\xa9grp':  'grouping',
        '\xa9day':  'date',         # TODO: figure this out
        'aART':     'artist',
        'cpil':     'compilation',  # boolean
        'apID':     'apple id',
        #'covr':     'album cover', TODO
        'cprt':     'copyright',
        '\xa9ART':  'artist',
        '\xa9nam':  'title',
        'pgap':     'gapless',      #  boolean
        '\xa9gen':  'genre',
}

norm_frame_mapping = dictionary_reverse(mp4_frame_mapping)

class MP4Tag(Tag):
    """The Tag implementation for MP4 (iTunes) tags"""

    def _get_mp4_key(self, key):
        if key in norm_frame_mapping:
            return norm_frame_mapping[key]
        else:
            return key
    
    def __getitem__(self, key):
        """__getitem__: artist = tag['artist']
        If a tag has multiple values, we return a list
        """
        mp4_tag = self._tag[self._get_mp4_key(key)]
        return mp4_tag

    def __setitem__(self, key, value):
        # date == year in most cases
        if key == 'year':
            key = 'date'
        
        self._tag[self._get_mp4_key(key)] = value

    def __delitem__(self, key):
        del(self._tag[self._get_mp4_key(key)])

    def __contains__(self, item):
        return (self._get_mp4_key(key) in self._tag)

    def keys(self):
        keys = []
        for mp4_key in self._tag.keys():
            if mp4_key in mp4_frame_mapping:
                keys.append(mp4_frame_mapping[mp4_key])
            else:
                keys.append(mp4_key)
        return keys
