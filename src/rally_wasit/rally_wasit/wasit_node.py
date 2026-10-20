import math
import time

from rally_interfaces.msg import RaceMap, RaceState
from rally_wasit.painter import Painter
from rally_wasit.stage import generate_stage, is_rock, route_length
import rclpy
from rclpy.qos import DurabilityPolicy, HistoryPolicy, QoSProfile, ReliabilityPolicy
from turtlesim.msg import Pose

# Provided, do not modify. The referee: builds and draws the stage, starts the
# race, keeps time and hands out penalties.

UPDATE_PERIOD = 0.1  # [s]

MAP_TOPIC = '/race/map'
STATE_TOPIC = '/race/state'
POSE_TOPIC = '/turtle1/pose'
MIRU_STATUS_TOPIC = '/miru/status'

SEED_PARAM = 'seed'
COUNTDOWN_PARAM = 'countdown'
TIME_LIMIT_PARAM = 'time_limit'

JUMP_START_DISTANCE = 0.05  # [m] movement before GO that counts as a jump start
JUMP_START_PENALTY = 10.0  # [s]
ROCK_PENALTY = 5.0  # [s]

MIRU_NODE = 'miru'
NAVIGATOR_NODE = 'navigator'


class WasitNode:
    def __init__(self, node):
        self.node = node

        node.declare_parameter(SEED_PARAM, -1)
        node.declare_parameter(COUNTDOWN_PARAM, 3.0)  # [s]
        node.declare_parameter(TIME_LIMIT_PARAM, 120.0)  # [s]

        seed = node.get_parameter(SEED_PARAM).value
        if seed < 0:
            seed = time.time_ns() % (2**31)
        self.stage = generate_stage(seed)
        self.seed = seed

        latched = QoSProfile(
            depth=1, history=HistoryPolicy.KEEP_LAST, reliability=ReliabilityPolicy.RELIABLE,
            durability=DurabilityPolicy.TRANSIENT_LOCAL)
        self.map_publisher = node.create_publisher(RaceMap, MAP_TOPIC, latched)
        self.state_publisher = node.create_publisher(RaceState, STATE_TOPIC, 10)
        node.create_subscription(Pose, POSE_TOPIC, self.on_pose, 10)

        self.painter = Painter(node)
        self.setup_done = False
        self.state = RaceState.PREPARING
        self.pose = None
        self.countdown_start = 0.0
        self.countdown_mark = 0
        self.go_time = 0.0
        self.final_elapsed = 0.0
        self.penalty = 0.0
        self.jump_started = False
        self.rocks_hit = set()
        self.cheats_reported = set()

        self.timer = None
        node.get_logger().info('wasit siap')

    def elapsed(self):
        if self.state == RaceState.GO:
            return time.monotonic() - self.go_time
        if self.state in (RaceState.FINISHED, RaceState.FAILED):
            return self.final_elapsed
        return 0.0

    def cell_of(self, pose):
        return round(pose.x - 1.0), round(pose.y - 1.0)

    def start(self):
        # Draws the stage before the node starts spinning: the painter waits for
        # every service call, which is not allowed inside a callback.
        while rclpy.ok() and not self.painter.is_ready():
            self.node.get_logger().info('menunggu turtlesim...', throttle_duration_sec=2.0)
            rclpy.spin_once(self.node, timeout_sec=0.1)
        if not rclpy.ok():
            return False

        self.painter.draw_stage(self.stage)
        self.painter.place_miru(self.stage)
        self.map_publisher.publish(self.build_map())
        self.setup_done = True

        steps = route_length(self.stage)
        self.node.get_logger().info(
            f'lintasan seed {self.seed}: start {self.stage.start}, finis {self.stage.finish}, '
            f'rute terpendek {steps} kotak')

        self.timer = self.node.create_timer(UPDATE_PERIOD, self.update)
        return True

    def build_map(self):
        msg = RaceMap()
        msg.width = self.stage.width
        msg.height = self.stage.height
        msg.rocks = list(self.stage.rocks)
        msg.start_col, msg.start_row = self.stage.start
        msg.finish_col, msg.finish_row = self.stage.finish
        return msg

    def check_cheating(self):
        # Miru must not read the map and the navigator must not read the pose.
        suspects = (
            (MAP_TOPIC, MIRU_NODE, f'{MIRU_NODE} membaca peta lintasan'),
            (POSE_TOPIC, NAVIGATOR_NODE, f'{NAVIGATOR_NODE} membaca posisi kura-kura langsung'))
        for topic, name, message in suspects:
            for info in self.node.get_subscriptions_info_by_topic(topic):
                if info.node_name == name and message not in self.cheats_reported:
                    self.cheats_reported.add(message)
                    self.node.get_logger().warn(f'CURANG: {message}')

    def players_ready(self):
        return self.node.count_publishers(MIRU_STATUS_TOPIC) > 0

    def update(self):
        self.check_cheating()
        logger = self.node.get_logger()

        if self.state == RaceState.PREPARING:
            if self.players_ready():
                self.state = RaceState.COUNTDOWN
                self.countdown_start = time.monotonic()
                self.countdown_mark = 0
            else:
                logger.info('menunggu miru...', throttle_duration_sec=2.0)

        elif self.state == RaceState.COUNTDOWN:
            countdown = self.node.get_parameter(COUNTDOWN_PARAM).value
            remaining = countdown - (time.monotonic() - self.countdown_start)
            mark = math.ceil(remaining)
            if remaining <= 0.0:
                self.state = RaceState.GO
                self.go_time = time.monotonic()
                logger.info('GO!')
            elif mark != self.countdown_mark:
                self.countdown_mark = mark
                logger.info(f'{mark}...')

        elif self.state == RaceState.GO:
            limit = self.node.get_parameter(TIME_LIMIT_PARAM).value
            if self.elapsed() > limit:
                self.end_race(RaceState.FAILED, f'gagal, waktu habis ({limit:.0f} s)')

        self.publish_state()

    def publish_state(self):
        msg = RaceState()
        msg.state = self.state
        msg.elapsed = float(self.elapsed())
        msg.penalty = float(self.penalty)
        self.state_publisher.publish(msg)

    def on_pose(self, msg):
        self.pose = msg
        if not self.setup_done:
            return

        if self.state in (RaceState.PREPARING, RaceState.COUNTDOWN):
            self.check_jump_start(msg)
        elif self.state == RaceState.GO:
            self.check_position(msg)

    def check_jump_start(self, pose):
        if self.jump_started:
            return
        start_x, start_y = self.stage.start[0] + 1.0, self.stage.start[1] + 1.0
        if math.hypot(pose.x - start_x, pose.y - start_y) > JUMP_START_DISTANCE:
            self.jump_started = True
            self.penalty += JUMP_START_PENALTY
            self.node.get_logger().warn(
                f'jump start, penalti {JUMP_START_PENALTY:.0f} s')

    def check_position(self, pose):
        col, row = self.cell_of(pose)
        if not (0 <= col < self.stage.width and 0 <= row < self.stage.height):
            self.end_race(RaceState.FAILED, 'gagal, keluar lintasan')
            return

        if is_rock(self.stage, col, row) and (col, row) not in self.rocks_hit:
            self.rocks_hit.add((col, row))
            self.penalty += ROCK_PENALTY
            self.node.get_logger().warn(
                f'menabrak batu di kotak ({col}, {row}), penalti {ROCK_PENALTY:.0f} s')

        if (col, row) == self.stage.finish:
            elapsed = self.elapsed()
            total = elapsed + self.penalty
            self.end_race(
                RaceState.FINISHED,
                f'finis {elapsed:.1f} s + penalti {self.penalty:.0f} s = {total:.1f} s')

    def end_race(self, new_state, message):
        self.final_elapsed = self.elapsed()
        self.state = new_state
        if new_state == RaceState.FINISHED:
            self.node.get_logger().info(message)
        else:
            self.node.get_logger().error(message)
        self.publish_state()
