"""oggify.Oggify

This is the worker module of Oggify. All common functions live here.
"""

import os, os.path

def _walk_src_tree(root, extension):
    org_dir = os.getcwd()
    chdir(root)
    symlink_dirs = []
    directories = {}
    encode = {}
    for current, subdirs, files in os.walk('.'):
        for subdir in subdirs:
            directories['/'.join((current[2:], subdir))] = None
            if os.path.islink(subdir):
                symlink_dirs.append(subdir)
        for file in files:
            if file.endswith(extension):
                encode['/'.join((current[2:], file))] = None
    chdir(org_dir)
    return (encode, directories)

def _compare_dst_tree(root, extension, encode, directories, src_extension):
    org_dir = os.getcwd()
    chdir(root)
    reencode = {}
    limited_purge = []
    purge = []
    for current, subdirs, files in os.walk('.'):
        dont_walk = []
        for subdir in subdirs:
            if '/'.join((current[2:], subdir)) not in directories:
                purge.append('/'.join((current[2:], subdir)))
                dont_walk.append(subdir)
        for dir in dont_walk:
            subdirs.remove(dir)

        for file in files:
            src_eq = '/'.join((current[2:],
                '.'.join(file.split('.')[:-1] + [src_extension])))
            if src_eq in encode:
                if not file.endswith(extension):
                    limited_purge.append('/'.join((current[2:], file)))
                else:
                    reencode[src_eq] = '/'.join((current[2:], file))
                    del encode[src_eq]
            else:
                purge.append('/'.join((current[2:], file)))
    chdir(org_dir)
    return (encode, reencode, limited_purge, purge)

def diff(src_dir, dst_dir, src_ext, dst_ext):
    (encode, src_directories) = _walk_src_tree(src_dir, src_ext)
    return _compare_dst_tree(dst_dir, dst_ext, encode, src_directories, src_ext)
