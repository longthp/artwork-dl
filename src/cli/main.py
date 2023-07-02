import argparse
from cli import extractor
from typing import Optional, Sequence


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = argparse.ArgumentParser(
        prog="artwork-dl",
        description="Download artwork from music services"
    )
    parser.add_argument("url", action="store", help="album/song URL")
    parser.add_argument("--file", "-f", action="store", help="mutiple albums/songs URLs as a file")

    args = parser.parse_args(argv)

    extractor.main(args.url)

    return 0


if __name__ == "__main__":
    exit(main())
