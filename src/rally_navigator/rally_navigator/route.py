from collections import deque

from rally_interfaces.msg import Instruction
from rally_navigator.grid import Cell, DIRECTION_COL, DIRECTION_COUNT, DIRECTION_ROW, EAST

# Provided, do not modify
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
    # ... tulis pencariannya di sini ...

    return trace_back(parent, grid.finish)

# TODO: TASK C
def route_to_directions(route):
    # Ubah rute (daftar kotak) jadi daftar arah tiap langkah: 0 timur, 1 utara, 2 barat, 3 selatan.
    return []

# TODO: TASK D
def directions_to_instructions(directions):
    # Gabungkan langkah lurus berturut-turut jadi satu instruksi, dan tutup tiap instruksi dengan belokannya.
    # Aturan khusus:
    # - Jika langkah pertama bukan ke timur, Miru harus belok dulu (instruksi pertama jaraknya 0).
    # - Putar balik ditulis dua belok kiri berturut-turut. 
    # - Instruksi terakhir tidak punya belokan (TURN_NONE).
    return []

# Provided, do not modify
def route_to_instructions(route):
    return directions_to_instructions(route_to_directions(route))
