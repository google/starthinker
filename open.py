import os
from shutil import copyfile, Error

from setup import EXECUTE_PATH

PATH_FROM = EXECUTE_PATH
PATH_TO = '/home/starthinker_opensource/'
OPEN_FLAG = '#  Licensed under the Apache License, Version 2.0 (the "License");'


def swap_path(path):
  return path.replace(EXECUTE_PATH, PATH_TO, 1)


def copy_dir(dpath):
  directory = swap_path(dpath)
  if not os.path.exists(directory): os.makedirs(directory)


def copy_file(dpath, fname, use_filter=True):
  path_from = dpath + fname
  path_to = swap_path(path_from)

  # filter out files
  if use_filter:
    if fname.endswith('.pyc'): return
    if dpath.startswith(PATH_FROM + '/.git/'): return 
    if dpath.startswith(PATH_FROM + '/ui/'): return
    if OPEN_FLAG not in open(path_from).read(): return

  # do the copy
  print path_from, path_to
  copy_dir(dpath)
  copyfile(path_from, path_to)


if __name__ == "__main__":

  # copy licenses
  copy_file(PATH_FROM, 'LICENSE', False)
  copy_file(PATH_FROM, 'README.md', False)
  copy_file(PATH_FROM, 'CONTRIBUTING.md', False)

  # copy samples
  copy_file(PATH_FROM + 'project/sample/', 'say_hello.json', False)

  # copy all licensed files
  for dpath, dlist, flist in os.walk(PATH_FROM):
    if dpath[-1] != '/': dpath += '/' # standardize all directories to end in a slash
    use_filter = not dpath.startswith(PATH_FROM + 'third_party/')
    for fname in flist:
      copy_file(dpath, fname, use_filter)
