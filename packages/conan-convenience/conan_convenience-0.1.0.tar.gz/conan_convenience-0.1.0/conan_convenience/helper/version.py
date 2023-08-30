#!/usr/bin/python3
from __future__ import annotations

import sys
import tomllib
from functools import cache
from importlib import metadata
from pathlib import Path

__version__ = None


@cache
def project_root() -> Path:
    """Find the project root directory by locating pyproject.toml."""
    current_file = Path(__file__)
    for parent_directory in current_file.parents:
        if (parent_directory / "pyproject.toml").is_file():
            return parent_directory
    raise FileNotFoundError("Could not find project root containing pyproject.toml")


def get_version() -> str:
    """Get the version of the package."""
    try:
        # Probably this is a regular install
        global __version__
        __version__ = metadata.version("conan_convenience")
    except metadata.PackageNotFoundError:
        pass
    try:
        # Probably this is the pyproject.toml of a development install
        path_to_pyproject_toml = project_root() / "pyproject.toml"
    except FileNotFoundError:
        # Probably not a development install
        path_to_pyproject_toml = None

    if path_to_pyproject_toml is not None:
        with open(path_to_pyproject_toml, "rb") as f:
            pyproject_version = tomllib.load(f)["tool"]["poetry"]["version"]
        if __version__ is None:
            # This is a development install
            __version__ = pyproject_version
        if pyproject_version != __version__:
            raise ValueError(
                f"pyproject.toml version ({pyproject_version}) does not match __version__ "
                f"({__version__}). Please reinstall the package to avoid inconsistencies. "
                f"For example, run\n  pip install --no-deps --editable {project_root()}",
            )
    return __version__
