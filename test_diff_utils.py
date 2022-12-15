import datetime
from unittest import TestCase
from diff_utils import compare_snapshots
from model import SnapshotDiff, FileSnapshot, Snapshot, DirSnapshot, SystemSnapshot


class Test(TestCase):
    def test_compare_snapshots(self):
        s1 = SystemSnapshot([], "md5")
        s2 = SystemSnapshot([], "md5")
        result = compare_snapshots(s1, s2)
        self.assertCountEqual([], result)

    def test_compare_snapshots_add_file(self):
        s1 = SystemSnapshot([], "md5")
        s2 = SystemSnapshot([
            FileSnapshot("path", "u", "g", "a", datetime.datetime.max, "md", 0)
        ], "md5")

        result = compare_snapshots(s1, s2)
        self.assertCountEqual([
            SnapshotDiff('add', 'path', 'f', 'object', None, None)
        ], result)

    def test_compare_snapshots_add_dir(self):
        s1 = SystemSnapshot([], "md5")
        s2 = SystemSnapshot([
            DirSnapshot("path", "u", "g", "a", datetime.datetime.max)
        ], "md5")

        result = compare_snapshots(s1, s2)
        self.assertCountEqual([
            SnapshotDiff('add', 'path', 'd', 'object', None, None)
        ], result)

    def test_compare_snapshots_remove_file(self):
        s1 = SystemSnapshot([
            FileSnapshot("path", "u", "g", "a", datetime.datetime.max, "md", 0)
        ], "md5")
        s2 = SystemSnapshot([], "md5")

        result = compare_snapshots(s1, s2)
        self.assertCountEqual([
            SnapshotDiff('delete', 'path', 'f', 'object', None, None)
        ], result)

    def test_compare_snapshots_remove_dir(self):
        s1 = SystemSnapshot([
            DirSnapshot("path", "u", "g", "a", datetime.datetime.max)
        ], "md5")
        s2 = SystemSnapshot([], "md5")

        result = compare_snapshots(s1, s2)
        self.assertCountEqual([
            SnapshotDiff('delete', 'path', 'd', 'object', None, None)
        ], result)

    def test_compare_snapshots_same_file(self):
        s1 = SystemSnapshot([
            FileSnapshot("path", "u", "g", "a", datetime.datetime.max, "md", 0)
        ], "md5")

        result = compare_snapshots(s1, s1)
        self.assertCountEqual([], result)

    def test_compare_snapshots_same_dir(self):
        s1 = SystemSnapshot([
            DirSnapshot("path", "u", "g", "a", datetime.datetime.max)
        ], "md5")

        result = compare_snapshots(s1, s1)
        self.assertCountEqual([], result)

    def test_compare_snapshots_remove_file_add_file(self):
        s1 = SystemSnapshot([
            FileSnapshot("path", "u", "g", "a", datetime.datetime.max, "md", 0)
        ], "md5")
        s2 = SystemSnapshot([
            FileSnapshot("path2", "u", "g", "a", datetime.datetime.max, "md", 0)
        ], "md5")

        result = compare_snapshots(s1, s2)
        self.assertCountEqual([
            SnapshotDiff('delete', 'path', 'f', 'object', None, None),
            SnapshotDiff('add', 'path2', 'f', 'object', None, None)
        ], result)

    def test_compare_snapshots_remove_dir_add_dir(self):
        s1 = SystemSnapshot([
            DirSnapshot("path", "u", "g", "a", datetime.datetime.max)
        ], "md5")
        s2 = SystemSnapshot([
            DirSnapshot("path2", "u", "g", "a", datetime.datetime.max)
        ], "md5")

        result = compare_snapshots(s1, s2)
        self.assertCountEqual([
            SnapshotDiff('delete', 'path', 'd', 'object', None, None),
            SnapshotDiff('add', 'path2', 'd', 'object', None, None)
        ], result)