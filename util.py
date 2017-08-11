def path_set(d, p, v):
  ''' Allows dict access via path list (e.g. path_set(d, [1,2,3], 5) == d[1][2][3]=5) '''
  d[p[0]] = path_set(d.get(p[0]) or {}, p[1:], v) if len(p) > 1 else v
  return d

def path_get(d, p):
  ''' Allows dict access via path list (e.g. path_get(d, [1,2,3]) == d[1][2][3]) '''
  r = d.get(p[0]) if type(d) == dict and len(p) > 0 else None
  return path_get(r, p[1:]) if len(p) > 1 and r else r

def walk_tree(T, K=[]):
  ''' Allows walking through a tree returning path list and leaf nodes--a bit like os.walk '''
  for k,v in T.items():
    if type(v) == dict:
      for kk,vv in walk_tree(v, K+[k]):
        yield((kk, vv))
    else:
      yield((K+[k], v))

def path_merge(d, *D):
  ''' Like dict(d, **dd for dd in D) but recusively on dicts for internal path merging '''
  for DD in D:
    for k, v in DD.items():
      vv = d.get(k, {})
      if type(vv) == dict and type(v) == dict:
        d[k] = path_merge(vv, v)
      else:
        d[k] = v
  return d

def paths_to_tree(*P):
  ''' Convert a file-system path into a dict tree '''
  import os
  T = {}
  for p in P:
    if os.path.isdir(p):
      for r, D, F in os.walk(p):
        R = list(filter(None, r.split(os.path.sep)))
        for d in D:
          path_set(T, R+[d], {})
        for f in F:
          path_set(T, R+[f], True)
    elif os.path.isfile(p):
      r, f = os.path.split(p)
      R = list(filter(None, r.split(os.path.sep)))
      path_set(T, R+[f], True)
  return T
