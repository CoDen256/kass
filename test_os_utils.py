from unittest import TestCase
from os_utils import walktree,resolve

class Test(TestCase):
    def test_walktree(self):
        walktree(resolve("."), print, print)
