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

import mutagen

class Tag(object):
    """Abstract class for tag implementations. Provides the general basics
    that all tags need.
    self._tag -> the original mutagen tag
    """
    def __init__(self, tag):
        self._tag = tag

    def save(self):
        """Saves tag out to disk."""
        self._tag.save()

    def __getitem__(self, key):
        return self._tag[key]

    def __setitem__(self, key, value):
        self._tag[key] = value

    def __contains__(self, key):
        return (key in self._tag)

    def __len__(self):
        return len(self._tag)

    def __delitem__(self, key):
        del(self._tag[key])

    def keys(self):
        return self._tag.keys()

    def has_key(self, k):
        return (k in self)

    def values(self):
        values = []
        for key in self.keys():
            values.append(self[key])
        return values

    def items(self):
        return zip(self.keys(), self.values())

    # TODO: Implement iterator
    def iteritems(self):
        pass

    def iterkeys(self):
        pass

    def itervalues(self):
        pass

    def __iter__(self):
        self.iterkeys()

    def get(self, k, default=None):
        if k in self:
            return self[k]
        else:
            return default

    def copy(self):
        dict = {}
        for k,v in self.items():
            dict[k] = v
        return dict

    def clear(self):
        for k in self.keys():
            del(self[k])

    def update(self, other=None, **kwargs):
        if other:
            for (k, v) in other.items():
                self[k] = v
        if kwargs:
            for (k, v) in kwargs.items():
                self[k] = v

    def setdefault(self, k, default=None):
        if k in self:
            return self[k]
        else:
            self[k] = default
            return default

    def pop(self, key, default=None):
        try:
            ret = self[key]
            del(self[key])
        except KeyError:
            if default:
                ret = default
            else:
                raise KeyError('%s' % key)
        return ret

    def popitem(self):
        if len(self):
            return self.pop(self.keys()[0])
        else:
            raise KeyError()
    filename = property(lambda self: self._tag.filename)

class TagException(Exception):
    """tag_wrapper general exception."""
    pass

def dictionary_reverse(org_dict):
    """Turns a dict of k -> v to v -> k"""
    new_dict = {}
    for k,v in org_dict.items():
        new_dict[v] = k
    return new_dict

from tag_wrapper.mp3 import ID3Tag
from tag_wrapper.mp4 import MP4Tag

def tag(filename, lang='eng', encoding='utf-8'):
    """This function front-ends the various implementors of the Tag class.
    You pass it a filename, and it returns an object of class TagDict for
    that file.
    """
    tag = mutagen.File(filename)
    if tag == None:
        raise TagException('%s does not contain a supported tag format.'
                % filename)
    elif type(tag) == mutagen.mp3.MP3:
        return ID3Tag(tag, lang, encoding)
    elif type(tag) == mutagen.mp4.MP4:
        return MP4Tag(tag)
    else:
        return Tag(tag)
