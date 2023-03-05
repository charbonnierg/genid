# Project scripts

## Available scripts

The following scripts are used within the project:

- [`install.py`](#installpy): install the python project
- [`notes.py`](#notespy): show release notes for the latest release only
- [`release.py`](#releasepy): used by [`semantic-release`](https://semantic-release.gitbook.io/semantic-release/) through [@semantic-release/exec](https://github.com/semantic-release/exec) plugin to prepare and publish a new release.
- [`version.py`](#versionpy): display project version.

### [`install.py`](./install.py)

The [`install.py`](./install.py) script can be used to install the python project.

It accepts two arguments:

- `-e` or `--extras`: a string of comma-separated extras such as `"dev,docs,test"`.
- `-a` or `--all`: a boolean flag indicating that all extras should be installed.

Example usage:

- Install with build extra only (default behaviour)

```console
python3 scripts/install.py
```

- Install some extras only

```console
python3 scripts/install.py --extras build,dev
```

- Install all extras

```console
python3 scripts/install.py --all
```

## [`notes.py`](./notes.py)

The [`notes.py`](./notes.py) script can be used to output in console the release notes for the latest release only.

This script does not accept argument.

Example usage:

```console
python3 scripts/notes.py
```

> The script is used in [Github Release workflow](../.github/workflows/github_release.yml) in order to generate the release body.

## [`release.py`](./release.py)

The [`release.py`](./release.py) script is meant to be used by [`semantic-release`](https://semantic-release.gitbook.io/semantic-release/) through [@semantic-release/exec](https://github.com/semantic-release/exec) plugin.

It is responsible for implementing the 3 steps:

- `prepareCmd`: Prepare the release (before semantic-release creates a new tag).

- `publishCmd`: Publish the release as a git branch.

- `successCmd`: Perform arbitrary actions after successful publish.

> The semantic-release configuration file `[release.config.js](../release.config.js)` references the [`release.py`](./release.py) script in plugins configuration block.

## [`version.py`](./version.py)

The [`version.py`](./version.py) can be used to display the project version. It does not accept any argument, and simply print current version found in `__about__.py` module into standard output.
