#!/usr/bin/env python3

"""Automate release management."""

import argparse
import os
import pathlib
import re
import subprocess
import sys

# Define release candidate branch name
RC_BRANCH_NAME = os.environ.get("RC_BRANCH_NAME", "next")
RELEASE_BRANCH_NAME = os.environ.get("STABLE_BRANCH_NAME", "main")


def update_version_string(new_version: str) -> None:
    """Update version string found in __about__.py module"""
    version_regex = re.compile(
        r"(^_*?version_*?\s*=\s*['\"])(\d+\.\d+\.\d+[^\"]*)", re.M
    )
    about = pathlib.Path(__file__).parent.parent.joinpath(
        "src/genid/__about__.py"
    )
    with about.open("r+") as about_file:
        content = about_file.read()
        about_file.seek(0)
        about_file.write(
            re.sub(
                version_regex,
                lambda match: "{}{}".format(match.group(1), new_version),
                content,
            )
        )
        about_file.truncate()


def run(cmd: str) -> None:
    """Run a command using shell mode and check the return code."""
    p = subprocess.run(cmd, shell=True)
    p.check_returncode()


def prepare_release(version: str, branch: str) -> None:
    """Prepare the release:

    1. Checkout target branch
    2. Update version string
    3. Add updated files
    4. Commit changes (disable CI)
    """
    run(f"git checkout {branch}")
    # Update version using function defined above
    update_version_string(new_version=version)
    # At this point semantic release already performed a commit
    run("git add .")
    # Commit changes to the current branch
    run(f"git commit -m 'chore(release): bump to version {version}' --no-verify")


def publish_release(branch: str) -> None:
    """Publish the release (push to git repo)."""
    # Checkout release branch
    run(f"git checkout {branch}")
    # Push release branch to remote
    run(f"git push origin {branch}")


def on_success(branch: str) -> None:
    """Merge changes back into next on success on releases only (I.E, not on release candidates)."""
    if branch == RELEASE_BRANCH_NAME:
        # Checkout release candidate branch ("next" by default)
        run(
            f"git switch -c {RC_BRANCH_NAME} 2>/dev/null || git checkout {RC_BRANCH_NAME}"
        )
        # Merge changes from release branch
        run(
            f"git merge --no-ff origin/{branch} -m 'chore(release): merge from {RELEASE_BRANCH_NAME} branch [skip ci]'"
        )
        # Push changes into release candidate branch ("next" by default)
        run(f"git push origin {RC_BRANCH_NAME}")


cli_parser = argparse.ArgumentParser(description="Semantic release step runner")
cli_parser.add_argument("step", type=str)
cli_parser.add_argument("--version", type=str, required=True)
cli_parser.add_argument("--branch", type=str, required=True)


if __name__ == "__main__":
    # The script expects a single positional argument
    args = cli_parser.parse_args()
    # Parse arguments
    step: str = args.step
    version: str = args.version
    branch: str = args.branch
    # Execute function based on received "step" value:
    if step == "prepare":
        prepare_release(version, branch)
    elif step == "publish":
        publish_release(branch)
    elif step == "success":
        on_success(branch)
    else:
        print(
            "ERROR: Invalid argument. Allowed values: ['prepare', 'publish', 'success']"
        )
        sys.exit(1)
