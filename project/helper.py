import argparse
from glob import glob
from util.project import get_project
from setup import EXECUTE_PATH

if __name__ == "__main__":

  parser = argparse.ArgumentParser()
  parser.add_argument('folder', help='one of the folders starthinker/project/')
  args = parser.parse_args()

  for filepath in glob('%sproject/%s/*.json' % (EXECUTE_PATH, args.folder)):
    try:
      project = get_project(filepath)
      print 'JSON OK:', filepath
    except Exception, e:
      print 'JSON ERROR:', filepath, str(e)
