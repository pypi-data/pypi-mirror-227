#!/usr/bin/python3
from __future__ import annotations

import os
import shutil
from pathlib import Path

from conan_convenience import config
from conan_convenience.helper.git import GitHelper
from conan_convenience.helper.profile_parsers import ProfileHelper


class ProjectHelper:
    def __init__(self) -> None:
        self.git = GitHelper()
        self.ph = ProfileHelper()

    def remove_build_directory(self, profile: Path) -> None:
        directory = config.project_path / self.ph.get_build_directory_name(profile)
        if directory.exists():
            if not config.ValidatedConfig.quiet:
                print(f"Build directory found, cleaning up...")
            if config.ValidatedConfig.verbose:
                self._print_tree(directory)
                print(f"Removing {str(directory)}")
            shutil.rmtree(directory)

    def _print_tree(self, path: Path) -> None:
        for root, dirs, files in os.walk(path):
            level = root.replace(path, "").count(os.sep)
            indent = " " * 4 * (level)
            print(f"{indent}{os.path.basename(root)}/")
            subindent = " " * 4 * (level + 1)
            for f in files:
                print(f"{subindent}{f}")
