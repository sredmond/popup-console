# Popup Console in Python

Navigating the command line prompt can be difficult for students who are new to programming. IDLE is a great GUI-based program that shows a command prompt side-by-side with a Python file, but that restricts users to IDLE.

This project provides a popup console in Tk for Python programs.

## Installation

TODO(sredmond): Write an installation from PyPI.

## Usage

By default, calling the `setup()` method will create a popup console window and redirect stdin and stdout to that window.

```
import console
console.setup()

print('Hello, world!')
name = input('What is your name?')
print('Hello', name)
```

This redirection happens at the level of `sys.stdin` and `sys.stdout`.
```
import console
console.setup()

import sys
print(sys.stdin)  # => ConsoleIO object.
```

The original `stdin` and `stdout` file objects can be accessed via `console.original_stdin` and `console.original_stdout`.

### Better Python: Being More Explicit

This behind-the-scenes implicit magic isn't very Pythonic. It's a reasonable default for our use case because we're hiding lots from our students, but 

```
import console
popup = console.create(capture=False)

popup.write()
popup.
```

### Creating Several Popup Consoles

With the default behavior, the popup console is spawned in another process so that Tk can listen for text input events concurrently to our potentially-slow Python code. However, you might not want this behavior. To just instantiate the actual Console widget:

```
import tkinter as tk
from console.widget import ConsoleWidget

root = tk.Tk()
widget = ConsoleWidget(root)
widget.pack()
```

There are two ways to write to the widget. Synchronously:

```
widget.print('Hello, world!')
widget.write('Hello, world!\n')
``` 

Asynchronously:

```
??
``` 

There is only one way to read from the widget.

```
name = widget.input('What is your name?')
entry = widget.readline()
```

## Boring Technical Details for the Curious

- When stdout is captured, `print` gets curried with `flush=True` by default.

## How does it work?

From the perspective of the console, it's a text widget that maintains a buffered input and a buffered output.

- The student calls `print`
- One way or another, this calls the `write` method of a subclass of TextIOBase
- this then writes out to subprocess' stdin.
- subprocess is busy-looping on checking stdin
- subprocess sees stdin and tells a tk window to print it
- tk window updates a tk text widget w/ new info.

- the student calls `input`
- one way or another, this calls readline on a subclass of textiobase
- this blocks on reading a line from a buffer of inbound lines.
- where does this buffer come from?
	- student for each subprocess spawned, a watchdog thread is spawned that monitors the subprocesses stdout, consumes it, and adds it to a buffer in memory.
	- subprocess prints a message to stdout
	- text entry, upon receiving an ENTER character, synchronously calls something like stdout.

perhaps this last one is better in reverse
- student hits ENTER
- tk text widget captures the entered line(s) and writes to some textiostream
- wrapper is busy looping checking the internal buffer for content, and upon finding some, writes to sp' stdout
- this unblocks a watchdog thread in the client process, which immediately consumes the content and buffers it.
- advanced - tell it to spawn a thread for 

## Notes

Don't forget to link simpio as a test dependency!

What to do... 

console is pretty good here!
popup console python

CONSOLE: on main thread, create a window with a text widget. on an event loop, consume from stdin and print to console if anything is there. otherwise, update and update idletasks.

upon registering a \n character, also write to stdout.

possibly: launch a background thread to just consume from stdin to avoid OS pipe buffer lockup. probably not though.

CLIENT: launch this CONSOLE in a subprocess and capture its stdin and stdout. to print to console, write to stdin. to read from console, blocking monitor its stdout.

real downside. goes through OS-level encoding? unless Python's wrappers do the "right thing"


OTHER USE:

Text Widget to be added to another existing Tk application.
can be given output by someone else (e.g. something like a console.write or console.print call)
maintains its own list of inputs. can be asked for input (blocking). that call awaits the UI providing some value.??

- remove ALL conceptual overhead
- probably not sublime + terminal