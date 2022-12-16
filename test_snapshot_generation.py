import os
from unittest import TestCase
from snapshot_generation import create_dir_snapshot, create_file_snapshot, create_system_snapshot
from os_utils import resolve
from sys import platform
from datetime import datetime as dt
from model import FileSnapshot, DirSnapshot


class Test(TestCase):
    def test_create_file_snapshot_linux(self):
        target = resolve("./test/generate/file.txt")
        result = os.stat(target)
        snapshot = create_file_snapshot(target, result, "md5")

        self.assertEquals(194, snapshot.size)
        self.assertEquals("d8425199a36abc6266699a6382f674a8", snapshot.message_digest)
        self.assertEquals(target, snapshot.full_path)
        self.assertEquals(dt(2022, 12, 16, 16, 36, 5), snapshot.last_modified)  # stat -c '%y' filename
        if platform == "linux":
            self.assertEquals("coden", snapshot.user)
            self.assertEquals("coden", snapshot.group)
            self.assertEquals("777", snapshot.access_mode)
        else:
            self.assertEquals("0", snapshot.user)
            self.assertEquals("0", snapshot.group)
            self.assertEquals("666", snapshot.access_mode)  # stat -c "%a" file.txt # 33206

    def test_create_dir_snapshot(self):
        target = resolve("./test/generate/folder")
        result = os.stat(target)
        snapshot = create_dir_snapshot(target, result)

        self.assertEquals(target, snapshot.full_path)
        self.assertEquals(dt(2022, 12, 16, 17, 22, 23), snapshot.last_modified)  # stat -c '%y' filename
        if platform == "linux":
            self.assertEquals("coden", snapshot.user)
            self.assertEquals("coden", snapshot.group)
            self.assertEquals("777", snapshot.access_mode)
        else:
            self.assertEquals("0", snapshot.user)
            self.assertEquals("0", snapshot.group)
            self.assertEquals("777", snapshot.access_mode)

    def test_create_system_snapshot_windows(self):
        target = resolve("./test/generate/full")
        result = create_system_snapshot(target, "sha1")
        expected = [
            FileSnapshot(resolve("./test/generate/full/file-1.txt"), "0", "0", "666", dt(2022, 12, 16, 18, 7, 8), "ca9d664f76909b6457775efd45acbed4be41b2d4", 334),
            FileSnapshot(resolve("./test/generate/full/file-2.txt"), "0", "0", "666", dt(2022, 12, 16, 18, 11, 1), "86f7e437faa5a7fce15d1ddcb9eaeaea377667b8", 1),
            FileSnapshot(resolve("./test/generate/full/sub/file-4.txt"), "0", "0", "666", dt(2022, 12, 16, 18, 10, 33), "c45cb38160169d49e45f247fee2b663f51dbefb3", 2128),
            FileSnapshot(resolve("./test/generate/full/sub/sub-2/file-5.txt"), "0", "0", "666", dt(2022, 12, 16, 18, 10, 19), "9f015960625351c70b44c722822e9fdeb3e9ef29", 19),

            DirSnapshot(resolve("./test/generate/full/empty"), "0", "0", "777", dt(2022, 12, 16, 17, 59, 22)),
            DirSnapshot(resolve("./test/generate/full/sub"), "0", "0", "777", dt(2022, 12, 16, 18, 10, 33)),
            DirSnapshot(resolve("./test/generate/full/sub/sub-2"), "0", "0", "777", dt(2022, 12, 16, 18, 10, 19))
        ]

        self.assertEqual("sha1", result.hash_function)

        self.assertCountEqual(expected, result.snapshots)
