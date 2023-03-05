#!/usr/bin/env python3

"""Print version to standard output."""

import pathlib
import re
import sys


def show_version_string() -> None:
    """Show version string found in __about__.py module"""
    version_regex = re.compile(
        r"(^_*?version_*?\s*=\s*['\"])(\d+\.\d+\.\d+[^\"]*)", re.M
    )
    about_file = pathlib.Path(__file__).parent.parent.joinpath("src/genid/__about__.py")
    try:
        about = about_file.read_text()
    except FileNotFoundError as exc:
        print(f"module not found: '{exc.filename}'")
        sys.exit(1)
    for match in version_regex.finditer(about):
        print(match.group(2))
        return
    print("Failed to extract version from pattern")
    sys.exit(1)


if __name__ == "__main__":
    show_version_string()
