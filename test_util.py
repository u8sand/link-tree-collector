from util import *
from unittest import TestCase

class TestUtil(TestCase):
  def test_path_set(self):
    self.assertEquals(
      path_set({}, 'a', 'b'),
      {'a': 'b'},
      'Basic create')
    self.assertEquals(
      path_set({'a': {'b': 'c'}}, ['a', 'b'], 'd'),
      {'a': {'b': 'd'}},
      'Replace subpath')
    self.assertEquals(
      path_set({'a': {'b': 'c'}}, ['b', 'a'], 'd'),
      {'a': {'b': 'c'}, 'b': {'a': 'd'}},
      'Create subpath')

  def test_path_get(self):
    self.assertEquals(
      path_get({}, ['a', 'b']),
      None,
      'Nothing to find')
    self.assertEquals(
      path_get({'a': 'b'}, ['a', 'b']),
      None,
      'End of the line')
    self.assertEquals(
      path_get({'a': 'b'}, 'a'),
      'b',
      'Basic find')
    self.assertEquals(
      path_get({'a': {'b': 'c'}}, ['a', 'b']),
      'c',
      'Find subpath')

  def test_walk_tree(self):
    T = {
      'a': {
        'b': {
          'c': 'd'
        },
        'e': {
          'f': 'g'
        },
        'h': 'i'
      },
      'j': 'k'
    }
    V = set([
      'a/b/c/d',
      'a/e/f/g',
      'a/h/i',
      'j/k'
    ])
    for k, v in walk_tree(T):
      p = '/'.join(k+[v])
      self.assertIn(p, V, "Path found")
      V.remove(p)
    self.assertEquals(V, set(), "All paths found")

  def test_path_merge(self):
    self.assertEquals(
      path_merge({}, {'a': 'b'}),
      {'a': 'b'},
      'Simple create')
    self.assertEquals(
      path_merge({'a': 'b'}, {}),
      {'a': 'b'},
      'Simple create (reverse)')
    self.assertEquals(
      path_merge({'a': 'b'}, {'a': {'b': 'c'}}),
      {'a': {'b': 'c'}},
      'Overlay overwrite')
    self.assertEquals(
      path_merge({'a': {'b': 'c'}}, {'a': 'b'}),
      {'a': 'b'},
      'Overlay drop')
    self.assertEquals(
      path_merge({'a': {'b': {'c': 'd'}}}, {'a': {'b': {'d': 'e'}}}),
      {'a': {'b': {'c': 'd', 'd': 'e'}}},
      'Overlay merge')

  def test_paths_to_tree(self):
    # setup
    import os
    os.mkdir('__test')
    os.mkdir('__test/a')
    os.mknod('__test/a/b')
    os.mkdir('__test/a/c')
    os.mknod('__test/d')
    os.mkdir('__test/e')
    os.mknod('__test/e/f')

    # test
    self.assertEquals(
      paths_to_tree('__test/a/b'),
      {
        '__test': {
          'a': {
            'b': True,
          },
        },
      },
      'Single file')
    self.assertEquals(
      paths_to_tree('__test/a/', '__test/e/'),
      {
        '__test': {
          'a': {
            'b': True,
            'c': {},
          },
          'e': {
            'f': True,
          },
        },
      },
      'Sub-trees')
    self.assertEquals(
      paths_to_tree('__test'),
      {
        '__test': {
          'a': {
            'b': True,
            'c': {},
          },
          'd': True,
          'e': {
            'f': True,
          },
        },
      },
      'Full tree')

    # cleanup
    os.remove('__test/a/b')
    os.remove('__test/d')
    os.remove('__test/e/f')
    os.rmdir('__test/a/c')
    os.rmdir('__test/a')
    os.rmdir('__test/e')
    os.rmdir('__test')
    self.assertEquals(
      paths_to_tree('__test'),
      {},
      'Successful Cleanup')
