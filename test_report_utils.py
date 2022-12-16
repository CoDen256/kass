import datetime
from unittest import TestCase

from model import SystemSnapshot, FileSnapshot, DirSnapshot, SnapshotDiff
from report_utils import create_init_report, create_verification_report


class Test(TestCase):
    def test_create_init_report(self):
        snap = SystemSnapshot([
            FileSnapshot("p", "u", "g", "a", datetime.datetime.now(), "m", 0),
            FileSnapshot("p", "u", "g", "a", datetime.datetime.now(), "m", 0),
            FileSnapshot("p", "u", "g", "a", datetime.datetime.now(), "m", 0),
            FileSnapshot("p", "u", "g", "a", datetime.datetime.now(), "m", 0),
            FileSnapshot("p", "u", "g", "a", datetime.datetime.now(), "m", 0),
            DirSnapshot("p", "u", "g", "a", datetime.datetime.now()),
            DirSnapshot("p", "u", "g", "a", datetime.datetime.now()),
            DirSnapshot("p", "u", "g", "a", datetime.datetime.now()),
        ], 'md5')
        report = create_init_report("/mon", "/ver", 10, snap)

        self.assertEqual(report.monitored_dir, "/mon")
        self.assertEqual(report.verification_file, "/ver")
        self.assertEqual(report.execution_time, 10)
        self.assertEqual(report.files_parsed, 5)
        self.assertEqual(report.directories_parsed, 3)

    def test_create_verification_report(self):
        snap = SystemSnapshot([
            FileSnapshot("p", "u", "g", "a", datetime.datetime.now(), "m", 0),
            FileSnapshot("p", "u", "g", "a", datetime.datetime.now(), "m", 0),
            FileSnapshot("p", "u", "g", "a", datetime.datetime.now(), "m", 0),
            FileSnapshot("p", "u", "g", "a", datetime.datetime.now(), "m", 0),
            DirSnapshot("p", "u", "g", "a", datetime.datetime.now()),
            DirSnapshot("p", "u", "g", "a", datetime.datetime.now()),
            DirSnapshot("p", "u", "g", "a", datetime.datetime.now()),
            DirSnapshot("p", "u", "g", "a", datetime.datetime.now()),
            DirSnapshot("p", "u", "g", "a", datetime.datetime.now()),
            DirSnapshot("p", "u", "g", "a", datetime.datetime.now()),
        ], 'md5')

        diffs = [
            SnapshotDiff("modify", "path", "f", "size", 0, 1),
            SnapshotDiff("modify", "path", "f", "size", 0, 1),
            SnapshotDiff("add", "path", "f", "size", 0, 1),
            SnapshotDiff("add", "path", "f", "object", 0, 1),

            SnapshotDiff("add", "path", "f", "user", 0, 1),
            SnapshotDiff("add", "path", "f", "group", 0, 1),
            SnapshotDiff("delete", "path", "f", "size", 0, 1),
            SnapshotDiff("add", "path", "f", "size", 0, 1),

            SnapshotDiff("add", "path", "f", "size", 0, 1),
            SnapshotDiff("add", "path", "f", "size", 0, 1),
        ]
        report = create_verification_report("monitored", "verification_file", 231, snap, diffs)

        self.assertEqual(report.monitored_dir, "monitored")
        self.assertEqual(report.verification_file, "verification_file")
        self.assertEqual(report.execution_time, 231)
        self.assertEqual(report.files_parsed, 4)
        self.assertEqual(report.directories_parsed, 6)
        self.assertEqual(report.warnings, 10)
        self.assertCountEqual(report.diffs, diffs)
