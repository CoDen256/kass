import os
from unittest import TestCase, skip
from snapshot_generation import create_dir_snapshot, create_file_snapshot, create_system_snapshot
from os_utils import resolve
from sys import platform
from datetime import datetime as dt
from model import FileSnapshot, DirSnapshot


class Test(TestCase):
    maxDiff = None
    def test_create_file_snapshot(self):
        target = resolve("./test/generate/file.txt")
        result = os.stat(target)
        snapshot = create_file_snapshot(target, result, "md5")

        self.assertEqual(167, snapshot.size)
        self.assertEqual("442201d0ea81097b88b844d53c33bb93", snapshot.message_digest)
        self.assertEqual(target, snapshot.full_path)
        self.assertEqual(dt(2022, 12, 16, 18, 47, 18), snapshot.last_modified)  # stat -c '%y' filename
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
        self.assertEqual(dt(2022, 12, 16, 18, 52, 12), snapshot.last_modified)  # stat -c '%y' filename
        if platform == "linux":
            self.assertEqual("coden", snapshot.user)
            self.assertEqual("coden", snapshot.group)
            self.assertEqual("777", snapshot.access_mode)
        else:
            self.assertEqual("0", snapshot.user)
            self.assertEqual("0", snapshot.group)
            self.assertEqual("777", snapshot.access_mode)

    def test_create_system_snapshot_windows(self):
        target = resolve("./test/generate/full")
        result = create_system_snapshot(target, "md5")
        user = "0"
        group = "0"
        expected = [
            FileSnapshot(resolve("./test/generate/full/file-1.txt"), user, group, "666", dt(2022, 12, 16, 18, 47, 12), "4462256a6ee3a6461a935e4cf02b8798", 287),
            FileSnapshot(resolve("./test/generate/full/file-2.txt"), user, group, "666", dt(2022, 12, 16, 18, 47, 15), "0cc175b9c0f1b6a831c399e269772661", 1),
            FileSnapshot(resolve("./test/generate/full/sub/file-4.txt"), user, group, "666", dt(2022, 12, 16, 18, 47, 23), "8bc2398146fb71fcdc2863d05d29433f", 1904),
            FileSnapshot(resolve("./test/generate/full/sub/sub-2/file-5.txt"), user, group, "666", dt(2022, 12, 16, 18, 47, 27), "1a6f8abe44f6b9c5a7c2435c43749dea", 17),

            DirSnapshot(resolve("./test/generate/full/sub"), user, group, "777", dt(2022, 12, 16, 18, 10, 33)),
            DirSnapshot(resolve("./test/generate/full/sub/sub-2"), user, group, "777", dt(2022, 12, 16, 18, 10, 19))
        ]

        self.assertEqual("md5", result.hash_function)

        self.assertCountEqual(expected, result.snapshots)

    # @skip
    # def test_create_system_snapshot_linux(self):
    #     target = resolve("./test/generate/full-linux")
    #     result = create_system_snapshot(target, "sha1")
    #     user = "coden"
    #     group = "coden"
    #     expected = [
    #         FileSnapshot(resolve("./test/generate/full/file-1.txt"), user, group, "777", dt(2022, 12, 16, 18, 7, 8), "ca9d664f76909b6457775efd45acbed4be41b2d4", 287),
    #         FileSnapshot(resolve("./test/generate/full/file-2.txt"), user, group, "777", dt(2022, 12, 16, 18, 11, 1), "86f7e437faa5a7fce15d1ddcb9eaeaea377667b8", 1),
    #         FileSnapshot(resolve("./test/generate/full/sub/file-4.txt"), user, group, "777", dt(2022, 12, 16, 18, 10, 33), "c45cb38160169d49e45f247fee2b663f51dbefb3", 1904),
    #         FileSnapshot(resolve("./test/generate/full/sub/sub-2/file-5.txt"), user, group, "777", dt(2022, 12, 16, 18, 10, 19), "9f015960625351c70b44c722822e9fdeb3e9ef29", 17),
    #
    #         DirSnapshot(resolve("./test/generate/full/empty"), user, group, "777", dt(2022, 12, 16, 17, 59, 22)),
    #         DirSnapshot(resolve("./test/generate/full/sub"), user, group, "777", dt(2022, 12, 16, 18, 10, 33)),
    #         DirSnapshot(resolve("./test/generate/full/sub/sub-2"), user, group, "777", dt(2022, 12, 16, 18, 10, 19))
    #     ]
    #
    #     self.assertEqual("sha1", result.hash_function)
    #
    #     self.assertCountEqual(expected, result.snapshots)
