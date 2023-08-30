#!/usr/bin/python3
from __future__ import annotations

import hashlib
from pathlib import Path


class VirtualException(BaseException):
    def __init__(self, _type, _func):
        BaseException(self)


class Downloader:
    def __init__(self) -> None:
        pass

    def download_file(self, origin_file_name: str, destination: Path) -> None:
        content = self.get(origin_file_name)
        with open(destination, "w") as f:
            f.write(content)

    def get(self, origin_file_name: str) -> str:
        raise VirtualException()

    def sha256(self, origin_file_name: str) -> str:
        return hashlib.sha256(
            self.get(origin_file_name).encode(
                "utf-8",
            ),
        ).hexdigest()

    def _urljoin(self, base: str, *args: str) -> str:
        result = base
        for arg in args:
            if not arg:
                continue
            if arg.startswith("/"):
                result = result.rstrip("/") + arg
            elif result == "":
                result = arg
            else:
                result = result + "/" + arg
        return result
