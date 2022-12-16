import datetime
from unittest import TestCase
from snapshot_generation import create_dir_snapshot, create_file_snapshot, create_system_snapshot
import os
from os_utils import resolve


class Test(TestCase):
    def test_create_file_snapshot(self):
        target = resolve("./test/generate/file.txt")
        result = os.stat(target)
        snapshot = create_file_snapshot(target, result, "md5")

        self.assertEquals(194, snapshot.size)
        self.assertEquals("coden", snapshot.user)
        self.assertEquals("coden", snapshot.group)
        self.assertEquals("d8425199a36abc6266699a6382f674a8", snapshot.message_digest)
        self.assertEquals(target, snapshot.full_path)
        self.assertEquals(datetime.datetime(2022, 12, 16, 16, 36, 5), snapshot.last_modified)  # stat -c '%y' filename
        self.assertEquals("777", snapshot.access_mode) # stat -c "%a" file.txt

    def test_create_dir_snapshot(self):
        self.fail()
