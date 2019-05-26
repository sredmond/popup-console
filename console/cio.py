"""Wrap a bridge to a subprocess running a console widget into a TextIO object.

The console client shouldn't have to know anything about the implementation of
the console subprocess. From the perspective of the client, the console backend
is just an opaque stream to be written to and read from.

NOTE(sredmond): Depending on the emergent complexity of this implementation, it
might be possible to wrap this up into the bridge itself.
"""
from console.bridge import ConsoleBridge

import io
import logging
import sys

logger = logging.getLogger(__name__)

class ConsoleIO(io.TextIOBase):
    """Wrap a console subprocess into a TextIO stream."""
    def __init__(self):
        # TODO(sredmond): What is the proper way to initialize the superclass?
        self.bridge = ConsoleBridge()

    def write(self, message):
        logger.debug('ConsoleIO is writing {!r}'.format(message))
        self.bridge.write(message)

    def readline(self, size=-1):
        return self.bridge.readline()

    # TODO(sredmond): Implement the rest of the TextIO methods.
