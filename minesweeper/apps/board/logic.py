from random import randrange
from typing import List

from board.models import Board, BoardCell
from django.db.models.query import QuerySet

from minesweeper.core.logic import BaseLogic


class BoardLogic(BaseLogic):

    def __init__(self):
        super().__init__()

        self.model = Board


class BoardCellLogic(BaseLogic):

    def __init__(self):
        super().__init__()

        self.model = BoardCell

    def bulk_update(
        self, objs: List[BoardCell], fields: List[str]
    ) -> List[BoardCell]:

        return self.model.objects.bulk_update(objs, fields=fields)

    def generate_board_cells_by_board(
        self, board: Board
    ) -> 'QuerySet[BoardCell]':

        width = board.width
        height = board.height

        MAX_FLAGS = (width * height) / 4
        flags, cells = 0, []
        for y in range(height):
            row = []
            for x in range(width):
                value = randrange(BoardCell.FLAG_VALUE, 1)
                if value == BoardCell.FLAG_VALUE:
                    flags += 1

                if flags > MAX_FLAGS:
                    value = 0

                row.append(self.model(x=x, y=y, value=value, board=board))
            cells.append(row)

        for y in range(height):
            for x in range(width):
                if cells[y][x].is_flag:
                    continue

                counter = 0
                variants_y = self.get_variants(y, len(cells))
                variants_x = self.get_variants(x, len(cells[y]))

                # horizontal
                for vy in variants_y:
                    if cells[y + vy][x].is_flag:
                        counter += 1

                # vertical
                for vx in variants_x:
                    if cells[y][x + vx].is_flag:
                        counter += 1

                # diagonal
                for vy in variants_y:
                    for vx in variants_x:
                        if cells[y + vy][x + vx].is_flag:
                            counter +=1

                cells[y][x].value = counter

        objs = [cell for row in cells for cell in row]
        return self.model.objects.bulk_create(objs)


    def inspect_board_cell(self, start: BoardCell) -> 'QuerySet[BoardCell]':

        if start.is_flag:
            start.show = True
            return [start]

        cells = []
        board = start.board
        width = board.width
        x = start.x
        y = start.y

        board_cells = list(self.find(board_id=board.id).order_by('y', 'x'))
        cells = [
            board_cells[idx * width:(idx + 1) * width] for idx in range(width)
        ]
        return self.check_board_cell(y=y, x=x, cells=cells, visited=[])


    def check_board_cell(
        self,
        y: int,
        x: int,
        cells: List[List[BoardCell]],
        visited: List[BoardCell]
    ) -> List[BoardCell]:

        cells_found = []

        if y < 0 or x < 0 or y >= len(cells) or x >= len(cells[y]):
            return cells_found

        cells[y][x].show = True

        cells_found.append(cells[y][x])
        visited.append(cells[y][x])

        if cells[y][x].is_flag:
            return cells_found

        if cells[y][x].value != 0:
            return cells_found

        variants_y = self.get_variants(y, len(cells))
        variants_x = self.get_variants(x, len(cells[y]))

        # horizontal
        for vy in variants_y:
            cell = cells[y + vy][x]
            if cell not in visited and cell.value >= 0:
                cells_found.extend(
                    self.check_board_cell(y + vy, x, cells, visited)
                )

        # vertical
        for vx in variants_x:
            cell = cells[y][x + vx]
            if cell not in visited and cell.value >= 0:
                cells_found.extend(
                    self.check_board_cell(y, x + vx, cells, visited)
                )

        # diagonal
        for vy in variants_y:
            for vx in variants_x:
                cell = cells[y + vy][x + vx]
                if cell not in visited and cell.value >= 0:
                    cells_found.extend(
                        self.check_board_cell(y + vy, x + vx, cells, visited)
                    )

        return cells_found

    def get_variants(self, value: int, rows_len: int) -> List[int]:
        variants = []

        if value < rows_len - 1:
            variants.append(1)

        if value > 0:
            variants.append(-1)

        return variants
