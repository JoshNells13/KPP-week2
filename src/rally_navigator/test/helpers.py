# Provided, do not modify.

from collections import deque

from rally_interfaces.msg import Instruction
from rally_navigator.grid import (
    Cell, DIRECTION_COL, DIRECTION_COUNT, DIRECTION_ROW, EAST, GridMap)


def make_map(rows_from_top):
    # '#' batu, 'S' start, 'F' finis, selain itu kotak kosong.
    height = len(rows_from_top)
    width = len(rows_from_top[0])
    rocks = [0] * (width * height)
    start = finish = Cell(0, 0)
    for row in range(height):
        text = rows_from_top[height - 1 - row]
        for col in range(width):
            if text[col] == '#':
                rocks[row * width + col] = 1
            elif text[col] == 'S':
                start = Cell(col, row)
            elif text[col] == 'F':
                finish = Cell(col, row)
    return GridMap(width, height, rocks, start, finish)


def make_instruction(instruction_id, distance, turn):
    return Instruction(id=instruction_id, distance=distance, turn=turn)


def shortest_steps(grid):
    # Jumlah langkah rute terpendek, atau -1 kalau tidak ada. Ditulis terpisah dari find_route.
    distance = {grid.start: 0}
    pending = deque([grid.start])
    while pending:
        cell = pending.popleft()
        for d in range(DIRECTION_COUNT):
            neighbor = Cell(cell.col + DIRECTION_COL[d], cell.row + DIRECTION_ROW[d])
            if grid.inside(neighbor) and not grid.is_rock(neighbor) and neighbor not in distance:
                distance[neighbor] = distance[cell] + 1
                pending.append(neighbor)
    return distance.get(grid.finish, -1)


def drive(grid, instructions):
    # Menjalankan instruksi seperti Miru. Hasilnya kotak terakhir, atau None kalau
    # keluar dari grid atau masuk kotak batu.
    cell = grid.start
    heading = EAST
    for instruction in instructions:
        for _ in range(instruction.distance):
            cell = Cell(cell.col + DIRECTION_COL[heading], cell.row + DIRECTION_ROW[heading])
            if not grid.inside(cell) or grid.is_rock(cell):
                return None
        if instruction.turn == Instruction.TURN_LEFT:
            heading = (heading + 1) % DIRECTION_COUNT
        elif instruction.turn == Instruction.TURN_RIGHT:
            heading = (heading - 1) % DIRECTION_COUNT
    return cell


def random_map(rng):
    rocks = [1 if rng.random() < 0.25 else 0 for _ in range(100)]
    start = Cell(0, rng.randrange(10))
    finish = Cell(9, rng.randrange(10))
    rocks[start.row * 10 + start.col] = 0
    rocks[finish.row * 10 + finish.col] = 0
    return GridMap(10, 10, rocks, start, finish)
