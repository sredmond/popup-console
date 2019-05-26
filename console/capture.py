"""Capture the stdin and stdout of the calling process."""
from console.cio import ConsoleIO

import builtins
import functools
import os
import sys

# Save references to the original stdin/stdout.
original_stdin = sys.stdin
original_stdout = sys.stdout


def setup(capture=True):
    io = ConsoleIO()
    if capture:
        sys.stdin = io
        sys.stdout = io  # TODO(sredmond): Maybe use contextlib.redirect_stdout
        # TODO(sredmond): Also capture stderr?

    return io
