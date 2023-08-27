# SPDX-FileCopyrightText: Peter Pentchev <roam@ringlet.net>
# SPDX-License-Identifier: BSD-2-Clause

"""A confget backend for reading INI-style files using the pyparsing library."""

from typing import List, Tuple

import pyparsing as pyp

from confget import defs

from . import ini_base


SectionRaw = Tuple[str, defs.SectionData]


_p_spc = pyp.Opt(pyp.Word(" \t"))


@_p_spc.set_parse_action
def _parse_spc(tokens: pyp.ParseResults) -> str:
    """Parse a (possibly empty) sequence of spaces and tabs into a string."""
    if len(tokens) == 1:
        assert isinstance(  # noqa: S101  # mypy needs this
            tokens[0], str
        ), f"_parse_spc[0] {tokens!r}"
        return tokens[0]

    return ""


_p_nl = pyp.Char("\n").suppress() - _p_spc


@_p_nl.set_parse_action
def _parse_nl(tokens: pyp.ParseResults) -> str:
    """Parse a newline, store the whitespace immediately following it into a string."""
    assert isinstance(tokens[0], str), f"_parse_nl {tokens!r}"  # noqa: S101  # mypy needs this
    return tokens[0]


_p_line_skip = (
    pyp.Opt(pyp.Char("#;") - pyp.ZeroOrMore(pyp.CharsNotIn("\n"))).suppress() + _p_nl.suppress()
)

_p_skip_lines = pyp.ZeroOrMore(_p_line_skip)

_p_var = pyp.CharsNotIn(" \t[#;=\n")


@_p_var.set_parse_action
def _parse_var(tokens: pyp.ParseResults) -> str:
    """Parse a variable name into a string."""
    assert isinstance(tokens[0], str), f"_parse_var {tokens!r}"  # noqa: S101  # mypy needs this
    return tokens[0]


_p_backslashes = pyp.ZeroOrMore(
    pyp.Opt(pyp.CharsNotIn("\\\n")) + pyp.Char("\\") + pyp.CharsNotIn("\\\n", exact=1)
) + pyp.Opt(pyp.CharsNotIn("\\\n"))


@_p_backslashes.set_parse_action
def _parse_backslashes(tokens: pyp.ParseResults) -> str:
    """Parse a single line, possibly containing backslashes, but not ending in one."""
    return "".join(tokens)


_p_continued = _p_backslashes + pyp.Char("\\").suppress() + _p_nl


@_p_continued.set_parse_action
def _parse_continued(tokens: pyp.ParseResults) -> str:
    """Parse one or more lines ending in backslashes, do not trim anything."""
    assert isinstance(tokens[0], str) and isinstance(  # noqa: S101,PT018  # mypy needs this
        tokens[1], str
    ), f"_parse_continued {tokens!r}"
    return tokens[0] + tokens[1]


_p_not_continued = _p_backslashes + _p_nl.suppress()


@_p_not_continued.set_parse_action
def _parse_not_continued(tokens: pyp.ParseResults) -> str:
    """Parse the last line of a value, trimming whitespace from the end."""
    assert isinstance(  # noqa: S101  # mypy needs this
        tokens[0], str
    ), f"_parse_non_continued {tokens!r}"
    return tokens[0].rstrip()


_p_line_var = (
    _p_var
    - _p_spc.suppress()
    + pyp.Literal("=").suppress()
    + _p_spc.suppress()
    + pyp.ZeroOrMore(_p_continued)
    + _p_not_continued
)


@_p_line_var.set_parse_action
def _parse_line_var(tokens: pyp.ParseResults) -> Tuple[str, str]:
    """Parse a variable name into a string."""
    return tokens[0], "".join(tokens[1:])


_p_section_start = (
    pyp.Char("[").suppress()
    - _p_spc.suppress()
    + pyp.CharsNotIn("]\n")
    + pyp.Char("]").suppress()
    + _p_spc.suppress()
    + _p_nl.suppress()
)


@_p_section_start.set_parse_action
def _parse_section_start(tokens: pyp.ParseResults) -> str:
    """Parse a section name into a string."""
    assert isinstance(  # noqa: S101  # mypy needs this
        tokens[0], str
    ), f"_parse_section_start {tokens!r}"
    return tokens[0].rstrip()


_p_section_contents = pyp.ZeroOrMore(_p_line_var - _p_skip_lines.suppress())


@_p_section_contents.set_parse_action
def _parse_section_contents(tokens: pyp.ParseResults) -> defs.SectionData:
    """Parse a (possibly empty) series of var=value lines into a dictionary."""
    res = {}
    for item in tokens:
        res[item[0]] = item[1]

    return res


_p_section = _p_section_start + _p_skip_lines().suppress() + _p_section_contents


@_p_section.set_parse_action
def _parse_section(tokens: pyp.ParseResults) -> SectionRaw:
    """Parse a section (name and contents) into a `SectionRaw` object."""
    return tokens[0], tokens[1]


_p_ini = (
    _p_spc.suppress()
    + _p_skip_lines().suppress()
    + _p_section_contents
    + pyp.ZeroOrMore(_p_section)
)


@_p_ini.set_parse_action
def _parse_ini(tokens: pyp.ParseResults) -> Tuple[defs.SectionData, List[SectionRaw]]:
    """Parse a full INI-style file into an unnamed section and others."""
    toklist = tokens.as_list()
    return toklist[0], toklist[1:]


_p_ini_complete = _p_ini.leave_whitespace().parse_with_tabs()


class INIPypBackend(ini_base.INIBackendBase):
    """Parse INI-style configuration files using the pyparsing library."""

    def read_file(self) -> defs.ConfigData:
        """Read and parse the INI-style file, invoke the callbacks."""
        res: defs.ConfigData = {"": {}}

        with self.open_file() as infile:
            raw = infile.read()
            first, rest = _p_ini_complete.parse_string(raw, parse_all=True).as_list()[0]
            first_name = (
                self._cfg.section
                if self._cfg.section_specified or self._cfg.section
                else ("" if first or not rest else rest[0][0])
            )
            if first:
                res[""] = first
            for name, sect_data in rest:
                if name in res:
                    res[name].update(sect_data)
                else:
                    res[name] = sect_data

        self._cfg.section = first_name
        self.parsed = res
        return self.get_dict()
