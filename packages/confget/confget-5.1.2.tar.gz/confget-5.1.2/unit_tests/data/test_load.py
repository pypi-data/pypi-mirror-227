# SPDX-FileCopyrightText: Peter Pentchev <roam@ringlet.net>
# SPDX-License-Identifier: BSD-2-Clause

"""Load a test definition from a JSON file."""

import json
import os
import pathlib
from typing import Any, Dict

from . import test_defs as tdefs


def _load_test_v2(data: Dict[str, Any], _version: Dict[str, int]) -> tdefs.FileDef:
    """Load the tests from a v2.x test file."""
    build: Dict[str, Any] = {"tests": []}

    for test in data["tests"]:
        raw = {
            key: value
            for key, value in test.items()
            if key in {"args", "keys", "xform", "backend", "stdin"}
        }

        if "exact" in test["output"]:
            raw["output"] = tdefs.ExactOutputDef(exact=test["output"]["exact"])
        elif "exit" in test["output"]:
            raw["output"] = tdefs.ExitOKOutputDef(success=test["output"]["exit"])
        else:
            raise ValueError("test output: " + repr(test["output"]))

        build["tests"].append(tdefs.SingleTestDef(**raw))

    return tdefs.FileDef(**build)


_PARSERS = {2: _load_test_v2}


def load_test(fname: str) -> tdefs.FileDef:
    """Load a single test file into a TestFileDef object."""
    with pathlib.Path(fname).open(encoding="UTF-8") as testf:
        data = json.load(testf)

    version = {
        "major": data["format"]["version"]["major"],
        "minor": data["format"]["version"]["minor"],
    }
    assert isinstance(version["major"], int)
    assert isinstance(version["minor"], int)

    parser = _PARSERS.get(version["major"], None)
    if parser is not None:
        return parser(data, version)
    raise NotImplementedError(
        f"Unsupported test format version {version['major']}.{version['minor']} for {fname}"
    )


def load_all_tests(testdir: str) -> Dict[pathlib.Path, tdefs.FileDef]:
    """Load all the tests in the defs/tests/ subdirectory."""
    tdir = testdir + "/defs/tests/"
    filenames = sorted(fname for fname in os.listdir(tdir) if fname.endswith(".json"))
    return {pathlib.Path(fname).with_suffix(""): load_test(tdir + fname) for fname in filenames}
