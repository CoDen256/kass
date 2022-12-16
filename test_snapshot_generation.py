import datetime
from unittest import TestCase
from snapshot_generation import create_dir_snapshot, create_file_snapshot, create_system_snapshot
import os
from os_utils import resolve
from sys import platform


class Test(TestCase):
    def test_create_file_snapshot_linux(self):
        target = resolve("./test/generate/file.txt")
        result = os.stat(target)
        snapshot = create_file_snapshot(target, result, "md5")

        self.assertEquals(194, snapshot.size)
        self.assertEquals("d8425199a36abc6266699a6382f674a8", snapshot.message_digest)
        self.assertEquals(target, snapshot.full_path)
        self.assertEquals(datetime.datetime(2022, 12, 16, 16, 36, 5), snapshot.last_modified)  # stat -c '%y' filename
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
        self.assertEquals(datetime.datetime(2022, 12, 16, 17, 22, 23), snapshot.last_modified)  # stat -c '%y' filename
        if platform == "linux":
            self.assertEquals("coden", snapshot.user)
            self.assertEquals("coden", snapshot.group)
            self.assertEquals("777", snapshot.access_mode)
        else:
            self.assertEquals("0", snapshot.user)
            self.assertEquals("0", snapshot.group)
            self.assertEquals("777", snapshot.access_mode)
