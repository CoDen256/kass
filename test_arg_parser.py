from unittest import TestCase
from siv import arg_parser

class Test(TestCase):
    def test_arg_parser_init(self):
        args = arg_parser().parse_args(["-i", "-D", "/path", "-V" "/ver", "-R", "/report", "-H" "md5"])
        self.assertEqual(args.monitored_directory, "/path")
        self.assertEqual(args.init, True)
        self.assertEqual(args.verify, False)
        self.assertEqual(args.verification_file, "/ver")
        self.assertEqual(args.report_file, "/report")
        self.assertEqual(args.hash_function, "md5")

    def test_arg_parser_verify(self):
        args = arg_parser().parse_args(["-v", "-D", "/path", "-V" "/ver", "-R", "/report"])
        self.assertEqual(args.monitored_directory, "/path")
        self.assertEqual(args.init, False)
        self.assertEqual(args.verify, True)
        self.assertEqual(args.verification_file, "/ver")
        self.assertEqual(args.report_file, "/report")
