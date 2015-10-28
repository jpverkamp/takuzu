import argparse
import logging
import model
import solvers
import sys
import time

parser = argparse.ArgumentParser(description = 'Solve Takuzu puzzles')
parser.add_argument('--debug', action = 'store_true', default = False, help = 'Print debug messages')
parser.add_argument('--method', default = 'human', help = 'The method to solve the puzzle with')
parser.add_argument('files', nargs = argparse.REMAINDER)
args = parser.parse_args()

logging.basicConfig(format = '%(message)s', level = logging.DEBUG if args.debug else logging.WARNING)

try:
    solve = getattr(solvers, args.method).solve
except:
    print('Unknown solver: {}'.format(args.method))
    sys.exit(-1)

for filename in args.files:
    takuzu = model.Takuzu(filename = filename)
    start = time.time()
    takuzu = solve(takuzu)
    end = time.time()

    print()
    print(takuzu)
    print('Solved in {:.02f} seconds'.format(end - start))
