import logging
import solvers.backtracker

def invert(v):
    return '0' if v == '1' else '1'

def permuate_nones(ls):
    '''Helper function to generate all permutations from filling in 0s and 1s into a list'''

    if ls == []:
        yield []
    elif ls[0]:
        for recur in permuate_nones(ls[1:]):
            yield [ls[0]] + recur
    else:
        for value in '01':
            for recur in permuate_nones(ls[1:]):
                yield [value] + recur

def __third_of_a_kind__(takuzu):
    '''If adding a value would make three in a row, add the other.'''

    for row in range(takuzu.size):
        for col in range(takuzu.size):
            if takuzu.get(row, col):
                continue

            for ((offset1_row, offset1_col), (offset2_row, offset2_col)) in [
                # Two already in a line
                (( 0,  1), ( 0,  2)),
                (( 0, -1), ( 0, -2)),
                (( 1,  0), ( 2,  0)),
                ((-1,  0), (-2,  0)),
                # Two with a hole in between
                (( 0,  1), ( 0, -1)),
                (( 1,  0), (-1,  0)),
            ]:

                val1 = takuzu.get(row + offset1_row, col + offset1_col)
                val2 = takuzu.get(row + offset2_row, col + offset2_col)

                if val1 and val2 and val1 == val2:
                    return takuzu.set(row, col, invert(val1))

    return False

def __fill_rows__(takuzu):
    '''If we can figure out how many 0s and 1s we need for each and any row/col needs only 0s or 1s, add them'''

    # Try to fill any rows that have all of the needed 0s/1s but not the other
    for index in range(takuzu.size):
        for row, col in [(index, None), (None, index)]:
            for value in '01':
                if takuzu.get(row, col).count(value) == takuzu.size / 2: # Have enough of 'value'
                    if takuzu.get(row, col).count(invert(value)) < takuzu.size / 2: # Not enough of the other one
                        return takuzu.set(row, col, invert(value))

    return False

def __fill_by_duplicates__(takuzu):
    '''Fill a puzzle by checking if any rows/cols are near enough to done that only one possibility is left.'''

    # Find all completed rows and cols
    completed_rows = [
        takuzu.get(row, None)
        for row in range(takuzu.size)
        if all(takuzu.get(row, None))
    ]

    # If have neither, this method won't work
    if completed_rows:
        for row in range(takuzu.size):
            row_data = takuzu.get(row, None)

            # Already a complete row, skip it
            if all(row_data):
                continue

            # Generate all posibilities, removing any that we already see
            possible_options = [
                option
                for option in permuate_nones(row_data)
                if (
                    option not in completed_rows
                    and option.count('0') == takuzu.size / 2
                    and option.count('1') == takuzu.size / 2
                )
            ]

            # If we have exactly one, set that one
            if len(possible_options) == 1:
                for col, value in enumerate(possible_options[0]):
                    takuzu = takuzu.set(row, col, value)
                return takuzu

RULES = [
    __third_of_a_kind__,
    __fill_rows__,
    __fill_by_duplicates__,
    solvers.backtracker.solve,
]

def solve(takuzu):
    '''Solve a Takuzu puzzle much as a human would: by applying a series of logical rules.'''

    while True:
        logging.debug('---------\nCurrent board:\n' + str(takuzu).strip())
        updated = False

        # If we've already solved it, return
        if takuzu.is_solved():
            return takuzu

        # Try to apply each rule in turn; if any rule works start over
        for rule in RULES:
            logging.debug('Trying {}'.format(rule))
            next_takuzu = rule(takuzu)

            if next_takuzu:
                takuzu = next_takuzu
                updated = True
                break

        # If we didn't apply any rule this iteration, done trying
        if not updated:
            break

    return takuzu
