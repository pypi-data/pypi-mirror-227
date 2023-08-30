#!/usr/bin/python3
from __future__ import annotations

from pathlib import Path

from conan_convenience import config
from conan_convenience.helper.profile_parsers import ProfileHelper


class ConanHelper:
    def __init__(self) -> None:
        self.ph = ProfileHelper()

    def get_conan_install_command(self, profile: Path) -> str:
        build_directory = self.ph.get_build_directory_name(profile)
        project = config.project_name.upper().replace("-", "_")
        if config.ValidatedConfig.ide_build:
            return f"conan install . -if {build_directory} -pr {profile.name} -e {project}_IDE_BUILD=1"
        return f"conan install . -if {build_directory} -pr {profile.name}"

    def get_conan_build_command(self, profile: Path) -> str:
        build_directory = self.ph.get_build_directory_name(profile)
        return f"conan build . -bf {build_directory}"

    def get_conan_source_command(self, profile: Path) -> str:
        build_directory = self.ph.get_build_directory_name(profile)
        return f"conan source . -if {build_directory}"

    def get_conan_package_name(self) -> str:
        project = config.project_name
        branch = (
            config.branch_name.replace(
                "/",
                "_",
            )
            .replace("-", "_")
            .split("_")
        )
        tag = branch[0]
        if len(branch) > 1:
            feature = ".".join(branch[1:])
        else:
            feature = "unspecified"
        version = f"0.1.0-{feature[:40]}"
        return f"{project}/{version}@local/{tag}"

    def get_conan_package_command(self, package_name: str, profile: Path) -> str:
        return f"conan create . {package_name} -pr {profile.name}"
