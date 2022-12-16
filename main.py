import argparse
from model import HashFunction

def arg_parser():
    parser = argparse.ArgumentParser(
        prog='ProgramName',
        description='What the program does',
        epilog='Text at the bottom of help')

    parser.add_argument("-i", dest='init', action="store_true")
    parser.add_argument("-v", dest='verify', action="store_true")
    parser.add_argument("-D", dest='monitored_directory')
    parser.add_argument("-V", dest='verification_file')
    parser.add_argument("-R", dest='report_file')
    parser.add_argument("-H", choices=["md5", "sha256"], dest='hash_function')
    return parser


def main():
    args = arg_parser().parse_args()
    print(args)


if __name__ == '__main__':
    main()
