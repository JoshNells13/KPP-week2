from rally_wasit.stage import is_rock
import rclpy
from rclpy.node import Node
from std_srvs.srv import Empty
from turtlesim.srv import Kill, SetPen, Spawn, TeleportAbsolute

# Provided, do not modify. Draws the stage on the turtlesim canvas with a
# helper turtle that has a pen, then removes the helper again.

PAINTER_NAME = 'painter'
CALL_TIMEOUT = 2.0  # [s]

GRID_COLOR = (90, 90, 90)
ROCK_COLOR = (220, 40, 40)
START_COLOR = (70, 130, 255)
FINISH_COLOR = (60, 220, 90)
TRAIL_COLOR = (255, 255, 255)

ROCK_INSET = 0.15  # [m] gap between a rock and the edge of its cell
MARK_INSET = 0.06  # [m]


def cell_center(col, row):
    return col + 1.0, row + 1.0


class Painter:
    def __init__(self, node: Node):
        self.node = node
        self.clear_client = node.create_client(Empty, '/clear')
        self.spawn_client = node.create_client(Spawn, '/spawn')
        self.kill_client = node.create_client(Kill, '/kill')
        self.turtle1_pen = node.create_client(SetPen, '/turtle1/set_pen')
        self.turtle1_teleport = node.create_client(TeleportAbsolute, '/turtle1/teleport_absolute')
        self.painter_pen = node.create_client(SetPen, f'/{PAINTER_NAME}/set_pen')
        self.painter_teleport = node.create_client(
            TeleportAbsolute, f'/{PAINTER_NAME}/teleport_absolute')

    def is_ready(self):
        return all(client.service_is_ready() for client in (
            self.clear_client, self.spawn_client, self.kill_client, self.turtle1_pen,
            self.turtle1_teleport))

    def call(self, client, request):
        future = client.call_async(request)
        rclpy.spin_until_future_complete(self.node, future, timeout_sec=CALL_TIMEOUT)
        return future.result()

    def pen(self, client, color, width, off):
        self.call(client, SetPen.Request(
            r=color[0], g=color[1], b=color[2], width=width, off=1 if off else 0))

    def move(self, client, x, y, theta=0.0):
        self.call(client, TeleportAbsolute.Request(x=float(x), y=float(y), theta=float(theta)))

    def draw_path(self, points, color):
        self.pen(self.painter_pen, color, 3, True)
        self.move(self.painter_teleport, *points[0])
        self.pen(self.painter_pen, color, 3, False)
        for x, y in points[1:]:
            self.move(self.painter_teleport, x, y)
        self.pen(self.painter_pen, color, 3, True)

    def draw_square(self, col, row, inset, color):
        x, y = cell_center(col, row)
        half = 0.5 - inset
        corners = [(x - half, y - half), (x + half, y - half), (x + half, y + half),
                   (x - half, y + half), (x - half, y - half)]
        self.draw_path(corners, color)

    def draw_rock(self, col, row):
        self.draw_square(col, row, ROCK_INSET, ROCK_COLOR)
        x, y = cell_center(col, row)
        half = 0.5 - ROCK_INSET
        self.draw_path([(x - half, y - half), (x + half, y + half)], ROCK_COLOR)
        self.draw_path([(x - half, y + half), (x + half, y - half)], ROCK_COLOR)

    def draw_stage(self, stage):
        self.call(self.clear_client, Empty.Request())
        self.call(self.spawn_client, Spawn.Request(x=1.0, y=1.0, theta=0.0, name=PAINTER_NAME))

        # Border of the grid.
        low = 0.5
        high_x = stage.width + 0.5
        high_y = stage.height + 0.5
        self.draw_path(
            [(low, low), (high_x, low), (high_x, high_y), (low, high_y), (low, low)], GRID_COLOR)

        for row in range(stage.height):
            for col in range(stage.width):
                if is_rock(stage, col, row):
                    self.draw_rock(col, row)

        self.draw_square(*stage.start, MARK_INSET, START_COLOR)
        self.draw_square(*stage.finish, MARK_INSET, FINISH_COLOR)
        self.draw_square(*stage.finish, MARK_INSET + 0.12, FINISH_COLOR)

        self.call(self.kill_client, Kill.Request(name=PAINTER_NAME))

    def place_miru(self, stage):
        x, y = cell_center(*stage.start)
        self.pen(self.turtle1_pen, TRAIL_COLOR, 2, True)
        self.move(self.turtle1_teleport, x, y, 0.0)
        self.pen(self.turtle1_pen, TRAIL_COLOR, 2, False)
