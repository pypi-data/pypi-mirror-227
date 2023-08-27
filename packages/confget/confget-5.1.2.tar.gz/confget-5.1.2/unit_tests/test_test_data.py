# SPDX-FileCopyrightText: Peter Pentchev <roam@ringlet.net>
# SPDX-License-Identifier: BSD-2-Clause

"""Make sure the test data is up to date."""

import pathlib
from typing import Set


def test_test_data() -> None:
    """Compare the test data to the one in the source t/ directory."""

    def get_files(path: pathlib.Path) -> Set[pathlib.Path]:
        """Get the relevant files from the test data directory."""
        tdefs = path / "defs/tests"
        files_ini = set(path.glob("*.ini"))
        files_tests = set(tdefs.glob("*.json"))
        assert files_ini
        assert files_tests
        files = files_ini | files_tests
        assert (path.is_file() for path in files)
        return files

    local = pathlib.Path(__file__).parent.parent / "test_data"
    local_tests = get_files(local)

    upstream = pathlib.Path(__file__).parent.parent.parent / "t"
    if not upstream.is_dir():
        return
    upstream_tests = get_files(upstream)

    for test in sorted(upstream_tests):
        local_test = local / test.relative_to(upstream)
        assert local_test.is_file()
        assert local_test.read_text(encoding="UTF-8") == test.read_text(encoding="UTF-8")

    for test in sorted(local_tests):
        upstream_test = upstream / test.relative_to(local)
        assert upstream_test.is_file()
