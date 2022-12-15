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

    def test_compare_snapshots_modify_file_size(self):
        s1 = SystemSnapshot([
            FileSnapshot("path", "u", "g", "a", datetime.datetime.max, "md", 0)
        ], "md5")
        s2 = SystemSnapshot([
            FileSnapshot("path", "u", "g", "a", datetime.datetime.max, "md", 1)
        ], "md5")

        result = compare_snapshots(s1, s2)
        self.assertCountEqual([
            SnapshotDiff('modify', 'path', 'f', 'size', 0, 1)
        ], result)

    def test_compare_snapshots_modify_file_hash(self):
        s1 = SystemSnapshot([
            FileSnapshot("path", "u", "g", "a", datetime.datetime.max, "md1", 0)
        ], "md5")
        s2 = SystemSnapshot([
            FileSnapshot("path", "u", "g", "a", datetime.datetime.max, "md2", 0)
        ], "md5")

        result = compare_snapshots(s1, s2)
        self.assertCountEqual([
            SnapshotDiff('modify', 'path', 'f', 'hash', "md1", "md2")
        ], result)
    def test_compare_snapshots_modify_file_user(self):
        s1 = SystemSnapshot([
            FileSnapshot("path", "u1", "g", "a", datetime.datetime.max, "md", 0)
        ], "md5")
        s2 = SystemSnapshot([
            FileSnapshot("path", "u2", "g", "a", datetime.datetime.max, "md", 0)
        ], "md5")

        result = compare_snapshots(s1, s2)
        self.assertCountEqual([
            SnapshotDiff('modify', 'path', 'f', 'user', "u1", "u2")
        ], result)

    def test_compare_snapshots_modify_file_group(self):
        s1 = SystemSnapshot([
            FileSnapshot("path", "u", "g1", "a", datetime.datetime.max, "md", 0)
        ], "md5")
        s2 = SystemSnapshot([
            FileSnapshot("path", "u", "g2", "a", datetime.datetime.max, "md", 0)
        ], "md5")

        result = compare_snapshots(s1, s2)
        self.assertCountEqual([
            SnapshotDiff('modify', 'path', 'f', 'group', "g1", "g2")
        ], result)

    def test_compare_snapshots_modify_file_access(self):
        s1 = SystemSnapshot([
            FileSnapshot("path", "u", "g", "a1", datetime.datetime.max, "md", 0)
        ], "md5")
        s2 = SystemSnapshot([
            FileSnapshot("path", "u", "g", "a2", datetime.datetime.max, "md", 0)
        ], "md5")

        result = compare_snapshots(s1, s2)
        self.assertCountEqual([
            SnapshotDiff('modify', 'path', 'f', 'access', "a1", "a2")
        ], result)

    def test_compare_snapshots_modify_file_modified(self):
        s1 = SystemSnapshot([
            FileSnapshot("path", "u", "g", "a", datetime.datetime.max, "md", 0)
        ], "md5")
        s2 = SystemSnapshot([
            FileSnapshot("path", "u", "g", "a", datetime.datetime.min, "md", 0)
        ], "md5")

        result = compare_snapshots(s1, s2)
        self.assertCountEqual([
            SnapshotDiff('modify', 'path', 'f', 'modified', datetime.datetime.max, datetime.datetime.min)
        ], result)

    def test_compare_snapshots_modify_file_modified_hash(self):
        s1 = SystemSnapshot([
            FileSnapshot("path", "u", "g", "a", datetime.datetime.max, "md1", 0)
        ], "md5")
        s2 = SystemSnapshot([
            FileSnapshot("path", "u", "g", "a", datetime.datetime.min, "md2", 0)
        ], "md5")

        result = compare_snapshots(s1, s2)
        self.assertCountEqual([
            SnapshotDiff('modify', 'path', 'f', 'modified', datetime.datetime.max, datetime.datetime.min),
            SnapshotDiff('modify', 'path', 'f', 'hash', "md1", "md2")
        ], result)

    def test_compare_snapshots_modify_file_all(self):
        s1 = SystemSnapshot([
            FileSnapshot("path", "u1", "g1", "a1", datetime.datetime.max, "md1", 0)
        ], "md5")
        s2 = SystemSnapshot([
            FileSnapshot("path", "u2", "g2", "a2", datetime.datetime.min, "md2", 1)
        ], "md5")

        result = compare_snapshots(s1, s2)
        self.assertCountEqual([
            SnapshotDiff('modify', 'path', 'f', 'modified', datetime.datetime.max, datetime.datetime.min),
            SnapshotDiff('modify', 'path', 'f', 'hash', "md1", "md2"),
            SnapshotDiff('modify', 'path', 'f', 'user', "u1", "u2"),
            SnapshotDiff('modify', 'path', 'f', 'access', "a1", "a2"),
            SnapshotDiff('modify', 'path', 'f', 'group', "g1", "g2"),
            SnapshotDiff('modify', 'path', 'f', 'size', 0, 1)
        ], result)

    def test_compare_snapshots_add_delete_same_path(self):
        s1 = SystemSnapshot([
            FileSnapshot("path", "u", "g", "a", datetime.datetime.max, "md", 0)
        ], "md5")
        s2 = SystemSnapshot([
            DirSnapshot("path", "u", "g", "a", datetime.datetime.max)
        ], "md5")

        result = compare_snapshots(s1, s2)
        self.assertCountEqual([
            SnapshotDiff('add', 'path', 'd', 'object', None, None),
            SnapshotDiff('delete', 'path', 'f', 'object', None, None)
        ], result)
