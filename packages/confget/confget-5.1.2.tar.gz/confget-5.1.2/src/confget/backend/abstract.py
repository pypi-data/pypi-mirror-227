# SPDX-FileCopyrightText: Peter Pentchev <roam@ringlet.net>
# SPDX-License-Identifier: BSD-2-Clause

"""An abstract metaclass for confget backends."""

import abc
import configparser

from confget import defs


class Backend(metaclass=abc.ABCMeta):
    """An abstract confget parser backend."""

    def __init__(self, cfg: defs.Config) -> None:
        """Store the runtime configuration, leave the rest to the implementation."""
        self._cfg = cfg

    @abc.abstractmethod
    def read_file(self) -> defs.ConfigData:
        """Read and parse the configuration file, invoke the callbacks."""
        raise NotImplementedError("Backend.read_file")

    @abc.abstractmethod
    def get_dict(self) -> defs.ConfigData:
        """Return the sections and values from the configuration file."""
        raise NotImplementedError("Backend.get_dict")

    def get_configparser(self) -> configparser.ConfigParser:
        """Return a ConfigParser object with the parsed values."""
        par = configparser.ConfigParser(interpolation=None)
        par.read_dict(self.get_dict())
        return par
