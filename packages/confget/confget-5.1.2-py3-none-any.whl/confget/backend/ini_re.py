# SPDX-FileCopyrightText: Peter Pentchev <roam@ringlet.net>
# SPDX-License-Identifier: BSD-2-Clause

"""A confget backend for reading INI-style files using regular expressions."""

import re
from typing import Callable, Dict, Match, NamedTuple, Pattern

from confget import defs

from . import ini_base


class MatcherType(NamedTuple):
    """Provide a parser function for lines matching the specified regex."""

    regex: Pattern[str]
    handle: Callable[
        [Match[str], Dict[str, str], defs.Config, defs.ConfigData],
        None,
    ]


def _handle_section(
    match: Match[str], state: Dict[str, str], cfg: defs.Config, res: defs.ConfigData
) -> None:
    """Handle a section heading: store the name."""
    state["section"] = match.group("name")
    if state["section"] not in res:
        res[state["section"]] = {}
    if not (cfg.section_specified or cfg.section or state["found"]):
        cfg.section = state["section"]
    state["found"] = state["section"]


def _handle_comment(
    _match: Match[str], _state: Dict[str, str], _cfg: defs.Config, _res: defs.ConfigData
) -> None:
    """Handle a comment line: ignore it."""


def _handle_variable(
    match: Match[str], state: Dict[str, str], _cfg: defs.Config, res: defs.ConfigData
) -> None:
    """Handle an assignment: store, check for a continuation."""
    state["name"] = match.group("name")
    state["found"] = state["name"]

    state["cont"] = match.group("cont")
    if state["cont"]:
        state["value"] = match.group("value") + match.group("ws")
    else:
        state["value"] = match.group("value")
        res[state["section"]][state["name"]] = state["value"]


_MATCHERS = [
    MatcherType(
        regex=re.compile(r"^ \s* (?: [#;] .* )? $", re.X),
        handle=_handle_comment,
    ),
    MatcherType(
        regex=re.compile(
            r"""
            ^
            \s* \[ \s*
            (?P<name> [^\]]+? )
            \s* \] \s*
            $""",
            re.X,
        ),
        handle=_handle_section,
    ),
    MatcherType(
        regex=re.compile(
            r"""
            ^
            \s*
            (?P<name> [^\s=]+ )
            \s* = \s*
            (?P<value> .*? )
            (?P<ws> \s* )
            (?P<cont> [\\] )?
            $""",
            re.X,
        ),
        handle=_handle_variable,
    ),
]


class INIRegexBackend(ini_base.INIBackendBase):
    """Parse INI-style configuration files using regular expressions."""

    def read_file(self) -> defs.ConfigData:
        """Read and parse the INI-style file, invoke the callbacks."""
        state = {
            "section": "",
            "name": "",
            "value": "",
            "cont": "",
            "found": "",
        }
        res: defs.ConfigData = {"": {}}

        with self.open_file() as infile:
            for orig_line in infile:
                line = orig_line.rstrip("\r\n")
                if state["cont"]:
                    if line.endswith("\\"):
                        line, state["cont"] = line[:-1], line[-1]
                        state["value"] += line
                    else:
                        state["cont"] = ""
                        state["value"] += line.rstrip()
                        res[state["section"]][state["name"]] = state["value"]
                    continue

                for data in _MATCHERS:
                    match = data.regex.match(line)
                    if match is None:
                        continue
                    data.handle(match, state, self._cfg, res)
                    break
                else:
                    raise ValueError(f"Unexpected line in {self._cfg.filename}: {line}")

        self.parsed = res
        return self.get_dict()
