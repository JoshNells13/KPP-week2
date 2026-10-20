from typing import NamedTuple

# Provided, do not modify.

# Kolom 0 ada di kiri dan baris 0 ada di bawah.
class Cell(NamedTuple):
    col: int
    row: int

# Empat arah yang urut berlawanan arah jarum jam: timur, utara, barat, selatan.
# Belok kiri berarti pindah ke arah berikutnya (timur ke utara), belok kanan
# berarti pindah ke arah sebelumnya (timur ke selatan).
DIRECTION_COUNT = 4
DIRECTION_COL = (1, 0, -1, 0)
DIRECTION_ROW = (0, 1, 0, -1)
EAST = 0

class GridMap:
    def __init__(self, width, height, rocks, start, finish):
        self.width = width
        self.height = height
        self.rocks = list(rocks)
        self.start = start
        self.finish = finish

    def inside(self, cell):
        return 0 <= cell.col < self.width and 0 <= cell.row < self.height

    def is_rock(self, cell):
        return self.rocks[cell.row * self.width + cell.col] == 1
