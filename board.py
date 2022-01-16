class Board:
    def __init__(self, board: list[list]):
        # rows is the basic input
        self._rows: list[list[int | str]] = board

        # order by columns
        self._columns: list[list[int | str]] = [[self._rows[x][y] for x in range(9)] for y in range(9)]

        # all elements
        self._all: list[int | str] = []
        for inner_list in self._rows:
            self._all += inner_list

        # order by blocks
        self._blocks: list[list[int | str]] = []
        for j in range(0, 81, 27):
            # for each line of blocks
            for i in range(3):
                # for each block in a line
                temp_ls = []
                for k in range(0, 9, 3):
                    # for each line in a block
                    temp_ls += self._all[j + (i + k) * 3: j + (i + k + 1) * 3]
                self._blocks.append(temp_ls)

        # testing the given input
        self._test_all()

    def __str__(self):
        return """
    {} {} {} | {} {} {} | {} {} {}
    {} {} {} | {} {} {} | {} {} {}
    {} {} {} | {} {} {} | {} {} {}
  --------+-------+-------- 
    {} {} {} | {} {} {} | {} {} {}
    {} {} {} | {} {} {} | {} {} {}
    {} {} {} | {} {} {} | {} {} {}
  --------+-------+-------- 
    {} {} {} | {} {} {} | {} {} {}
    {} {} {} | {} {} {} | {} {} {}
    {} {} {} | {} {} {} | {} {} {}""".format(*self._all)

    @staticmethod
    def _get_block_by_pos(x, y):
        return x // 3 * 3 + y // 3

    def _test_all(self):
        """The method checks the given input. If the input is invalid, an Exception will be raised."""
        for item in self._all:
            assert item == '.' or isinstance(item, int) and 1 <= item <= 9, f'Board contains {item!r}.'
        for ind, row in enumerate(self._rows):
            for num in range(1, 10):
                assert row.count(num) < 2, f"Board contains '{num}' more than once in row number {ind + 1}."
        for ind, column in enumerate(self._columns):
            for num in range(1, 10):
                assert column.count(num) < 2, f"Board contains '{num}' more than once in column number {ind + 1}."
        for ind, block in enumerate(self._blocks):
            for num in range(1, 10):
                assert block.count(num) < 2, f"Board contains '{num}' more than once in block number {ind + 1}."

    def _check_value_in_pos(self, val: int, x: int, y: int):
        """The method checks if a value fits in a specific position."""
        # Input integrity check
        assert isinstance(val, int) and 1 <= val <= 9, f"Invalid value. val should be an integer in range 1-9, {val=!r}"
        assert isinstance(x, int) and 0 <= x <= 8, f"Invalid x. x should be an integer in range 0-8, {x=!r}"
        assert isinstance(y, int) and 0 <= y <= 8, f"Invalid y. y should be an integer in range 0-8, {y=!r}"
        assert self._rows[x][y] == '.', f"Invalid position. Position must be empty."

        if val in self._rows[x]:
            return False
        if val in self._columns[y]:
            return False
        if val in self._blocks[self._get_block_by_pos(x, y)]:
            return False
        return True

    def _find_next_pos(self, current_row):
        """The method searches for the first position of an empty cell, starting at the current row."""
        new_x = new_y = -1
        for new_x in range(current_row, 9):
            try:
                new_y = self._rows[new_x].index('.')
            except ValueError:
                continue
            else:
                break

        return new_x, new_y

    def _set_value(self, val, x: int, y: int):
        """The method sets a given value in a given position"""
        # Input integrity check
        assert val == '.' or isinstance(val, int) and 1 <= val <= 9, "Invalid value. val should be an integer in " \
                                                                     f"range 1-9 or a single dot '.', {val=!r} "
        assert isinstance(x, int) and 0 <= x <= 8, f"Invalid x. x should be an integer in range 0-8, {x=!r}"
        assert isinstance(y, int) and 0 <= y <= 8, f"Invalid y. y should be an integer in range 0-8, {y=!r}"

        self._rows[x][y] = val
        self._all[x * 9 + y] = val
        self._columns[y][x] = val
        self._blocks[self._get_block_by_pos(x, y)][x % 3 * 3 + y % 3] = val

    def solve(self, current_row=0):
        """A recursive method that tries to solve the board.
         If the board was solved, True is returned, otherwise False."""
        x, y = self._find_next_pos(current_row)
        if y == -1:
            return True
        for i in range(1, 10):
            if self._check_value_in_pos(i, x, y):
                self._set_value(i, x, y)
                if self.solve(x):
                    return True
                self._set_value('.', x, y)
        return False
