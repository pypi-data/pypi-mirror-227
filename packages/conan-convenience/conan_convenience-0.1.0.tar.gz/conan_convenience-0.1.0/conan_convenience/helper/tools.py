#!/usr/bin/python3
from __future__ import annotations

import filecmp
import hashlib
from pathlib import Path
from subprocess import run
from subprocess import STDOUT

from conan_convenience import config
from conan_convenience.helper.downloader.downloader import Downloader
from conan_convenience.helper.git import GitHelper


class tools_helper:
    def __init__(self) -> None:
        self.files = config.ValidatedConfig.configuration_files
        self.downloader = config.get_downloader()

    def download_file(
        self,
        destination: Path,
        dry_run: bool = True,
    ) -> bool:
        if destination.is_file():
            with open(destination) as f:
                file = f.read()
            hash = hashlib.sha256((file).encode("utf-8")).hexdigest()
            if hash == self.downloader.sha256(destination.name):
                if not config.ValidatedConfig.quiet:
                    print(f"{destination} file already up to date.")
                return True
            elif dry_run:
                if not config.ValidatedConfig.quiet:
                    print(
                        f"{destination} is out of date, please update to the latest version...",
                    )
                return False
        elif dry_run:
            print(f"{destination} file does not exist...")
            return False
        if not config.ValidatedConfig.quiet:
            print(f"Writing {destination} file...")
        self._backup_file(destination)
        self.downloader.download_file(destination.name, destination)
        GitHelper().add_to_gitignore(destination)
        return True

    def install_config_files(self) -> None:
        for config_file in self.files:
            self.download_file(
                config.project_path / config_file,
                dry_run=False,
            )
            if config_file == ".pre-commit-conf.yml":
                self.install_pre_commit_hooks(config.project_path)

    def check_config_files(self) -> bool:
        requires_update = False
        for config_file in self.files:
            if not self.download_file(
                config.project_path / config_file,
                dry_run=True,
            ):
                requires_update = True
            if config_file == ".pre-commit-conf.yml":
                if not self.check_pre_commit_hooks(config.project_path):
                    requires_update = True
        if requires_update:
            raise Exception(
                "Please update your config files to the latest version. "
                "Run 'conan-convenience --update-config' to update them.",
            )
        return requires_update

    def install_pre_commit_hooks(self) -> None:
        if config.ValidatedConfig.verbose:
            print("Running 'pre-commit install'...")
            run(
                "pre-commit install",
                stderr=STDOUT,
                shell=True,
            )
            print("Running 'pre-commit autoupdate'...")
            run(
                "pre-commit autoupdate",
                stderr=STDOUT,
                shell=True,
            )
        else:
            sub = run(
                "pre-commit install",
                shell=True,
                capture_output=True,
            )
            if sub.returncode != 0:
                print(sub.stdout.decode("utf-8"))
            sub = run(
                "pre-commit autoupdate",
                shell=True,
                capture_output=True,
            )
            if sub.returncode != 0:
                print(sub.stdout.decode("utf-8"))

    def check_pre_commit_hooks(self) -> bool:
        if config.ValidatedConfig.verbose:
            print("Running 'pre-commit autoupdate'...")
            run(
                "pre-commit autoupdate",
                stderr=STDOUT,
                shell=True,
            )
        else:
            sub = run(
                "pre-commit autoupdate",
                shell=True,
                capture_output=True,
            )
            if sub.returncode != 0:
                print(sub.stdout.decode("utf-8"))
        return True

    def _backup_file(self, filename: Path) -> None:
        if filename.is_file():
            backup_name = filename.with_name(f"{filename.name}.old")
            if config.ValidatedConfig.verbose:
                print("Backing up old file...")
            cnt = 1
            while backup_name.exists():
                backup_name = filename.with_name(f"{filename.name}.old.{cnt}")
                if filecmp.cmp(filename, backup_name, shallow=False):
                    if not config.ValidatedConfig.quiet:
                        print("Backup already exists, skipping...")
                    return
                cnt += 1
            filename.rename(backup_name)
