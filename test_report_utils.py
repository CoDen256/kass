import datetime
from unittest import TestCase

from model import SystemSnapshot, FileSnapshot, DirSnapshot
from report_utils import create_init_report


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
