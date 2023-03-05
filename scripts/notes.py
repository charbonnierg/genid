#!/usr/bin/env python3

import pathlib


def get_notes() -> str:
    changelog = pathlib.Path(__file__).parent.parent / "CHANGELOG.md"
    content = changelog.read_text()
    notes = content.split("\n## ", maxsplit=2)[0]
    return notes.strip()


if __name__ == "__main__":
    print(get_notes())
