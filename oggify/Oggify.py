"""oggify.Oggify

This is the worker module of Oggify. All common functions live here.
"""

import os, os.path

def _src_parse(arg, dirname, fnames):
    src_ext, dst_ext, encode, dirs = arg
    for file in fnames:
        if os.path.islink(file):
            continue # TODO: do something with this
        if os.path.isdir(file):
            dirs[('/'.join((dirname[2:], file)))] = None
            continue
        if file.endswith(src_ext):
            src_fname = '/'.join((dirname[2:], file))
            dst_fname = '.'.join(src_fname.split('.')[:-1] + [dst_ext])
            encode[src_fname] = dst_fname

def _walk_src_tree(root, src_ext, dst_ext):
    org_dir = os.getcwd()
    os.chdir(root)
    symlink_dirs = []
    dirs = {}
    encode = {}
    os.path.walk('.', _src_parse, (src_ext, dst_ext, encode, dirs))
    os.chdir(org_dir)
    return (encode, dirs)

def _dst_parse(arg, dirname, fnames):
    src_ext, dst_ext, encode, dirs = arg
    for file in fnames:
        if os.path.islink(file):
            continue # TODO: do I care?
        if (os.path.isdir(file)
                and '/'.join((dirname[2:], file)) not in dirs):
            fname.remove(file)
            continue # TODO: Add to purge!
        dst_fname = '/'.join((dirname[2:], file))
        src_fname_eq = '.'.join(src_fname.split('.')[:-1] + [src_ext])
        if src_fname_eq in encode and not file.endswith(dst_ext):
            # TODO: limited purge!
            pass
        elif src_fname_eq in encode and file.endswith(dst_ext):
            # TODO: reencode
            pass

def _compare_dst_tree(root, dst_ext, encode, dirs, src_ext):
    org_dir = os.getcwd()
    os.chdir(root)
    reencode = {}
    limited_purge = []
    purge = []
    os.path.walk('.', _dst_parse, (src_ext, dst_ext, encode, dirs))
    os.chdir(org_dir)
    return (encode, reencode, limited_purge, purge)

def diff(src_dir, dst_dir, src_ext, dst_ext):
    (encode, src_directories) = _walk_src_tree(src_dir, src_ext, dst_ext)
    return _compare_dst_tree(dst_dir, dst_ext, encode, src_directories, src_ext)
