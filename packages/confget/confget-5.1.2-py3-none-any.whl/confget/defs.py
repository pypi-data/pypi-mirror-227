# SPDX-FileCopyrightText: Peter Pentchev <roam@ringlet.net>
# SPDX-License-Identifier: BSD-2-Clause

"""Common definitions for the confget configuration parsing library."""

import dataclasses
import enum
import sys
from typing import Dict, List, Optional


class BackendType(str, enum.Enum):
    """The supported confget backends."""

    INI = "ini"
    INI_PYP = "ini-pyp"
    INI_REGEX = "ini-regex"

    def __str__(self) -> str:
        """Return a human-readable representation (the string itself)."""
        return self.value


VERSION = "5.1.2"
VERSION_STRING = VERSION
FEATURES = [
    ("BASE", VERSION),
    ("REGEX", "1.0"),
    (
        "REGEX_IMPL_PYTHON",
        f"{sys.version_info[0]}.{sys.version_info[1]}",
    ),
    ("INI_BACKEND", BackendType.INI_PYP),
    ("INI_PYP", "1.0"),
    ("INI_REGEX", "1.0"),
]

SectionData = Dict[str, str]
ConfigData = Dict[str, SectionData]


@dataclasses.dataclass
class Config:
    """Base class for the internal confget configuration."""

    varnames: List[str]
    filename: Optional[str] = None
    section: str = ""
    section_specified: bool = False
    encoding: str = ""
