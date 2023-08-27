# SPDX-FileCopyrightText: Peter Pentchev <roam@ringlet.net>
# SPDX-License-Identifier: BSD-2-Clause

"""Run the confget tests using the Python methods.

Load the test data, then run the tests using the objects provided by
the Python library, not by executing the command-line tool.
"""

import itertools
import pathlib
from typing import Dict
from unittest import mock

import pytest

import confget
from confget import format as cformat

from .data import test_defs as tdefs
from .data import test_load as tload


TESTS = tload.load_all_tests(tdefs.get_test_path(None))

FULL_TEST_DATA_BEFORE_RIF = [
    (fname, test)
    for fname, idx, test in sorted(
        itertools.chain(
            *[
                [(tfile[0], idx, test) for idx, test in enumerate(tfile[1].tests)]
                for tfile in TESTS.items()
            ]
        )
    )
]

FULL_TEST_DATA = list(
    itertools.chain(
        *[
            [(str(fname), use_rif, test) for use_rif in (False, True)]
            for fname, test in FULL_TEST_DATA_BEFORE_RIF
        ]
    )
)

SKIP_ARGS = {"check_only"}


# We keep the fname parameter for visibility in the test logs.
# Also, this function is only ever invoked on the test data we built above, so
# there will hopefully be no confusion about the boolean parameter.
@pytest.mark.parametrize(("fname", "use_rif", "test"), FULL_TEST_DATA)
def test_run(fname: str, use_rif: bool, test: tdefs.SingleTestDef) -> None:  # noqa: ARG001,FBT001
    """Instantiate a confget object, load the data, check it."""
    if set(test.args.keys()) & SKIP_ARGS:
        return
    if use_rif and not test.backend.startswith("ini"):
        return

    config = test.get_config()

    def get_file_data() -> Dict[str, Dict[str, str]]:
        """Read the file data: backend or read_ini_file()."""
        if use_rif:
            return confget.read_ini_file(config)

        backend = test.get_backend()
        obj = backend(config)
        return obj.read_file()

    if test.stdin:
        infile = tdefs.get_test_path(test.stdin)
        with mock.patch("sys.stdin", new=pathlib.Path(infile).open(encoding="UTF-8")):
            data = get_file_data()
    else:
        data = get_file_data()

    res = cformat.filter_vars(config, data)
    output = test.do_xform(line for line in res)
    test.output.check_result(output)
