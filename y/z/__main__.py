"""

"""


def z_help():
    """Help for the Zoidberg Conspiracy"""

    print("help")
    return 0


def md():
    from sys import stdout, stdin
    from json import dump

    from .md import parse_stream

    for data in parse_stream(stdin):
        dump(data, stdout, indent=4)
        print()

    return 0


if __name__ == "__main__":
    from sys import argv

    if len(argv) > 1:
        match argv[1]:
            case "md":
                md()
                exit()

    z_help()
    exit()
