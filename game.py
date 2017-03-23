from typing import List

from copy import copy

PLAYER_X = 'X'
EMPTY_CELL = '_'
PLAYER_O = 'O'


class Cell:
    def __init__(self, pos):
        self.pos = pos
        self.data = {
            PLAYER_X: 0,
            PLAYER_O: 0
        }
        self.tables = 0

    def __iadd__(self, other):
        self.data[other] += 1
        return self

    def __str__(self):
        return "{}:({:.2f}; {:.2f}) ".format(
            self.pos,
            self.data[PLAYER_X] / self.tables,
            self.data[PLAYER_O] / self.tables,
        )


class Game:
    def __init__(self):
        self.tables = [Table()]  # type: List[Table]

    def step(self, player: int, positions: List[int]):
        new_tables = []
        for table in self.tables:
            if EMPTY_CELL == table.win():
                for pos in positions:
                    if not self.is_allowed(pos):
                        raise ValueError("Клетка {} заполнена, ход в неё невозможен".format(pos))

                    _t = copy(table)
                    _t.add_figure(player, pos)
                    new_tables.append(_t)
            else:
                new_tables.append(table)

        if 0 == len(new_tables):
            raise ValueError("Bad Step!")
        self.tables = new_tables

    def is_allowed(self, pos) -> bool:
        """ Нельзя ходить в полностью заполненную клетку """
        for table in self.tables:
            if table.is_empty(pos):
                return True
        return False

    @property
    def field(self) -> List[Cell]:
        field = [Cell(x) for x in range(9)]

        for table in self.tables:
            for pos, cell in table.cells:
                field[pos] += cell

        act_tables = sum(1 for table in self.tables if table.win() == EMPTY_CELL)

        for cell in field:
            cell.tables = len(self.tables)

        return field

    @property
    def winners(self):
        data = {
            PLAYER_X: 0,
            EMPTY_CELL: 0,
            PLAYER_O: 0,
            'tables': len(self.tables)
        }

        for table in self.tables:
            data[table.win()] += 1

        return data


win_tables = [
    # horisont
    (0, 1, 2),
    (3, 4, 5),
    (6, 7, 8),
    # vertical
    (0, 3, 6),
    (1, 4, 7),
    (2, 5, 8),
    # dyagonales
    (0, 4, 8),
    (2, 4, 6)
]


class Table:
    def __init__(self, table: 'Table' = None):
        self.data = copy(table.data) if table else [EMPTY_CELL for _ in range(9)]

    def add_figure(self, figure, pos) -> bool:
        if self.is_empty(pos):
            self.data[pos] = figure
            return True
        else:
            return False

    def is_empty(self, pos):
        return EMPTY_CELL == self.data[pos]

    def win(self):
        for a, b, c in win_tables:
            if self.data[a] == self.data[b] == self.data[c]\
                    and self.data[a] is not None\
                    and self.data[a] != EMPTY_CELL:
                return self.data[a]
        return EMPTY_CELL

    @property
    def cells(self):
        for i, cell in zip(range(9), self.data):
            if cell != EMPTY_CELL:
                yield i, cell

    def __copy__(self) -> 'Table':
        return Table(self)

    def __str__(self):
        return "".join(self.data)
