#!/usr/bin/python3
from __future__ import annotations

from pathlib import PosixPath

import requests

from conan_convenience import config
from conan_convenience.helper.downloader.downloader import Downloader


class Http(Downloader):
    def __init__(self) -> None:
        if not config.ValidatedConfig.http.url.startswith("http"):
            raise ValueError("url must start with http or https")

    def get(self, origin_file_name: str) -> str:
        full_url = self._urljoin(
            config.ValidatedConfig.http.url,
            config.ValidatedConfig.path,
            origin_file_name,
        )
        req = requests.get(full_url)

        return req.text
