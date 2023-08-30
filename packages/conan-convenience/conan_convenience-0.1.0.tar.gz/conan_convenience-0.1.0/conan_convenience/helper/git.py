#!/usr/bin/python3
from __future__ import annotations

from pathlib import Path

from conan_convenience import config


class GitHelper:
    def __init__(self) -> None:
        self.gitignore_info_text = config.ValidatedConfig.gitignore_info_text

    def add_to_gitignore(self, path: Path, needle: str) -> None:
        ignore_file = self.find_git_dir(path) / ".gitignore"

        contents = []
        if ignore_file.exists():
            with open(ignore_file) as f:
                contents = f.read().splitlines()

        try:
            from gitignore_parser import parse_gitignore

            matches = parse_gitignore(ignore_file)
            if matches(needle):
                if config.ValidatedConfig.verbose:
                    print(f"{needle} already in .gitignore")
                return
        except:
            for line in contents:
                if needle.strip() == line.strip():
                    if config.ValidatedConfig.verbose:
                        print(f"{needle} already in .gitignore")
                    return
        new_contents = self._insert_after_section(contents, needle)
        # end with a new line
        if new_contents[-1] != "":
            new_contents.append("")
        with open(ignore_file, "w") as f:
            f.write("\n".join(new_contents))

    def get_current_branch(self, path: Path) -> str:
        head_dir = self.find_git_dir(path) / ".git" / "HEAD"
        with head_dir.open("r") as f:
            content = f.read().splitlines()

        for line in content:
            if line[0:4] == "ref:":
                return line.partition("refs/heads/")[2]

    def get_project_path(self, path: Path) -> str:
        search_path = path
        while (git_dir := self.find_git_dir(path)) != None:
            # check for profiles directory
            if (git_dir / "profiles").exists():
                if not config.ValidatedConfig.quiet:
                    print(f"Found project directory: {git_dir}")
                return git_dir
            if config.ValidatedConfig.verbose:
                print(
                    f"Could not find profiles directory in {git_dir}, moving up...",
                )
            search_path = search_path.parent
        raise Exception(f"Could not find profiles directory in {path}...")

    def find_git_dir(self, path: Path) -> Path:
        if (path / ".git").exists():
            return path
        elif path.parent == path:
            return None
        else:
            return self.find_git_dir(path.parent)

    def _insert_after_section(self, ignore_contents: list, needle: str) -> list:
        section_idx = self._find_section(ignore_contents)
        if section_idx is None:
            ignore_contents.append("")
            ignore_contents.append(self.gitignore_info_text)
            ignore_contents.append(needle)
            ignore_contents.append("")
        else:
            ignore_contents.insert(section_idx + 1, needle)
        return ignore_contents

    def _find_section(self, ignore_contents: list):
        for idx, line in enumerate(ignore_contents):
            if line.strip() == self.gitignore_info_text.strip():
                return idx
        return None
