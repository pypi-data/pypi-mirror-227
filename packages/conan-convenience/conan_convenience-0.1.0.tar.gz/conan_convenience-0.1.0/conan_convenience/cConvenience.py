#!/usr/bin/python3
from __future__ import annotations

import argparse
import os
import sys
from os import getcwd
from pathlib import Path
from subprocess import run
from subprocess import STDOUT

from conan_convenience import config
from conan_convenience.helper import version
from conan_convenience.helper.conan_cmd_generator import ConanHelper
from conan_convenience.helper.git import GitHelper
from conan_convenience.helper.profile_parsers import ProfileHelper
from conan_convenience.helper.project_helper import ProjectHelper
from conan_convenience.helper.tools import tools_helper
from conan_convenience.ui import UserInterface


class cConvenience:
    def __init__(self):
        self.name = "cConvenience"
        self.description = "Conan Convenience script"
        self.usage = (
            "Just call me when you are in the project directory, no arguments needed."
        )
        self.author = "eph"
        self.argus = self.args().parse_args()
        config.load_config(self.argus.config, self.argus)
        if self.argus.no_ide is not None:
            config.ValidatedConfig.ide_build = not self.argus.no_ide
        self.git = GitHelper()
        config.project_path = self.git.get_project_path(
            Path(self.argus.pdir),
        )
        config.project_name = config.project_path.name
        config.branch_name = self.git.get_current_branch(config.project_path)
        self.tools = tools_helper()
        self.project_helper = ProjectHelper()
        self.profile_helper = ProfileHelper()
        self.conan_helper = ConanHelper()

    @property
    def version(self):
        return version.get_version()

    def args(self) -> argparse.ArgumentParser:
        parser = argparse.ArgumentParser(
            prog=self.name,
            description=self.description,
            epilog=f"Brought to you by {self.author} - Version {self.version}",
        )

        parser.add_argument(
            "pdir",
            nargs="?",
            default=getcwd(),
            metavar="project-dir",
            help="the path to the project directory, defaults"
            + "to the current directory",
        )  # positional argument
        # option that takes a value
        parser.add_argument(
            "-V",
            "--version",
            action="version",
            version=f"%(prog)s {self.version}",
            help="show program's version number and exit",
        )
        parser.add_argument(
            "-l",
            "--list",
            action="store_true",
            help="list all available profiles",
        )
        parser.add_argument(
            "-p",
            "--profile",
            type=int,
            help="explicitly select a profile index (non interactive mode)",
            nargs="*",
        )
        parser.add_argument(
            "-q",
            "--quiet",
            action="store_true",
            help="hide build and install output",
        )
        parser.add_argument(
            "-v",
            "--verbose",
            action="store_true",
            help="show verbose output",
        )
        parser.add_argument(
            "-d",
            "--dirty",
            action="store_true",
            help="do not clean the build directory before building",
        )
        parser.add_argument(
            "-c",
            "--create",
            action="store_true",
            help="create a conan package from the current build directory",
        )
        parser.add_argument(
            "-i",
            "--no_ide",
            action="store_true",
            help="do not set IDE build environment variable",
            default=None,
        )
        parser.add_argument(
            "-w",
            "--windows",
            action="store_true",
            help="build all windows profiles",
            default=False,
        )
        parser.add_argument(
            "-u",
            "--update",
            "--update-config",
            action="store_true",
            help="update conan-convenience",
            default=False,
        )
        parser.add_argument(
            "--config",
            action="store_const",
            help="use a custom config-file",
            default=False,
        )
        return parser

    def worker(self, profile, create, dirty):
        if config.ValidatedConfig.auto_update:
            self._check_for_update()

        if not config.ValidatedConfig.quiet:
            print(f"Selected profile: {profile}")
            print(f"Project name: {config.project_name}")

        if create:
            pkg = self.conan_helper.get_conan_package_name()
            if not config.ValidatedConfig.quiet:
                print(f"Creating package: {pkg}")
                print(f"Running Conan create command: ")
                print(self.conan_helper.get_conan_package_command(pkg, profile))
            if config.ValidatedConfig.verbose:
                run(
                    self.conan_helper.get_conan_package_command(pkg, profile),
                    stderr=STDOUT,
                    shell=True,
                )
            else:
                sub = run(
                    self.conan_helper.get_conan_package_command(pkg, profile),
                    shell=True,
                    capture_output=True,
                )
                if sub.returncode != 0:
                    print(sub.stdout.decode("utf-8"))
            print(f"Package name: {pkg}")
            sys.exit(0)

        if not dirty:
            self.project_helper.remove_build_directory(profile)
        self.git.add_to_gitignore(
            config.project_path,
            self.profile_helper.get_build_directory_name(profile),
        )
        if not config.ValidatedConfig.quiet:
            print(f"Running Conan install command: ")
            print(self.conan_helper.get_conan_install_command(profile))
        if config.ValidatedConfig.verbose:
            run(
                self.conan_helper.get_conan_install_command(
                    profile,
                ),
                stderr=STDOUT,
                shell=True,
            )
        else:
            sub = run(
                self.conan_helper.get_conan_install_command(
                    profile,
                ),
                shell=True,
                capture_output=True,
            )
            if sub.returncode != 0:
                print(sub.stdout.decode("utf-8"))
        if not config.ValidatedConfig.quiet:
            print(f"Running Conan source command: ")
            print(self.conan_helper.get_conan_source_command(profile))
        if config.ValidatedConfig.verbose:
            run(
                self.conan_helper.get_conan_source_command(profile),
                stderr=STDOUT,
                shell=True,
            )
        else:
            sub = run(
                self.conan_helper.get_conan_source_command(profile),
                shell=True,
                capture_output=True,
            )
            if sub.returncode != 0:
                print(sub.stdout.decode("utf-8"))
        if not config.ValidatedConfig.quiet:
            print(f"Running Conan build command: ")
            print(self.conan_helper.get_conan_build_command(profile))
        if config.ValidatedConfig.verbose:
            run(
                self.conan_helper.get_conan_build_command(profile),
                stderr=STDOUT,
                shell=True,
            )
        else:
            sub = run(
                self.conan_helper.get_conan_build_command(profile),
                shell=True,
                capture_output=True,
            )
            if sub.returncode != 0:
                print(sub.stdout.decode("utf-8"))

    def start(self):
        os.chdir(config.project_path)

        if self.tools.check_config_files():
            sys.exit(1)

        profiles = self.profile_helper.get_profiles()

        if self.argus.update:
            self.tools.install_config_files()
            self._check_for_update()

        if self.argus.list:
            self.list_profiles(profiles)
            sys.exit(0)
        elif self.argus.profile:
            for p in self.argus.profile:
                profile = profiles[p]
                self.worker(
                    profile,
                    self.argus.create,
                    self.argus.dirty,
                )
        elif self.argus.windows:
            for p in profiles:
                if "windows-noos" in p or "windows-unittest" in p:
                    profile = profiles[p]
                    self.worker(
                        profile,
                        self.argus.create,
                        self.argus.dirty,
                    )
        else:
            ui = UserInterface()
            profile = ui.select_profile(profiles)
            self.worker(
                profile,
                self.argus.create,
                self.argus.dirty,
            )

    def _check_for_update(self):
        if not config.ValidatedConfig.quiet:
            print("Checking for updates...")
        if config.ValidatedConfig.verbose:
            run(
                "pip install --upgrade conan-convenience",
                stderr=STDOUT,
                shell=True,
            )
        else:
            sub = run(
                "pip install --upgrade conan-convenience",
                shell=True,
                capture_output=True,
            )
            if sub.returncode != 0:
                print(sub.stdout.decode("utf-8"))


def cli():
    try:
        cc = cConvenience()
        cc.start()
    except KeyboardInterrupt:
        print("Keyboard interrupt detected, exiting...")
        sys.exit(1)
    except Exception as e:
        print(e)
        sys.exit(1)


if __name__ == "__main__":
    cli()
