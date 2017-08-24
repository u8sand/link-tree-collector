#!/bin/env python

import os
from time import time
from subprocess import Popen, PIPE
from util import *

def Popen_v(argv, *args, **kwargs):
  ''' Verbose version of Popen '''
  print(*argv)
  return Popen(argv, *args, **kwargs)

last_time = time()
def rolling_time():
  global last_time
  t = time()
  dt = t - last_time
  last_time = t
  return dt

print('Loading pacman packages...')
pacman_pkgs = set(Popen_v(["bash", "-c",
  "pacman -Qii | awk '/^MODIFIED/{print $2}'"
], stdout=PIPE).stdout.read().decode().splitlines())
pacman_pkgs_tree = paths_to_tree(*pacman_pkgs)
print('...', rolling_time())

print('Loading whitelist...', end=' ')
whitelist = set(map(os.path.expandvars, open('whitelist', 'r').read().splitlines()))
whitelist_tree = paths_to_tree(*whitelist)
print(rolling_time())

print('Loading blacklist...', end=' ')
blacklist = set(map(os.path.expandvars, open('blacklist', 'r').read().splitlines()))
blacklist_tree = paths_to_tree(*blacklist)
print(rolling_time())

# Note that this order causes blacklist to trump whitelist no matter what
#  a nicer approach might be to let depth trump all but it would require
#  a different implementation
print('Merging trees...', end=' ')
filelist_tree = path_merge(pacman_pkgs_tree, whitelist_tree)
for path, _ in walk_tree(blacklist_tree):
  path_set(filelist_tree, path, False)
print(rolling_time())

print('Creating links...')
Popen_v(['rm', '-r', 'root'])
Popen_v(['mkdir', '-p', 'root'])
for path, want in walk_tree(filelist_tree):
  if not want:
    continue
  f = os.path.sep+os.path.sep.join(path)
  dirname = 'root'+os.path.dirname(f)
  if not os.path.exists(dirname):
    Popen_v(['mkdir', '-p', dirname])
  Popen_v(['ln', '-P', f, 'root'+f])
print('...', rolling_time())
print('Done.')
