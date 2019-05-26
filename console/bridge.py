"""Spawn and manage a background process that will display the graphical console."""
import logging
import multiprocessing
import pathlib
import queue
import subprocess
import sys
import threading

logger = logging.getLogger(__name__)

def background(conn):
    from console.background import main
    main(conn)
    conn.close()

class ConsoleBridge:
    def __init__(self):
        parent_conn, child_conn = multiprocessing.Pipe()

        # Spawn a child process to run the background graphical popup console.
        self.child = multiprocessing.Process(target=background, args=(child_conn, ))
        self.child.start()

        self.conn = parent_conn

    def write(self, content):
        self.conn.send(content)

    def readline(self):
        try:
            return self.conn.recv()
        except EOFError as err:
            raise


if __name__ == '__main__':
    bridge = ConsoleBridge()
    bridge.write('From FG: Áccénts are ókåy but emøjî are nOt. Symbols (åßß∂ƒ©˙∆©¬˚) are fine. \n')
