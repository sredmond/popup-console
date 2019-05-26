"""A graphical Tk widget emulating a console."""
import logging
import sys

import tkinter as tk

logger = logging.getLogger(__name__)

# Text defaults.
FONT = ('Helvetica', 24, 'normal')
HEIGHT = 20  # Rows.
WIDTH = 80  # Column.

# Custom Marks
INPUT_START = 'input_start'
INPUT_END = 'input_end'


class ConsoleWidget(tk.Text):
    def __init__(self, master, *args, stderr=sys.stderr, stdout=sys.stdout, **kwargs):
        """Text widget to proxy internal commands."""
        kwargs.setdefault('height', HEIGHT)
        kwargs.setdefault('width', WIDTH)
        kwargs.setdefault('font', FONT)

        # Among other things, sets self.tk to the master's TkApplication.
        super().__init__(master, *args, **kwargs)

        self.master = master  # Tk master

        self.stderr = stderr
        self.stdout = stdout

        # Proxy the underlying object.
        self._orig = self._w + "_orig"
        self.tk.call("rename", self._w, self._orig)
        self.tk.createcommand(self._w, self._proxy)

        self.bind('<<LineStaged>>', self.process_line_input)

        # Set up the marks.
        self.mark_set(INPUT_START, '1.0')
        self.mark_gravity(INPUT_START, tk.LEFT)
        self.mark_set(INPUT_END, tk.END)
        self.mark_gravity(INPUT_END, tk.RIGHT)

        # The history of input strings.
        self.history = []

        # The current input string.
        self.current = ''

        # Staged lines to output.
        self.output_buffer = []


    def _proxy(self, command, *args):
        """Proxy all inbound Tk calls.

        If the command is not one of `'insert'`, `'delete'`, or `'replace'`, it
        is proxied to the underlying object.

        Otherwise:
        """
        command = command.lower()  # Tk commands should always be lowercase, but we'll take no chances.

        if command == 'mark' and args[0] == 'set' and args[1] == 'insert':
            # Don't let the insert cursor get outside the input range.
            desired = self.index(args[2])
            if self.compare(INPUT_START, '<=', desired) and self.compare(desired, '<=', INPUT_END):
                tk_command = (self._orig, command) + args
                return self.tk.call(tk_command)
            else:
                return

        # Proxy commands that don't do text modification directly to the underlying Tk object.
        if command not in ('insert', 'delete', 'replace'):
            tk_command = (self._orig, command) + args
            logger.warning('Forwarding {} {}'.format(command, args))
            return self.tk.call(tk_command)

        logger.warning('Handling {} {}'.format(command, args))

        # User has inserted some content.
        if command == 'insert':
            # What ways are there to insert content? This section hasn't been tested portably.
            # Type a single character:
            #     args == ('insert', '?') where `'?'` represents any 1-letter character.
            # Paste from a pasteboard:
            #     args == ('insert', 'content') where `'content'` is a string of any length (possibly empty).
            # Presumably, the `'insert'` at index zero refers to the mark at which content is inserted.
            assert args[0] == 'insert'
            content = args[1]

            # If we're not in the correct region, insert at the end.
            if not self.compare(INPUT_START, '<=', tk.INSERT) or not self.compare(tk.INSERT, '<', INPUT_END):
                self.mark_set(tk.INSERT, INPUT_END)  # TODO Does this bind them forever?

            # Print the content.
            tk_command = (self._orig, 'insert')  + (tk.INSERT, content)
            self.tk.call(tk_command)

            # Consume the content.
            self.current += content
            logger.warning(self.current)
            lines = self.current.split('\n')  # TODO(sredmond): This might not work on Windows
            for line in lines[:-1]:
                self.output_buffer.append(line)
                self.event_generate("<<LineStaged>>")

            self.current = self.get(INPUT_START, INPUT_END).rstrip('\n')
            logger.warn('active text {}'.format(self.current))


        # User has deleted some content.
        elif command == 'delete':
            # What ways are there to delete content?
            # Delete a single character:
            #     args == ('insert-1c', ) which likely means "delete at the insert mark minus one "
            # Delete a selected range:
            #     args == ('sel.first', 'sel.last') which means delete this selection.
            # We'll choose to emulate the same behavior as iTerm and Python: regardless of the selection, delete the
            # character immediately before the insert cursor.

            # Only delete when the cursor is between the start and end.
            if self.compare(INPUT_START, '<', tk.INSERT) and self.compare(tk.INSERT, '<=', INPUT_END):
                # Ignore args entirely.
                tk_command = (self._orig, 'delete', 'insert-1c')
                self.tk.call(tk_command)

        else:  # command == 'replace'
            # What ways are there to replace content?
            # Honestly, I haven't encountered any yet.
            pass

    def process_line_input(self, event):
        value = self.get('input_start', tk.END).rstrip('\n')  # Probably not needed to strip this trailing new line.
        logger.warning('start={}, end={}'.format(self.index('input_start'), self.index(tk.END)))
        logger.warning('Got a line! ' + repr(value))

        self.stdout.write(value + '\n')
        self.stdout.flush()

        self.event_generate("<<LineEntered>>")

    def read(self, size=-1):
        return 'from read'

    def readline(self, size=-1):
        return self.output_buffer.pop(0)

    def write(self, message):
        logger.warning('widget write: {}'.format(repr(message)))

        # Bypass the proxy to insert directly
        cmd = (self._orig, 'insert', tk.END, message)
        self.tk.call(cmd)
        self.mark_set(INPUT_START, 'end-1c')

        logger.warn('got start at {}'.format(self.index('input_start')))
        self.see(tk.END)

        # Update this widget's idle tasks (which involves drawing the characters to the screen).
        self.update_idletasks()  # TODO(sredmond): This, or self.master.update_idletasks()?

    def enable(self):
        self.config(state=tk.NORMAL)

    def disable(self):
        # NOTE! Disabling a widget causes all insertion and deletion calls to silently fail.
        # TODO(sredmond): Disable the proxy as well.
        self.config(state=tk.DISABLED)


if __name__ == '__main__':
    root = tk.Tk()
    widget = ConsoleWidget(root)
    widget.pack(fill='both', expand=True)
    root.lift()
    widget.write('Hello!\nWorld')
    root.mainloop()
