"""Functions for Oggify operation.

This module provides the external functions for using Oggify operations in
your programs.
"""

import os, os.path

def _walk_src_tree(root, src_ext, dst_ext):
    symlink_dirs = []
    dirs = {}
    encode = {}
    org_dir = os.getcwd()
    os.chdir(root)
    for current, subdirs, files in os.walk('.'):
        for subdir in subdirs:
            dirs['/'.join((current[2:], subdir))] = None
            if os.path.islink(subdir):
                symlink_dirs.append(subdir)
        for file in files:
            if file.endswith(src_ext):
                src_fname = '/'.join((current[2:], file))
                dst_fname = '.'.join(src_fname.split('.')[:-1] + [dst_ext])
                encode[src_fname] = dst_fname
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
        dont_walk = []
        for subdir in subdirs:
            if '/'.join((current[2:], subdir)) not in dirs:
                purge.append('/'.join((current[2:], subdir)))
                subdirs.remove(dir)

        for file in files:
            src_eq = '/'.join((current[2:],
                '.'.join(file.split('.')[:-1] + [src_extension])))
            if src_eq in encode:
                if not file.endswith(extension):
                    limited_purge.append('/'.join((current[2:], file)))
                else:
                    reencode[src_eq] = encode[src_eq]
                    del encode[src_eq]
            else:
                purge.append('/'.join((current[2:], file)))
    os.chdir(org_dir)
    return (encode, reencode, limited_purge, purge)

def diff(src_dir, dst_dir, src_ext, dst_ext):
    """diff - Produce action structures for Oggify.
    Arguments:
        src_dir - the root of the source tree
        src_ext - the extension to use for source files, ie: 'flac'
        dst_dir - the root for the output tree
        dst_ext - the extension to use for destination files, ie: 'ogg'
    
    Returns (encode, reencode, limited_purge, purge).
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
    (encode, src_dirs) = _walk_src_tree(src_dir, src_ext, dst_ext)
    return _compare_dst_tree(dst_src, src_ext, encode, src_dirs)
