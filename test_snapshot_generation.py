import os
from unittest import TestCase, skip
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

        self.assertEqual(194, snapshot.size)
        self.assertEqual("d8425199a36abc6266699a6382f674a8", snapshot.message_digest)
        self.assertEqual(target, snapshot.full_path)
        self.assertEqual(dt(2022, 12, 16, 16, 36, 5), snapshot.last_modified)  # stat -c '%y' filename
        if platform == "linux":
            self.assertEqual("coden", snapshot.user)
            self.assertEqual("coden", snapshot.group)
            self.assertEqual("777", snapshot.access_mode)
        else:
            self.assertEqual("0", snapshot.user)
            self.assertEqual("0", snapshot.group)
            self.assertEqual("666", snapshot.access_mode)  # stat -c "%a" file.txt # 33206

    def test_create_dir_snapshot(self):
        target = resolve("./test/generate/folder")
        result = os.stat(target)
        snapshot = create_dir_snapshot(target, result)

        self.assertEqual(target, snapshot.full_path)
        self.assertEqual(dt(2022, 12, 16, 17, 22, 23), snapshot.last_modified)  # stat -c '%y' filename
        if platform == "linux":
            self.assertEqual("coden", snapshot.user)
            self.assertEqual("coden", snapshot.group)
            self.assertEqual("777", snapshot.access_mode)
        else:
            self.assertEqual("0", snapshot.user)
            self.assertEqual("0", snapshot.group)
            self.assertEqual("777", snapshot.access_mode)

    # @skip
    def test_create_system_snapshot_windows(self):
        target = resolve("./test/generate/full")
        result = create_system_snapshot(target, "sha1")
        user = "0"
        group = "0"
        expected = [
            FileSnapshot(resolve("./test/generate/full/file-1.txt"), user, group, "666", dt(2022, 12, 16, 18, 7, 8), "ca9d664f76909b6457775efd45acbed4be41b2d4", 334),
            FileSnapshot(resolve("./test/generate/full/file-2.txt"), user, group, "666", dt(2022, 12, 16, 18, 11, 1), "86f7e437faa5a7fce15d1ddcb9eaeaea377667b8", 1),
            FileSnapshot(resolve("./test/generate/full/sub/file-4.txt"), user, group, "666", dt(2022, 12, 16, 18, 10, 33), "c45cb38160169d49e45f247fee2b663f51dbefb3", 2128),
            FileSnapshot(resolve("./test/generate/full/sub/sub-2/file-5.txt"), user, group, "666", dt(2022, 12, 16, 18, 10, 19), "9f015960625351c70b44c722822e9fdeb3e9ef29", 19),

            DirSnapshot(resolve("./test/generate/full/empty"), user, group, "777", dt(2022, 12, 16, 17, 59, 22)),
            DirSnapshot(resolve("./test/generate/full/sub"), user, group, "777", dt(2022, 12, 16, 18, 10, 33)),
            DirSnapshot(resolve("./test/generate/full/sub/sub-2"), user, group, "777", dt(2022, 12, 16, 18, 10, 19))
        ]

        self.assertEqual("sha1", result.hash_function)

        self.assertCountEqual(expected, result.snapshots)

    @skip
    def test_create_system_snapshot_linux(self):
        target = resolve("./test/generate/full-linux")
        result = create_system_snapshot(target, "sha1")
        user = "coden"
        group = "coden"
        expected = [
            FileSnapshot(resolve("./test/generate/full/file-1.txt"), user, group, "777", dt(2022, 12, 16, 18, 7, 8), "ca9d664f76909b6457775efd45acbed4be41b2d4", 334),
            FileSnapshot(resolve("./test/generate/full/file-2.txt"), user, group, "777", dt(2022, 12, 16, 18, 11, 1), "86f7e437faa5a7fce15d1ddcb9eaeaea377667b8", 1),
            FileSnapshot(resolve("./test/generate/full/sub/file-4.txt"), user, group, "777", dt(2022, 12, 16, 18, 10, 33), "c45cb38160169d49e45f247fee2b663f51dbefb3", 2128),
            FileSnapshot(resolve("./test/generate/full/sub/sub-2/file-5.txt"), user, group, "777", dt(2022, 12, 16, 18, 10, 19), "9f015960625351c70b44c722822e9fdeb3e9ef29", 19),

            DirSnapshot(resolve("./test/generate/full/empty"), user, group, "777", dt(2022, 12, 16, 17, 59, 22)),
            DirSnapshot(resolve("./test/generate/full/sub"), user, group, "777", dt(2022, 12, 16, 18, 10, 33)),
            DirSnapshot(resolve("./test/generate/full/sub/sub-2"), user, group, "777", dt(2022, 12, 16, 18, 10, 19))
        ]

        self.assertEqual("sha1", result.hash_function)

        self.assertCountEqual(expected, result.snapshots)
