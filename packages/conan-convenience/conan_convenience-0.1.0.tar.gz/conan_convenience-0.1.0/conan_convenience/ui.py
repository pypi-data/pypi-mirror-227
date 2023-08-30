#!/usr/bin/python3
from __future__ import annotations

from pathlib import Path

from conan_convenience import config
from conan_convenience.helper.tools import tools_helper


class UserInterface:
    def __init__(self) -> None:
        pass

    def list_profiles(self, profiles: list) -> None:
        if len(profiles) == 0:
            raise Exception("No profiles found.")
        for idx, profile in enumerate(profiles):
            print(f"{idx}. {profile.name}")

    def select_profile(self, profiles: list) -> Path:
        self.list_profiles(profiles)
        print("A  abort")
        print("I  install configurations")
        print("Select profile: ", end="")
        selection = input()
        if not selection.isdigit():
            if selection.upper() == "A":
                return None
            elif selection.upper() == "I":
                th = tools_helper()
                th.install_config_files(
                    config.project_path,
                    quite=True,
                    verbose=False,
                )
                return None
            else:
                raise Exception("Invalid selection.")
        idx = int(selection)
        return profiles[idx]
