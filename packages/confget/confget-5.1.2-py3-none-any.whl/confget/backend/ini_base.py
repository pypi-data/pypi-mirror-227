# SPDX-FileCopyrightText: Peter Pentchev <roam@ringlet.net>
# SPDX-License-Identifier: BSD-2-Clause

"""A base class for confget backends for reading INI-style files."""

import abc
import locale
import pathlib
import sys
from typing import IO

from confget import defs

from . import abstract


class INIBackendBase(abstract.Backend, metaclass=abc.ABCMeta):
    """Parse INI-style configuration files."""

    STDIN_NAME = "-"

    encoding: str
    parsed: defs.ConfigData

    def __init__(self, cfg: defs.Config) -> None:
        """Validate the filename and the encoding (either specified or detected)."""
        super().__init__(cfg)

        if self._cfg.filename is None:
            raise ValueError("No config filename specified")

        encoding = self._cfg.encoding if self._cfg.encoding else locale.nl_langinfo(locale.CODESET)
        if not encoding:
            raise ValueError("No encoding specified or defined for the current locale")

        self.encoding = encoding
        self.parsed = {}

    def open_file(self) -> IO[str]:
        """Open the requested file or input stream."""
        assert self._cfg.filename is not None  # noqa: S101  # mypy needs this
        if self._cfg.filename == self.STDIN_NAME:
            # We can't use sys.stdin.reconfigure() on Python 3.6
            return open(  # noqa: SIM115,PTH123
                sys.stdin.fileno(), encoding=self.encoding, closefd=False
            )

        return pathlib.Path(self._cfg.filename).open(encoding=self.encoding)  # noqa: SIM115

    def get_dict(self) -> defs.ConfigData:
        """Return the sections and values from the configuration file."""
        return {item[0]: dict(item[1]) for item in self.parsed.items()}
