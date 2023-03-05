"""Generate the code reference pages and navigation."""

import sys
from pathlib import Path

import mkdocs_gen_files
import urllib3

nav = mkdocs_gen_files.Nav()

for path in sorted(Path("src").rglob("*.py")):
    module_path = path.relative_to("src").with_suffix("")
    doc_path = path.relative_to("src").with_suffix(".md")
    full_doc_path = Path("reference", doc_path)

    parts = tuple(module_path.parts)

    if parts[-1] == "__init__":
        parts = parts[:-1]
        doc_path = doc_path.with_name("index.md")
        full_doc_path = full_doc_path.with_name("index.md")
    elif parts[-1] == "__main__":
        continue

    nav[parts] = doc_path.as_posix()

    with mkdocs_gen_files.open(full_doc_path, "w") as fd:
        ident = ".".join(parts)
        fd.write(f"::: {ident}")

    mkdocs_gen_files.set_edit_path(full_doc_path, path)

with mkdocs_gen_files.open("reference/SUMMARY.md", "w") as nav_file:
    nav_file.writelines(nav.build_literate_nav())


with mkdocs_gen_files.open("CHANGELOG.md", "w") as changelog_file:
    changelog = Path("CHANGELOG.md")
    if changelog.is_file():
        changelog_file.write(changelog.read_text())
    else:
        changelog_file.write("No version released yet")


with mkdocs_gen_files.open("LICENSE.md", "w") as license_file:
    http = urllib3.PoolManager()
    LICENSE = "MIT"
    response = http.request(
        "GET",
        f"https://raw.githubusercontent.com/spdx/license-list-data/main/text/{LICENSE}.txt",
    )
    data = response.data.decode("utf-8")
    if response.status != 200:
        print("Failed to fetch license:", file=sys.stderr)
        print(data, file=sys.stderr)
        sys.exit(1)
    license_file.write(
        data.replace("[yyyy]", "2023").replace(
            "[name of copyright owner]", "Guillaume Charbonnier"
        )
    )
