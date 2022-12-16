import argparse
from model import HashFunction
from runner import run_initialize_mode, run_verification_mode


def arg_parser():
    parser = argparse.ArgumentParser(
        prog='siv.py',
        description='System Integration Verifier')

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("-i", dest='init', action="store_true", help="Initialization mode")
    group.add_argument("-v", dest='verify', action="store_true", help="Verification mode")

    parser.add_argument("-D", dest='monitored_directory', required=True)
    parser.add_argument("-V", dest='verification_file', required=True)
    parser.add_argument("-R", dest='report_file', required=True)

    parser.add_argument("-H", choices=list([i.value for i in HashFunction]),
                        dest='hash_function',
                        help="Hash function to be used for computing message digest of files")
    return parser


def main():
    parser = arg_parser()
    args = parser.parse_args()
    if args.init:
        if args.hash_function is None:
            parser.error("The following arguments are required for Initialization mode: -H")
        run_initialize_mode(args.monitored_directory, args.verification_file, args.report_file, args.hash_function)
    if args.verify:
        run_verification_mode(args.monitored_directory, args.verification_file, args.report_file)


if __name__ == '__main__':
    main()
