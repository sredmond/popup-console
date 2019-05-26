"""Spawn and manage a background process that will display the graphical console."""
import logging
import pathlib
import queue
import subprocess
import sys
import threading
import urllib.parse as urlparse

logger = logging.getLogger(__name__)

class ConsoleSubprocess:
    def __init__(self):
        try:
            # TODO(sredmond): Make sure this runs the same python3. Maybe fork a subprocess?
            path = str(pathlib.Path(__file__).parent / 'background.py')
            self.subp = subprocess.Popen(['python3', path], stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True)
        except BrokenPipeError as err:
            print('Oh no! A broken pipe! :(')  # TODO(sredmond): Handle this (more) gracefully.
            raise err

        # NOTE: Tcl only supports the basic multilingual plane, so no emojis.
        self.write('From FG: Áccénts are ókåy but emøjî are nOt. Symbols (åßß∂ƒ©˙∆©¬˚) are fine. \n')
        self.flush()

        # A simple queue communicates between the watchdog thread and the main thread.
        self.queue = queue.SimpleQueue()
        self.watchdog = threading.Thread(target=self.monitor)
        self.watchdog.start()

    def write(self, content):
        # Pay no attention to the url-encoding that's happening so newlines don't cause the receiving process to see a line.
        self.subp.stdin.write(urlparse.quote(content))

    def flush(self):
        self.subp.stdin.write('\n')
        self.subp.stdin.flush()

    def readline(self):
        return self.queue.get()

    def monitor(self):
        for line in self.subp.stdout:
            if not line: continue

            logger.debug('Watchdog saw {!r}'.format(line))
            self.queue.put(line)

    def wait(self):
        self.subp.wait()


if __name__ == '__main__':
    sub = ConsoleSubprocess()
    sub.write('hello there')
    sub.wait()

