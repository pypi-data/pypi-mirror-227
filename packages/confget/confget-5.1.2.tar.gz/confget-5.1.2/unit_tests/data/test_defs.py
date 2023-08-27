# SPDX-FileCopyrightText: Peter Pentchev <roam@ringlet.net>
# SPDX-License-Identifier: BSD-2-Clause

"""Class definitions for the confget test suite."""

import abc
import dataclasses
import os
import shlex
from typing import Any, Dict, Iterable, List, NamedTuple, Optional, Type

from confget import backend as cbackend
from confget import defs as cdefs
from confget import format as cformat


class CmdOpt(NamedTuple):
    """Keep track of command-line options that require an argument."""

    option: str
    has_argument: bool


CMDLINE_OPTIONS = {
    "check_only": CmdOpt("-c", has_argument=False),
    "filename": CmdOpt("-f", has_argument=True),
    "hide_var_name": CmdOpt("-n", has_argument=False),
    "list_all": CmdOpt("-l", has_argument=False),
    "match_var_names": CmdOpt("-L", has_argument=False),
    "match_var_values": CmdOpt("-m", has_argument=True),
    "section": CmdOpt("-s", has_argument=True),
    "section_override": CmdOpt("-O", has_argument=False),
    "section_specified": CmdOpt("", has_argument=False),
    "show_var_name": CmdOpt("-N", has_argument=False),
}


def get_test_path(relpath: Optional[str]) -> str:
    """Get the path to a test definition file."""
    return os.environ.get("TESTDIR", "test_data") + ("/" + relpath if relpath is not None else "")


@dataclasses.dataclass(frozen=True)
class XFormType(metaclass=abc.ABCMeta):
    """Transform something to something else with great prejudice."""

    @property
    @abc.abstractmethod
    def command(self) -> str:
        """Get the shell command to transform the confget output."""
        raise NotImplementedError(f"{type(self).__name__}.command")

    @abc.abstractmethod
    def do_xform(self, res: Iterable[cformat.FormatOutput]) -> str:
        """Transform the Python representation of the result."""
        raise NotImplementedError(f"{type(self).__name__}.do_xform()")


@dataclasses.dataclass(frozen=True)
class XFormNone(XFormType):
    """No transformation, newlines preserved."""

    @property
    def command(self) -> str:
        """Return a no-op shell command, nothing at all."""
        return ""

    def do_xform(self, res: Iterable[cformat.FormatOutput]) -> str:
        """Return the output exactly as it was produced."""
        return "\n".join([line.output_full for line in res])


@dataclasses.dataclass(frozen=True)
class XFormNewlineToSpace(XFormType):
    """Translate newlines to spaces."""

    @property
    def command(self) -> str:
        """Get the shell command to merge all lines into one."""
        return '| tr "\\n" " "'

    def do_xform(self, res: Iterable[cformat.FormatOutput]) -> str:
        """Merge the lines output by confget."""
        return "".join(line.output_full + " " for line in res)


@dataclasses.dataclass(frozen=True)
class XFormCountLines(XFormType):
    """Count the lines output by confget."""

    sought: Optional[str] = None
    sought_in: bool = True

    @property
    def command(self) -> str:
        """Get the shell command to count lines, either the matching ones or all of them."""
        prefix = (
            "| fgrep -{inv}e {sought} ".format(
                inv="" if self.sought_in else "v",
                sought=shlex.quote(self.sought),
            )
            if self.sought is not None
            else ""
        )
        return prefix + "| wc -l | tr -d ' '"

    def do_xform(self, res: Iterable[cformat.FormatOutput]) -> str:
        """Return the number of matching lines (all of them if "sought" not specified)."""
        if self.sought is None:
            return str(len(list(res)))

        lines = [line for line in res if self.sought_in == (self.sought in line.output_full)]
        return str(len(lines))


XFORM = {
    "": XFormNone(),
    "count-lines": XFormCountLines(),
    "count-lines-eq": XFormCountLines(sought="="),
    "count-lines-non-eq": XFormCountLines(sought="=", sought_in=False),
    "newline-to-space": XFormNewlineToSpace(),
}


class OutputDef(metaclass=abc.ABCMeta):
    """A definition for a single test's output."""

    def __init__(self) -> None:  # noqa: B027
        """No initialization at all for the base class."""

    @abc.abstractmethod
    def get_check(self) -> str:
        """Get the check string as a shell command."""
        raise NotImplementedError(f"{type(self).__name__}.get_check()")

    @property
    @abc.abstractmethod
    def var_name(self) -> str:
        """Get the variable name to display."""
        raise NotImplementedError(f"{type(self).__name__}.var_name")

    @abc.abstractmethod
    def check_result(self, _res: str) -> None:
        """Check whether the processed confget result is correct."""
        raise NotImplementedError(f"{type(self).__name__}.check_result()")


class ExactOutputDef(OutputDef):
    """Check that the program output this exact string."""

    def __init__(self, exact: str) -> None:
        """Initialize an exact test output object."""
        super().__init__()
        self.exact = exact

    def get_check(self) -> str:
        """Get the "is this the correct string?" check as a shell command."""
        return '[ "$v" = ' + shlex.quote(self.exact) + " ]"

    @property
    def var_name(self) -> str:
        """Get the "v" variable name to display."""
        return "v"

    def check_result(self, res: str) -> None:
        """Check whether the processed confget result is exactly as expected."""
        assert res == self.exact


class ExitOKOutputDef(OutputDef):
    """Check that the program succeeded or failed as expected."""

    def __init__(self, *, success: bool) -> None:
        """Initialize an "finished successfully" test output object."""
        super().__init__()
        self.success = success

    def get_check(self) -> str:
        """Get the "did the program succeed?" check as a shell command."""
        return '[ "$res" {compare} 0 ]'.format(compare="=" if self.success else "!=")

    @property
    def var_name(self) -> str:
        """Get the "res" variable name to display."""
        return "res"

    def check_result(self, res: str) -> None:
        """Raise an error since this class merely tests the program's exit code."""
        raise NotImplementedError(repr((self, res)))


@dataclasses.dataclass(frozen=True)
class SingleTestDef:
    """A definition for a single test."""

    args: Dict[str, str]
    keys: List[str]
    output: OutputDef
    xform: str = ""
    backend: str = cdefs.BackendType.INI
    stdin: Optional[str] = None

    def get_backend(self) -> Type[cbackend.abstract.Backend]:
        """Get the appropriate confget backend type."""
        return cbackend.BACKENDS[self.backend]

    def get_config(self) -> cformat.FormatConfig:
        """Convert the test's data to a config object."""
        data: Dict[str, Any] = {}
        for name, value in self.args.items():
            if name == "hide_var_name":
                continue

            opt = CMDLINE_OPTIONS[name]
            if opt.has_argument:
                data[name] = value
            else:
                data[name] = True

        if "filename" in data:
            data["filename"] = get_test_path(data["filename"])
        elif self.stdin:
            data["filename"] = "-"

        data["show_var_name"] = "show_var_name" in self.args or (
            ("match_var_names" in self.args or "list_all" in self.args or len(self.keys) > 1)
            and "hide_var_name" not in self.args
        )

        return cformat.FormatConfig(self.keys, **data)

    def do_xform(self, res: Iterable[cformat.FormatOutput]) -> str:
        """Return the output delimiter depending on the xform property."""
        return XFORM[self.xform].do_xform(res)


@dataclasses.dataclass(frozen=True)
class FileDef:
    """A definition for a file defining related tests."""

    tests: List[SingleTestDef]
