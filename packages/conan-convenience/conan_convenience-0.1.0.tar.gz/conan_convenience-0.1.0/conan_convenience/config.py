#!/usr/bin/python3
from __future__ import annotations

from pathlib import Path

import confuse

from conan_convenience.helper.downloader.downloader import Downloader


template = {
    "configuration_files": confuse.StrSeq(),
    "provider": confuse.OneOf(["gitlab", "http", "local"]),
    "gitlab": confuse.Optional(
        {
            "url": confuse.Optional("https://gitlab.com"),
            "token": confuse.Optional(str),
            "project": str,
            "branch": confuse.Optional("master"),
        },
    ),
    "http": confuse.Optional(
        {"url": str},
    ),
    "local": confuse.Optional(
        {"path": str},
    ),
    "path": confuse.Optional(""),
    "dependencies": confuse.Optional(confuse.StrSeq()),
    "gitignore_info_text": confuse.Optional(
        "# This section is managed by conan-convenience",
    ),
    "update_gitignore": confuse.Optional(True),
    "auto_update": confuse.Optional(True),
    "ide_prefix": confuse.Optional("clion"),
    "ide_build": confuse.Optional(True),
    "verbose": confuse.Optional(False),
    "quiet": confuse.Optional(False),
}
_config = None
ValidatedConfig = None
branch_name = "unknown"
project_name = "unknown"
project_path = Path(".")


def load_config(custom_config_file: str = None, args: list = None) -> None:
    global _config
    _config = confuse.Configuration("conan_convenience", __name__)
    if custom_config_file:
        _config.set_file(custom_config_file)
    _config.set_args(args, dots=True)
    # TODO add config file as parameter
    global ValidatedConfig
    ValidatedConfig = _config.get(template)


def get(key: str):
    global _config
    return _config[key]


def get_downloader() -> Downloader:
    if ValidatedConfig.provider == "gitlab":
        from conan_convenience.helper.downloader.gitlab import Gitlab

        return Gitlab()
    elif ValidatedConfig.provider == "http":
        from conan_convenience.helper.downloader.http import Http

        return Http()
    elif ValidatedConfig.provider == "local":
        from conan_convenience.helper.downloader.local import Local

        return Local()
    else:
        raise ValueError(f"Unknown provider: {ValidatedConfig.provider}")
