#!/usr/bin/python3
from __future__ import annotations

import re
from pathlib import Path

from conan_convenience import config


class ProfileHelper:
    def __init__(self) -> None:
        pass

    def get_profiles(self) -> list:
        profile_path = config.project_path / "profiles"
        if not profile_path.exists():
            raise Exception(
                f"Path does not exist: {profile_path}\nPlease make sure this is a project directory and try again.",
            )
        if not config.ValidatedConfig.quiet:
            print(f"Searching for profiles in {profile_path}...")
        return sorted(profile_path.rglob("*.profile"))

    def get_profile_params(self, profile: Path) -> dict:
        params = profile.name.rsplit(".", maxsplit=1)[0].split("-")
        buildTypeIdx = (
            params.index("debug")
            if "debug" in params
            else params.index(
                "release",
            )
            if "release" in params
            else len(params)
        )
        res = {"task": "build"}

        # left of build type
        # linux-release.profile
        res["buildOS"] = params[0]
        if buildTypeIdx < len(params):
            res["buildType"] = params[buildTypeIdx]
        if buildTypeIdx > 1:
            # windows-noos-debug.profile
            # linux-noos-release.profile
            res["hostOS"] = params[1]
            # windows-unittest.profile
            if params[1] == "unittest":
                res["task"] = "development"
        if buildTypeIdx > 2:
            # linux-noos-2954a-debug.profile
            # windows-noos-2954b-release.profile
            res["board"] = params[2]

        # right of build type
        # windows-noos-debug-baseio.profile
        # windows-noos-nucleo_u575-debug.profile
        if len(params) > buildTypeIdx + 1:
            res["flavour"] = params[buildTypeIdx + 1]
        return res

    def get_build_directory_name(self, profile: Path) -> str:
        # [(ide_prefix)/cmake]-[task]-[buildOS]-[hostOS]-[board]-[flavour]-[buildType]
        params = self.get_profile_params(profile)
        build_directory = [
            config.ValidatedConfig.ide_prefix
            if config.ValidatedConfig.ide_build
            else "cmake",
            params.get(
                "task",
            ),
            params.get("buildOS"),
            params.get("hostOS"),
            params.get("board"),
            params.get("flavour"),
            params.get("buildType"),
        ]
        return "-".join([i for i in build_directory if i is not None])
