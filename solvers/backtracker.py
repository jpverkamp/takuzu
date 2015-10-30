import logging

def solve(takuzu):
    '''Solve a puzzle using backtracking (also a fall back for the human solver).'''

    queue = [takuzu]

    # DEBUG
    spots = 0
    for row in range(takuzu.size):
        for col in range(takuzu.size):
            if not takuzu.get(row, col):
                spots += 1

    logging.debug('Starting backtracker, {} possibilities to try ({} spots)'.format(
        2 ** spots,
        spots
    ))
    # /DEBUG

    while queue:
        takuzu = queue.pop()
        logging.animate(takuzu)
        logging.debug('Current board:\n' + str(takuzu).strip())

        # Solved, we're done!
        if takuzu.is_solved():
            return takuzu

        # If we don't have a valid solution, stop looking on this branch
        if not takuzu.is_valid():
            continue

        # Otherwise, find one empty spot and try both possiblities
        def enqueue():
            for row in range(takuzu.size):
                for col in range(takuzu.size):
                    if not takuzu.get(row, col):
                        for value in '01':
                            queue.append(takuzu.set(row, col, value))
                        return
        enqueue()

    return False
