# SPDX-FileCopyrightText: Peter Pentchev <roam@ringlet.net>
# SPDX-License-Identifier: BSD-2-Clause

"""Test that the backends return ConfigParser objects."""

import confget

from .data import test_defs as tdefs


def test_ini() -> None:
    """Test the ConfigParser object returned by the INI file backend."""
    cfg = confget.Config([], filename=tdefs.get_test_path("t3.ini"))
    ini = confget.BACKENDS[confget.BackendType.INI](cfg)

    data = ini.read_file()
    assert set(data.keys()) == {"", "a"}
    assert data["a"]["aonly"] == "a"
    assert data["a"]["both"] == "a"
    assert data[""]["defonly"] == "default"
    assert data[""]["both"] == "default"
    assert "aonly" not in data[""]
    assert "defonly" not in data["a"]

    par = ini.get_configparser()
    assert set(par.sections()) == {"", "a"}
    assert par.get("a", "aonly") == "a"
    assert par.get("a", "both") == "a"
    assert par.get("", "defonly") == "default"
    assert par.get("", "both") == "default"
    assert "aonly" not in par[""]
    # And this is where ConfigParser gets weird...
    assert par.get("a", "defonly") == "default"
