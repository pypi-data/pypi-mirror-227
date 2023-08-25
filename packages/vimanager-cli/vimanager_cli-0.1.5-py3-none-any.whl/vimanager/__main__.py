# -*- coding: utf-8 -*-

"""
The MIT License (MIT)

Copyright (c) 2023-present Lee-matod

Permission is hereby granted, free of charge, to any person obtaining a
copy of this software and associated documentation files (the "Software"),
to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense,
and/or sell copies of the Software, and to permit persons to whom the
Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
DEALINGS IN THE SOFTWARE.
"""
from __future__ import annotations

import click
import colorama

from .cli import compare, delete, inspect, rename, sort

try:
    from .cli import spotify
except ImportError:
    spotify = None

colorama.init(autoreset=True)


@click.group("vimanager")
def entrypoint():
    """An unofficial ViMusic CLI that enhances playlist management.

    See the source code at https://github.com/Lee-matod/vimanager-cli.
    """


entrypoint.add_command(compare)
entrypoint.add_command(inspect)
entrypoint.add_command(sort)
entrypoint.add_command(delete)
entrypoint.add_command(rename)
if spotify is not None:
    entrypoint.add_command(spotify)


if __name__ == "__main__":
    entrypoint()
