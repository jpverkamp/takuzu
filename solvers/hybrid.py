import copy
import logging
import solvers.backtracker
import solvers.human
import random

RULES = copy.copy(solvers.human.RULES)
RULES.remove(solvers.backtracker.solve)

def solve(takuzu):
    '''
    Solve a puzzle using a hybrid model.

    Start with the human solver.
    Every time you get stuck, guess at a spot.
    Switch back to the human solver (backtracking to step 2 on failures).
    '''

    queue = [takuzu]

    # DEBUG
    spots = 0
    for row in range(takuzu.size):
        for col in range(takuzu.size):
            if not takuzu.get(row, col):
                spots += 1

    logging.debug('Starting hybrid backtracker, {} possibilities to try ({} spots)'.format(
        2 ** spots,
        spots
    ))
    # /DEBUG

    while queue:
        takuzu = queue.pop()

        # Solved, we're done!
        if takuzu.is_solved():
            return takuzu

        # If we don't have a valid solution, stop looking on this branch
        if not takuzu.is_valid():
            continue

        # Try to advance using the human rules until they all fail
        while True:
            logging.animate(takuzu)
            logging.debug('Current board:\n' + str(takuzu).strip())
            updated = False
            for rule in RULES:
                logging.debug('Trying {}'.format(rule))
                next_takuzu = rule(takuzu)

                if next_takuzu:
                    takuzu = next_takuzu
                    updated = True
                    break

            if not updated:
                break

        # Solved, we're done!
        if takuzu.is_solved():
            return takuzu

        # Once they've failed, find one empty spot and try both possiblities
        def enqueue():
            for row in range(takuzu.size):
                for col in range(takuzu.size):
                    if not takuzu.get(row, col):
                        for value in '01':
                            queue.append(takuzu.set(row, col, value))
                        return
        enqueue()


    return False
