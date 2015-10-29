import collections

class Takuzu(object):

    def __init__(self, filename = None, parent = None):
        '''
        Represent a Takuzu puzzle (a grid of 0, 1, and .)

        If filename is set, load from file.
        If parent is set, extend that Takuzu puzzle.

        If neither or both is set, that is an error.
        '''

        if not (filename or parent) or (filename and parent):
            raise Exception('Set exactly one of filename and parent')

        self.size = 0
        self.tiles = collections.defaultdict(lambda : False)
        self.parent = False

        if parent:
            self.size = parent.size
            self.parent = parent

        elif filename:
            with open(filename, 'r') as fin:
                for row, line in enumerate(fin):
                    for col, char in enumerate(line.strip()):
                        if char in '01':
                            self.tiles[row, col] = char

                        self.size = col + 1

    def __eq__(self, other):
        '''Check if two Takuzu puzzles are equal.'''

        for row in range(self.size):
            for col in range(self.size):
                if self.get(row, col) != other.get(row, col):
                    return False

        return True

    def __str__(self):
        '''Return a string representation the same as can be read from a file.'''

        out = ''

        for row in range(self.size):
            for col in range(self.size):
                out += str(self.get(row, col) or '.')
            out += '\n'

        return out

    def get(self, row = None, col = None):
        '''
        Access a tile in the current puzzle, return False for unset values

        If the current puzzle doesn't have a value set, recur to parents.
        If either row or col is set to None, return that entire row or column.
        If neither is set, return nested lists containing all current values.
        '''

        # Note: We need the ugly != None to correctly deal with row or col = 0. Sometimes truthiness is annoying.

        if row != None and col != None:
            return self.tiles[row, col] or (self.parent and self.parent.get(row, col))
        elif row != None:
            return [self.get(row, col) for col in range(self.size)]
        elif col != None:
            return [self.get(row, col) for row in range(self.size)]
        else:
            return [
                [self.get(row, col) for col in range(self.size)]
                for row in range(self.size)
            ]

    def set(self, row, col, val):
        '''
        Create a child Takuzu object with the specific value set.

        If either row or column is set to None, fill any empty elements in that entire row with the given value.
        '''

        child = Takuzu(parent = self)

        if row != None and col != None:
            child.tiles[row, col] = val
        elif row != None:
            for col in range(self.size):
                if not child.get(row, col):
                    child.tiles[row, col] = val
        elif col != None:
            for row in range(self.size):
                if not child.get(row, col):
                    child.tiles[row, col] = val
        else:
            raise Exception('Must set at least one of row and column')

        return child

    def is_full(self):
        '''If all values have been filled in.'''

        for row in range(self.size):
            for col in range(self.size):
                if not self.get(row, col):
                    return False

        return True

    def is_solved(self):
        '''Return True iff this puzzle is solved.'''

        # A puzzle that isn't full cannot be solved
        if not self.is_full():
            return False

        # Cannot have three identical numbers in a line
        for row in range(self.size):
            for col in range(self.size):
                if self.get(row - 1, col) == self.get(row, col) == self.get(row + 1, col):
                    return False

                if self.get(row, col - 1) == self.get(row, col) == self.get(row, col + 1):
                    return False

        # All rows and columns must have the same count of 0s and 1s (but 0s =/= 1s)
        for index in range(self.size):
            if (
                self.get(index, None).count('0') != self.size / 2
                or self.get(index, None).count('1') != self.size / 2
                or self.get(None, index).count('0') != self.size / 2
                or self.get(None, index).count('1') != self.size / 2
            ):
                return False

        # No two rows or columns can be equal
        for first_index in range(self.size):
            for second_index in range(first_index):
                if (
                    self.get(first_index, None) == self.get(second_index, None)
                    or self.get(None, first_index) == self.get(None, second_index)
                ):
                    return False

        # Whee passed all three conditions!
        return True
