#!/bin/sh
# SPDX-FileCopyrightText: Peter Pentchev <roam@ringlet.net>
# SPDX-License-Identifier: BSD-2-Clause

set -e

: "${TOX_STAGES:=tox-stages}"

env TOX_DEVEL_FILES='../t/defs/tools/generate.py' $TOX_STAGES run 'ruff' '@check' '@tests'
