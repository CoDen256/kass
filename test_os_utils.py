from unittest import TestCase
from os_utils import walktree, resolve, is_parent_of_file


class Test(TestCase):
    def test_walktree(self):
        pass
        # walktree(resolve("test"), print, print)

    def test_is_parent_of_file(self):
        self.assertTrue(is_parent_of_file("/a/b/c", "/a/b/c/d"))
        self.assertTrue(is_parent_of_file("/a/b/c/e/f", "/a/b/c/e/f/g/h/d"))
        self.assertFalse(is_parent_of_file("/a/b/c", "/a/b/e/d"))
        self.assertFalse(is_parent_of_file("/a/b/c", "/a/b/d"))
        self.assertFalse(is_parent_of_file("/a/b/c", "/a/d"))

    def test_resolve(self):
        print(resolve("test"))
        print(resolve("."))
        print(resolve("../"))
