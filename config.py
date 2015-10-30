import argparse
import atexit
import curses
import logging
import os
import platform
import sys

parser = argparse.ArgumentParser(description = 'Solve Takuzu puzzles')
parser.add_argument('--debug', action = 'store_true', default = False, help = 'Print debug messages')
parser.add_argument('--animated', action = 'store_true', default = False, help = 'Animate progress')
parser.add_argument('--method', default = 'human', help = 'The method to solve the puzzle with')
parser.add_argument('files', nargs = argparse.REMAINDER)
args = parser.parse_args()

animated = args.animated
debug = args.debug
method = args.method
files = args.files

logging.basicConfig(format = '%(message)s', level = logging.DEBUG if debug else logging.WARNING)

# Set up curses, clean it up when the program is done and output the last frame to stdout
if animated:
    screen = curses.initscr()
    last_frame = ''

    def on_exit():
        curses.endwin()
        print(last_frame)

    atexit.register(on_exit)

def animate(obj):
    global last_frame
    last_frame = str(obj)

    if animated:
        screen.clear()
        screen.addstr(0, 0, str(obj))
        screen.refresh()

logging.animate = animate
