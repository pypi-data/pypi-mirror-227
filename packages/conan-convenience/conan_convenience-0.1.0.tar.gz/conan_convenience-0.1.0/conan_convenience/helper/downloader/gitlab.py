#!/usr/bin/python3
from __future__ import annotations

from pathlib import PosixPath

import gitlab

from conan_convenience import config
from conan_convenience.helper.downloader.downloader import Downloader


class Gitlab(Downloader):
    def __init__(self) -> None:
        if not config.ValidatedConfig.gitlab.url:
            raise ValueError("Gitlab URL is not set")
        if not config.ValidatedConfig.gitlab.project:
            raise ValueError("Gitlab project is not set")
        pass

    def sha256(self, origin_file_name: str) -> str:
        # private token or personal token authentication and custom URL
        gl = gitlab.Gitlab(
            config.ValidatedConfig.gitlab.url,
            private_token=config.ValidatedConfig.gitlab.token,
        )

        # Get a project by name with namespace
        project = gl.projects.get(config.ValidatedConfig.gitlab.project)

        # Get a project's file
        headers = project.files.head(
            self._urljoin(config.ValidatedConfig.path, origin_file_name),
            ref=config.ValidatedConfig.gitlab.branch,
        )

        return headers["X-Gitlab-Content-Sha256"]

    def get(self, origin_file_name: str) -> str:
        # private token or personal token authentication and custom URL
        gl = gitlab.Gitlab(
            config.ValidatedConfig.gitlab.url,
            private_token=config.ValidatedConfig.gitlab.token,
        )

        # Get a project by name with namespace
        project = gl.projects.get(config.ValidatedConfig.gitlab.project)

        # Get a project's file
        return (
            project.files.get(
                self._urljoin(config.ValidatedConfig.path, origin_file_name),
                ref=config.ValidatedConfig.gitlab.branch,
            )
            .decode()
            .decode("utf-8")
        )
