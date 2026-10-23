from collections import deque

from rally_interfaces.msg import Instruction
from rally_navigator.grid import Cell, DIRECTION_COL, DIRECTION_COUNT, DIRECTION_ROW, EAST

# Provided, do not modify
#basically to get back the shortest route via 
def trace_back(parent, finish):
    if finish not in parent:
        return []

    route = []
    cell = finish
    while cell is not None:
        route.append(cell)
        cell = parent[cell]
    route.reverse()
    return route

# TODO: TASK B
def find_route(grid):
    # Cari rute terpendek dari grid.start ke grid.finish dengan BFS, tetangga dicek berurutan
    # timur, utara, barat, selatan.
    # Return list kosong kalau tidak ada jalan.
    if not grid.inside(grid.start) or not grid.inside(grid.finish):
        return []

    # Ambil kotak dari pending. Untuk setiap tetangga yang di dalam grid yang bukan batu dan
    # belum dikunjungi, catat asalnya di parent lalu masukkan ke pending.
    parent = {grid.start: None}
    pending = deque([grid.start])

    while pending:
        currentnode = pending.popleft()

        for direction in range(DIRECTION_COUNT):
            neighbor = Cell (currentnode.col + DIRECTION_COL[direction], currentnode.row + DIRECTION_ROW[direction])
            

            if grid.inside(neighbor) and not grid.is_rock(neighbor) and neighbor not in parent:
            
                parent[neighbor] = currentnode
                pending.append(neighbor)

        

    # ... tulis pencariannya di sini ...

    return trace_back(parent, grid.finish)

# TODO: TASK C
def route_to_directions(route):
    # Ubah rute (daftar kotak) jadi daftar
    # arah tiap langkah: 0 timur, 1 utara, 2 barat, 3 selatan.
    directions = []
    #nge cek rutenya mengarah kemana (utara, timur, barat, selatan)
    for x in range(len(route) - 1):
        current = route[x]
        next_cell = route[x+1]

        dx = next_cell.col - current.col
        dy = next_cell.row - current.row

        if dx == 1: #right
            directions.append(0)
        if dx == -1: #left
            directions.append(2)
        if dy == 1: #up
            directions.append(1)
        if dy == -1: #down
            directions.append(3)
    #check
    return directions

# TODO: TASK D
def directions_to_instructions(directions):
    # Gabungkan langkah lurus berturut-turut jadi satu instruksi,
    # dan tutup tiap instruksi dengan belokannya.
    
    # Aturan khusus:
    # - Jika langkah pertama bukan ke timur, Miru harus belok dulu (instruksi pertama jaraknya 0).
    # - Putar balik ditulis dua belok kiri berturut-turut. 
    # - Instruksi terakhir tidak punya belokan (TURN_NONE).
    instructions = []

    def add_instruction(distance, turn):
        instruction = Instruction()
        instruction.id = len(instructions) + 1
        instruction.distance = distance
        instruction.turn = turn
        instructions.append(instruction)

    if not directions:
        add_instruction(0, Instruction.TURN_NONE)
        return instructions

    first_turn = (directions[0] - EAST) % DIRECTION_COUNT
    if first_turn == 1:
        add_instruction(0, Instruction.TURN_LEFT)
    elif first_turn == 3:
        add_instruction(0, Instruction.TURN_RIGHT)
    elif first_turn == 2:
        add_instruction(0, Instruction.TURN_LEFT)            
        add_instruction(0, Instruction.TURN_LEFT)       

    segments = []
    for direction in directions:
        if segments and segments[-1][0] == direction:
            old_direction, distance = segments[-1]
            segments[-1] = (old_direction, distance + 1)
        else:
            segments.append((direction, 1))

    for index, (direction, distance) in enumerate(segments):
        if index == len(segments) - 1:
            add_instruction(distance, Instruction.TURN_NONE)
            continue

        next_direction = segments[index + 1][0]
        turn = (next_direction - direction) % DIRECTION_COUNT

        if turn == 1:
            add_instruction(distance, Instruction.TURN_LEFT)
        elif turn == 3:
            add_instruction(distance, Instruction.TURN_RIGHT)
        else:
            add_instruction(distance, Instruction.TURN_LEFT)
            add_instruction(0, Instruction.TURN_LEFT)

    return instructions

# Provided, do not modify
def route_to_instructions(route):
    return directions_to_instructions(route_to_directions(route))
