usage: `takuzu.py [-h] [--debug] [--method METHOD] ...`

Solve Takuzu puzzles

optional arguments:
* `-h, --help       show this help message and exit`
* `--debug          Print debug messages`
* `--method METHOD  The method to solve the puzzle with`

current methods:
* `backtracker` - simple backtracking solver; very slow
* `human` - applies heuristics to solve the puzzle much as a human would; falls back to `backtracker` when it can no longer make any progress
* `hybrid` - switches back and forth between `human` and `backtracker`, guessing only once when it otherwise wouldn't work
