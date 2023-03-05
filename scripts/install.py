#!/usr/bin/env python3

"""Install the project in editable mode."""

import argparse
import os
import pathlib
import subprocess
import sys
import venv

PROJECT_DIR = pathlib.Path(__file__).parent.parent.resolve(True)
VENV_DIR = PROJECT_DIR / ".venv"


if os.name == "nt":
    VENV_PYTHON = VENV_DIR / "Scripts" / "python.exe"
else:
    VENV_PYTHON = VENV_DIR / "bin" / "python"


def install_virtualenv() -> None:
    """Create a virtualenv and install dependencies"""
    venv.create(
        VENV_DIR,
        system_site_packages=False,
        clear=False,
        with_pip=True,
        prompt=None,
    )
    try:
        subprocess.run(
            [
                VENV_PYTHON,
                "-m",
                "pip",
                "install",
                "-U",
                "pip",
                "setuptools",
                "wheel",
            ]
        )
    except Exception:
        # No need to print traceback, error will be printed from subprocess stderr
        sys.exit(1)


def install_project(extras: str = "") -> None:
    """Installing project in editable mode using pip"""
    cmd = [
        VENV_PYTHON,
        "-m",
        "pip",
        "install",
        "-e",
        PROJECT_DIR.as_posix() + (f"[{extras}]" if extras else ""),
    ]
    try:
        subprocess.run(cmd)
    except Exception:
        # No need to print traceback, error will be printed from subprocess stderr
        sys.exit(1)


cli_parser = argparse.ArgumentParser(
    description=(
        "Create or update virtual environment in project root directory then "
        "install project."
    )
)
cli_parser.add_argument(
    "--no-build",
    action="store_true",
    required=False,
    default=False,
    help="Do not install build dependencies",
)
cli_parser.add_argument(
    "--dev",
    action="store_true",
    required=False,
    default=False,
    help="Install development extras",
)
cli_parser.add_argument(
    "--docs",
    action="store_true",
    required=False,
    default=False,
    help="Install documentation extras",
)
cli_parser.add_argument(
    "-e",
    "--extras",
    type=str,
    required=False,
    default=None,
    help="Install additional extras",
)
cli_parser.add_argument(
    "-a",
    "--all",
    action="store_true",
    required=False,
    default=False,
    help="Install all extras",
)
cli_parser.add_argument(
    "--show-python-path",
    action="store_true",
    required=False,
    default=False,
    help="Show path to python interpreter within virtual environment and exit",
)

if __name__ == "__main__":
    args = cli_parser.parse_args()
    # Show venv
    if args.show_python_path:
        print(VENV_PYTHON.as_posix())
        sys.exit(0)
    # Parse arguments
    extras = set(args.extras.split(",")) if args.extras else set()
    # First make sure virtualenv exists
    install_virtualenv()
    # Gather extras
    if not args.no_build:
        extras = extras.union(set(["build"]))
    if args.dev:
        extras = extras.union(set(["dev", "build"]))
    if args.docs:
        extras = extras.union(set(["docs", "build"]))
    if args.all:
        extras = extras.union(set(["dev", "docs", "build"]))
    # Install project in development mode
    install_project(",".join(extras))
