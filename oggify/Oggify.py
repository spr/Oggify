# oggify.Oggify - General Library for Oggify
# Copyright (c) 2008 Scott Paul Robertson (spr@scottr.org)
#
# This is part of Oggify (http://scottr.org/oggify/)
#
# Oggify is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version
# 
# Oggify is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with Oggify; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA

"""Functions for Oggify operation.

This module provides the external functions for using Oggify operations in
your programs.
"""

import os, os.path, sys, re, tempfile, shutil

class OggifyError(StandardError):
    """Runtime error for Oggify"""
    pass

def _process_walk(current, subdirs, files, encode, dirs, sym, src_ext, dst_ext):
    for subdir in subdirs:
        dirs[os.path.join(current, subdir)] = None
        if os.path.islink(subdir):
            sym.append(subdir)
    for file in files:
        if file.endswith(src_ext):
            src_fname = os.path.join(current, file)
            dst_fname = '.'.join(src_fname.split('.')[:-1] + [dst_ext])
            encode[src_fname] = dst_fname

def _walk_src_tree(root, src_ext, dst_ext, follow_symlinks=False):
    sym = []
    dirs = {}
    encode = {}
    org_dir = os.getcwd()
    os.chdir(root)
    for current, subdirs, files in os.walk('.'):
        _process_walk(current[2:], subdirs, files, encode, dirs,
                sym, src_ext, dst_ext)
    if follow_symlinks:
        for dir in sym:
            for current, subdirs, files in os.walk(dir):
                _process_walk(current, subdirs, files, encode, dirs, sym,
                        src_ext, dst_ext)
    os.chdir(org_dir)
    return (encode, dirs)

def _compare_dst_tree(root, src_ext, dst_ext, encode, dirs):
    reencode = {}
    limited_purge = []
    purge = []
    if not os.path.exists(root):
        return (encode, {}, [], [])
    org_dir = os.getcwd()
    os.chdir(root)
    for current, subdirs, files in os.walk('.'):
        for subdir in subdirs:
            if current != '.':
                test = '/'.join((current[2:], subdir))
            else:
                test = subdir
            if test not in dirs:
                purge.append(os.path.join(current[2:], subdir))
                subdirs.remove(subdir)

        for file in files:
            src_eq = os.path.join(current[2:],
                '.'.join(file.split('.')[:-1] + [src_ext]))
            if src_eq in encode:
                if not file.endswith(dst_ext):
                    limited_purge.append(os.path.join(current[2:], file))
                else:
                    reencode[src_eq] = encode[src_eq]
                    del encode[src_eq]
            else:
                purge.append(os.path.join(current[2:], file))
    os.chdir(org_dir)
    return (encode, reencode, limited_purge, purge)

def _adjust_filenames(src_dir, dst_dir, files):
    n_files = {}
    for k,v in files.items():
        n_files[os.path.join(src_dir, k)] = os.path.join(dst_dir, v)
    return n_files

def _adjust_list_filesnames(dir, files):
    return [os.path.join(dir, f) for f in files]

def diff(src_dir, dst_dir, src_ext, dst_ext, follow_symlinks=False):
    """Produce action structures for Oggify.
        src_dir - the root of the source tree
        src_ext - the extension to use for source files, ie: 'flac'
        dst_dir - the root for the output tree
        dst_ext - the extension to use for destination files, ie: 'ogg'
    
    Returns (encode, reencode, limited_purge, purge):
        encode - A dictionary of "source file" => "destination file" where
            source file is all of the files in src_dir with src_ext that do
            not exist in dst_dir.
        reencode - A dictionary of "source file" => "destination file" where
            source file is all of the files in src_dir with src_ext that do
            exist in dst_dir with dst_ext
        limited_purge - A list of files in dst_dir that are in src_dir with
            src_ext, but do not have dst_ext.
        purge - A list of files and directories that do not exist in src_dir
            with src_ext. Any non-src_ext files will wind up here.
    """
    (encode, src_dirs) = _walk_src_tree(src_dir, src_ext, dst_ext, 
            follow_symlinks)
    (encode, reencode, limited_purge, purge) =  _compare_dst_tree(dst_dir,
            src_ext, dst_ext, encode, src_dirs)
    encode = _adjust_filenames(src_dir, dst_dir, encode)
    reencode = _adjust_filenames(src_dir, dst_dir, reencode)
    purge = _adjust_list_filesnames(dst_dir, purge)
    limited_purge = _adjust_list_filesnames(dst_dir, limited_purge)
    return (encode, reencode, limited_purge, purge)

def list_plugins(type=None):
    """List the installed oggify plugins.
        type - 'encode' or 'decode' or None.

    Returns a list of strings representing the installed oggify plugins
    of type. (None returns all plugins)
    """
    from oggify import plugins
    plugin_dir = plugins.__path__[0]
    contents = os.listdir(plugin_dir)
    plugins = []
    for filename in contents:
        if re.search(r'\.py$', filename) and filename != '__init__.py':
            plugin = filename.split('.')[0]
            mod = __import__('.'.join(('oggify', 'plugins', plugin)),
                    fromlist=[''])
            if type == None or hasattr(mod.Codec, type):
                plugins.append(plugin)
    return plugins

def load_plugin(plugin, type):
    """Load an oggify plugin by string.
        plugin - string of the plugin
        type - "encode" or "decode"

    Raises an OggifyError if the plugin requested does not support the type.

    Returns oggify.plugins.Codec object of the plugin.
    """
    try:
        mod = __import__('.'.join(('oggify', 'plugins', plugin)),
                fromlist=[''])
    except ImportError:
        raise OggifyError("%s plugin does not exist" % plugin)

    if not hasattr(mod.Codec, type):
        raise OggifyError("%s is not a %s codec!" % (plugin, type))

    codec = mod.Codec()
    return codec

def process_file(decoder, encoder, src_file, dst_file, quality,
        nice=10, verbose=False, temp_file=None):
    """Encode a file using the correct source format file.
        decoder - oggify.plugins.Codec, type 'input'
        encoder - oggfiy.plugins.Codec, type 'output'
        src_file - string, source file (from oggify.Oggify.diff)
        dst_file - string, destination file (from oggify.Oggify.diff)
        quality - int, 0 - 10. Quality to use for encoding (see oggenc(1))
        nice - int, -20 - 19. Nice value to use for processing.
        verbose - boolean, Determines how much is printed to sys.stdout
        temp_file - string, filename to use while encoding to handle 
                    interrupts

    Raises an OggifyError if the decode or encode process does not return
    successfully.

    This properly calls the Codec objects to take src_file to dst_file.
    """

    if verbose:
        output = sys.stdout
    else:
        output = open(os.devnull, 'w')

    dir = os.path.dirname(dst_file)
    if not os.path.exists(dir):
        os.makedirs(dir)
    decoder_process = decoder.decode(src_file, nice)
    unlink = False
    if temp_file == None:
        temp_file = tempfile.mkstemp()[1]
        unlink = True
    encoder_process = encoder.encode(temp_file, quality, nice,
            decoder_process.stdout, output)
    encoder_process.wait()
    if ((encoder_process.returncode != 0 
                and encoder_process.returncode != None)
            or (decoder_process.returncode != 0
                and decoder_process.returncode != None)):
        raise OggifyError("Encode/decode process failure")
    shutil.copy(temp_file, dst_file)
    if unlink:
        os.unlink(temp_file)
    encoder.set_tags(dst_file, decoder.get_tags(src_file))
    if not verbose:
        output.close()

def encode(decoder, encoder, files, options, temp_file=None,
        cond=lambda x, y: True):
    sorted = files.keys()
    sorted.sort()
    for src in sorted:
        if cond(src, files[src]):
            print "Encoding %s to %s" % (src, files[src])
            process_file(decoder, encoder, src, files[src],
                    options.quality, options.nice, options.verbose,
                    temp_file)

def purge(items, act=False):
    if not act:
        return
    for item in items:
        print "Removing %s" % item
        if os.path.isdir(item):
            os.removedirs(item)
        else:
            os.unlink(item)
