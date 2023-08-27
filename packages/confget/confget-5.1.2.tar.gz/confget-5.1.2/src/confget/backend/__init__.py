# SPDX-FileCopyrightText: Peter Pentchev <roam@ringlet.net>
# SPDX-License-Identifier: BSD-2-Clause

"""Provide an interface to all the configuration format backends."""

from typing import Dict, Type

from confget import defs

from . import abstract
from . import ini_pyp
from . import ini_re


BACKENDS: Dict[str, Type[abstract.Backend]] = {
    defs.BackendType.INI: ini_pyp.INIPypBackend,
    defs.BackendType.INI_PYP: ini_pyp.INIPypBackend,
    defs.BackendType.INI_REGEX: ini_re.INIRegexBackend,
}
