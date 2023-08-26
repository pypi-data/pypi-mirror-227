from os.path import isfile
from sys import argv, exit

from stapidoc.stapi import emit_stapidoc


def main():
    if len(argv) < 2:
        print(f"Usage: {argv[0]} input_file")
        exit(-1)

    [_cmd, input_file, *_] = argv

    if not isfile(input_file):
        raise OSError(f"{input_file} is not a file")

    with open(input_file, "r") as f:
        stapidoc = emit_stapidoc(f.read())

    print(stapidoc)


if __name__ == "__main__":
    main()
