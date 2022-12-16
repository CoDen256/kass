import datetime
from unittest import TestCase

from model import SystemSnapshot, DirSnapshot, FileSnapshot, HashFunction
from os_utils import resolve, sha1
from snapshot_serialization import write_system_snapshot, load_system_snapshot


class Test(TestCase):
    format = "%m-%d-%YT%H:%M:%S"
    date0 = datetime.datetime.strptime("10-10-2010T10:10:50", format)
    date1 = datetime.datetime.strptime("12-13-2020T23:24:30", format)
    date2 = datetime.datetime.strptime("11-12-2030T22:50:00", format)

    snap = SystemSnapshot(
        [
            DirSnapshot("/root/dir/", "user-2", "group-2", "777", datetime.datetime.max.replace(microsecond=0)),
            FileSnapshot("/root/dir/file-2.txt", "user-1", "group-0", "666", date1, "aaa", 1),
            FileSnapshot("/root/file-3.txt", "user-0", "group-0", "555", date0, "bbb", 1),
            FileSnapshot("/root/dir/sub/folder/file-1.txt", "user-1", "group-1", "444",
                         datetime.datetime.max.replace(microsecond=0), "ccc",
                         1),
            DirSnapshot("/root/dir/sub", "user-3", "group-3", "333", date0),
            DirSnapshot("/root/dir/sub/folder", "user-4", "group-4", "111", date2),
            DirSnapshot("/root/dir/sub/folder/deeper", "user-5", "group-5", "222", date1),
        ],
        'md5'
    )
    source = resolve("./test/serialize/example-snapshot.csv")

    def test_parse_snapshot(self):
        target = load_system_snapshot(Test.source)
        self.assertEqual(target.hash_function, Test.snap.hash_function)
        self.assertCountEqual(target.snapshots, Test.snap.snapshots)

    def test_write_snapshot(self):
        target = resolve("./test/serialize/test-snapshot.csv")
        write_system_snapshot(Test.snap, target)
        self.assertEqual("4adaa9dd9d3dc77feb3ed6d8527d01df2a6168fb", sha1(target))
        self.assertEqual(sha1(target), sha1(Test.source))

    def test_parse_write_snapshot(self):
        target = resolve("./test/serialize/test-2-snapshot.csv")

        write_system_snapshot(Test.snap, target)
        parsed = load_system_snapshot(target)

        self.assertEqual(parsed.hash_function, "md5")
        self.assertEqual(Test.snap.hash_function, parsed.hash_function)
        self.assertCountEqual(Test.snap.snapshots, parsed.snapshots)
