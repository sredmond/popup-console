"""Run a full background program that launches and manages a ConsoleWidget."""
from console.widget import ConsoleWidget

import io
import logging
import multiprocessing
import sys
import threading
import tkinter as tk
from tkinter import messagebox

logger = logging.getLogger(__name__)

# Show a default menu bar.
def _set_menubar(root):
    """Create a menu bar."""
    menubar = tk.Menu(root)
    filemenu = tk.Menu(menubar, tearoff=0)
    # filemenu.add_command(label="Save As...", command=self.save_as_dialog)
    filemenu.add_separator()
    filemenu.add_command(label="Exit", command=root.quit)
    menubar.add_cascade(label="File", menu=filemenu)
    helpmenu = tk.Menu(menubar, tearoff=0)
    helpmenu.add_command(label="About...", command=lambda: messagebox.showinfo('About', 'Hello, world!'))
    menubar.add_cascade(label="Help", menu=helpmenu)
    root.config(menu=menubar)

# Watch stdin for messages.
def monitor(widget, queue, conn):
    while True:
        try:
            content = conn.recv()
        # Raised when the the connection is empty and the other end was closed.
        except (OSError, EOFError):  # TODO(sredmond): Documentation suggests that its only EOFError.
            return
        else:
            queue.put(content)
            widget.event_generate('<<LineReceived>>')

# def mouth(widget, conn):
#     try:
#         for line in widget.stdout:
#             logger.debug('Mouth will say {!r}'.format(line))
#             conn.send(line)
#     except EOFError:
#         raise


def main(conn):
    queue = multiprocessing.Queue()

    # Widget callback captures the shared queue.
    def process_line(event):
        line = queue.get()
        logger.warning('process_line saw {!r} of type {}'.format(line, type(line)))
        widget.write(line)

    # Open up a widget.
    root = tk.Tk()
    widget = ConsoleWidget(root, out=conn.send, stdout=io.StringIO())
    widget.pack(fill='both', expand=True)
    root.lift()
    widget.write('Hello! - BG Process\n')
    widget.bind('<<LineReceived>>', process_line)

    # Spawn a thread to watch the connection and inform the (busy) Tk widget that it has content to consume.
    watchdog = threading.Thread(target=monitor, args=(widget, queue, conn))
    watchdog.start()  # TODO(sredmond): When is this thread joined?

    # speaker = threading.Thread(target=mouth, args=(widget, conn))
    # speaker.start()  # TODO(sredmond): When is this thread joined?

    _set_menubar(root)

    # Run forever.
    root.mainloop()

if __name__ == '__main__':
    main()

