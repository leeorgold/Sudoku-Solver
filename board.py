class Board:
    def __init__(self, board, n=9):
        # rows is the basic input
        self._n = n
        self._sqrt = self._n ** .5
        assert self._sqrt == int(self._sqrt), f'n is not a perfect square. n = {self._n}'
        self._sqrt = int(self._sqrt)
        self._rows = self._get_copy_of_input(board)
        # self._rows: list[list[int | str]] = board

        # order by columns
        self._columns = [[self._rows[x][y] for x in range(self._n)] for y in range(self._n)]

        # all elements
        self._all = []
        for inner_list in self._rows:
            self._all += inner_list

        # order by blocks
        self._blocks: list[list[int | str]] = []
        for j in range(0, self._n ** 2, self._n * self._sqrt):
            # for each line of blocks
            for i in range(self._sqrt):
                # for each block in a line
                temp_ls = []
                for k in range(0, self._n, self._sqrt):
                    # for each line in a block
                    temp_ls += self._all[j + (i + k) * self._sqrt: j + (i + k + 1) * self._sqrt]
                self._blocks.append(temp_ls)

        # testing the given input
        self._test_all()

    def __str__(self):
        #       return """
        #   {} {} {} | {} {} {} | {} {} {}
        #   {} {} {} | {} {} {} | {} {} {}
        #   {} {} {} | {} {} {} | {} {} {}
        # --------+-------+--------
        #   {} {} {} | {} {} {} | {} {} {}
        #   {} {} {} | {} {} {} | {} {} {}
        #   {} {} {} | {} {} {} | {} {} {}
        # --------+-------+--------
        #   {} {} {} | {} {} {} | {} {} {}
        #   {} {} {} | {} {} {} | {} {} {}
        #   {} {} {} | {} {} {} | {} {} {}""".format(*self._all)
        st = ' '
        for rows in range(self._sqrt):
            for row in range(self._sqrt):
                for i in range(self._sqrt):
                    st += '{:^2} ' * self._sqrt + '| '
                st = st[:-2] + '\n '
            if rows < self._sqrt - 1:
                st = st[:-1] + ('-' * (3 * self._sqrt + 1) + '+') * self._sqrt
                st = st[:-1] + '\n '

        return st.format(*self._all)


    @staticmethod
    def _get_copy_of_input(rows):
        copy = []
        for row in rows:
            copy.append(row.copy())
        return copy

    def _get_block_by_pos(self, x, y):
        return x // self._sqrt * self._sqrt + y // self._sqrt

    def _test_all(self):
        """The method checks the given input. If the input is invalid, an Exception will be raised."""
        assert len(self._rows) == self._n, f'The board contains {len(self._rows)} rows instead of {self._n}'
        assert len(self._columns) == self._n, f'The board contains {len(self._columns)} columns instead of {self._n}'
        for item in self._all:
            assert item == '.' or isinstance(item, int) and 1 <= item <= self._n, f'Board contains {item!r}.'
        for ind, row in enumerate(self._rows):
            for num in range(1, self._n + 1):
                assert row.count(num) < 2, f"Board contains '{num}' more than once in row number {ind + 1}."
        for ind, column in enumerate(self._columns):
            for num in range(1, self._n + 1):
                assert column.count(num) < 2, f"Board contains '{num}' more than once in column number {ind + 1}."
        for ind, block in enumerate(self._blocks):
            for num in range(1, self._n + 1):
                assert block.count(num) < 2, f"Board contains '{num}' more than once in block number {ind + 1}."

    def _is_empty_pos(self, x, y):
        assert isinstance(x, int) and 0 <= x < self._n, \
            f"Invalid x. x should be an integer in range 0-{self._n - 1}, {x=!r}"
        assert isinstance(y, int) and 0 <= y < self._n, \
            f"Invalid y. y should be an integer in range 0-{self._n - 1}, {y=!r}"
        return self._rows[x][y] == '.'

    def _check_value_in_pos(self, val: int, x: int, y: int):
        """The method checks if a value fits in a specific position."""
        # Input integrity check
        assert isinstance(val, int) and 1 <= val <= self._n, \
            f"Invalid value. val should be an integer in range 1-{self._n}, {val=!r}"
        assert self._is_empty_pos(x, y), f"Invalid position. Position must be empty."

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
        for new_x in range(current_row, self._n):
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
        assert val == '.' or isinstance(val, int) and 1 <= val <= self._n, \
            f"Invalid value. val should be an integer in range 1-9 or a single dot '.', {val=!r}"
        assert isinstance(x, int) and 0 <= x <= self._n - 1, \
            f"Invalid x. x should be an integer in range 0-{self._n - 1}, {x=!r}"
        assert isinstance(y, int) and 0 <= y <= self._n - 1, \
            f"Invalid y. y should be an integer in range 0-{self._n - 1}, {y=!r}"

        self._rows[x][y] = val
        self._all[x * self._n + y] = val
        self._columns[y][x] = val
        self._blocks[self._get_block_by_pos(x, y)][x % self._sqrt * self._sqrt + y % self._sqrt] = val

    def solve(self, current_row=0):
        """A recursive method that tries to solve the board.
         If the board was solved, True is returned, otherwise False."""
        x, y = self._find_next_pos(current_row)
        if y == -1:
            return True
        for i in range(1, self._n + 1):
            if self._check_value_in_pos(i, x, y):
                self._set_value(i, x, y)
                if self.solve(x):
                    return True
                self._set_value('.', x, y)
        return False

    def is_solved(self):
        try:
            self._all.index('.')
        except ValueError:
            return True
        else:
            return False
