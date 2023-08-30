#!/usr/bin/python3
from __future__ import annotations

import hashlib
from pathlib import Path

from conan_convenience import config
from conan_convenience.helper.downloader.downloader import Downloader


class Local(Downloader):
    def __init__(self) -> None:
        self.path = Path(config.ValidatedConfig.local.path)

    def get(self, origin_file_name: str) -> str:
        with open(self.path / config.ValidatedConfig.path / origin_file_name) as f:
            file = f.read()
        return file
