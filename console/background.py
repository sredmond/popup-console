"""Run a full background program that launches and manages a ConsoleWidget."""
from widget import ConsoleWidget

import logging
import multiprocessing
import sys
import threading
import tkinter as tk
from tkinter import messagebox
import urllib.parse as urlparse

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
def monitor_stdin(widget, queue):
    for line in sys.stdin:
        if line:
            queue.put(line[:-1])  # Strip the trailing newline.
            # TODO(sredmond): Also strip /r on windows?
            widget.event_generate('<<LineReceived>>')

def main():
    queue = multiprocessing.Queue()

    # Widget callback captures the shared queue.
    def process_line(event):
        line = urlparse.unquote(queue.get())
        logger.warning('process_line saw {} of type {}'.format(repr(line), type(line)))
        widget.write(line)

    # Open up a widget.
    root = tk.Tk()
    widget = ConsoleWidget(root)
    widget.pack(fill='both', expand=True)
    root.lift()
    widget.write('Hello! - BG Process\n')
    widget.bind('<<LineReceived>>', process_line)

    # Spawn a thread to watch stdin and inform the (busy) Tk widget that it has content to consume.
    watchdog = threading.Thread(target=monitor_stdin, args=(widget, queue))
    watchdog.start()

    _set_menubar(root)

    # Run forever.
    root.mainloop()

if __name__ == '__main__':
    main()

