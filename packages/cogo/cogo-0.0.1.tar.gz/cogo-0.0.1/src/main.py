import sys
import argparse
from commands import config, collect, distribute, get_repo_path


def create_parser():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(
        help="available subcommands",
        dest="command",
        required=True,
    )

    parser.add_argument("-v", "--version", action="version", version="0.1.0")

    config_parser = subparsers.add_parser("config", help="Shows the loaded config file")

    collect_parser = subparsers.add_parser(
        "collect", help="copies all files into the repository"
    )
    collect_parser.add_argument(
        "--dry-run",
        action="store_true",
        help="only print the files that would be copied",
    )

    distribute_parser = subparsers.add_parser(
        "distribute", help="copies all files into their destination"
    )
    distribute_parser.add_argument(
        "--dry-run",
        action="store_true",
        help="only print the files that would be copied",
    )

    cd_parser = subparsers.add_parser("cd", help="prints the path to the repository")
    ls_parser = subparsers.add_parser("ls", help="prints the path to the repository")

    return parser


def main():
    ns = create_parser().parse_args(sys.argv[1:])

    match ns.command:
        case "config":
            config(ns)
        case "collect":
            collect(ns)
        case "distribute":
            distribute(ns)
        case "cd":
            p = get_repo_path()
            print(f"\n  cd /d {p}")
        case "ls":
            p = get_repo_path()
            print(f"\n  ls {p}")
        case _:
            print("Not a valid command! Use --help for more information.")


if __name__ == "__main__":
    main()
