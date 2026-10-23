from rally_interfaces.msg import DriverStatus, Instruction, RaceMap
from rally_navigator.grid import Cell, GridMap
from rally_navigator.route import find_route, route_to_instructions
from rcl_interfaces.msg import SetParametersResult
from rclpy.qos import DurabilityPolicy, QoSProfile, ReliabilityPolicy

MAP_TOPIC = '/race/map'
STATUS_TOPIC = '/miru/status'
INSTRUCTION_TOPIC = '/navigator/instruction'
INSTRUCTIONS_AHEAD_PARAM = 'instructions_ahead'

DEFAULT_INSTRUCTIONS_AHEAD = 2
MIN_INSTRUCTIONS_AHEAD = 1
MAX_INSTRUCTIONS_AHEAD = 5

TURN_NAMES = {
    Instruction.TURN_NONE: 'finish',
    Instruction.TURN_LEFT: 'belok kiri',
    Instruction.TURN_RIGHT: 'belok kanan',
}

class NavigatorNode:
    def __init__(self, node):
        self.node = node

        self.grid = None
        self.instructions = []
        self.last_status = None
        self.sent_count = 0

        # TODO: TASK A - Subscribe ke MAP_TOPIC callback on_map dengan QoS transient_local dan reliable
        map_qos = QoSProfile(
            depth = 1,
            reliability = ReliabilityPolicy.RELIABLE,
            durability = DurabilityPolicy.TRANSIENT_LOCAL
        )
        self.map_subscription = node.create_subscription(RaceMap, MAP_TOPIC, self.on_map, map_qos)

        # TODO: TASK E - Buat publisher untuk INSTRUCTION_TOPIC dan subscriber untuk STATUS_TOPIC callback on_status
        self.instruction_publisher = node.create_publisher(Instruction, INSTRUCTION_TOPIC ,10)

        self.status_subscription = node.create_subscription(DriverStatus, STATUS_TOPIC, self.on_status, 10)

        # TODO: TASK F - Daftarkan parameter INSTRUCTIONS_AHEAD_PARAM bawaan DEFAULT_INSTRUCTIONS_AHEAD dengan on_parameter_change.
        self.node.declare_parameter(INSTRUCTIONS_AHEAD_PARAM, DEFAULT_INSTRUCTIONS_AHEAD)
        self.node.add_on_set_parameters_callback(self.on_parameter_change)
            
        self.node.get_logger().info('navigator siap')

    # TODO: TASK A
    def on_map(self, msg):
        # Abaikan jika peta sudah ada, atau jika jumlah batunya tidak cocok dengan width*height, tampilkan log error.
        # Jika aman, simpan sebagai GridMap di self.grid, tampilkan log peta diterima, lalu panggil self.plan_route().
        if self.grid is not None:
            return

        if msg.width <= 0 or msg.height <= 0 or len(msg.rocks) != msg.width * msg.height:
            self.node.get_logger().error('peta tidak valid')
            return

        self.grid = GridMap(
            msg.width,
            msg.height,
            msg.rocks,
            Cell(msg.start_col, msg.start_row),
            Cell(msg.finish_col, msg.finish_row),
        )

        rock_count = sum(msg.rocks)
        self.node.get_logger().info(
            f'peta diterima: {msg.width}x{msg.height}, {rock_count} batu, '
            f'start ({msg.start_col}, {msg.start_row}), '
            f'finis ({msg.finish_col}, {msg.finish_row})'
        )
        self.plan_route()
        self.send_instructions()

    # Provided, do not modify
    def plan_route(self):
        route = find_route(self.grid)
        if not route:
            self.node.get_logger().error('tidak ada rute dari start ke finish')
            return

        self.instructions = route_to_instructions(route)
        self.node.get_logger().info(
            f'rute {len(route) - 1} kotak, {len(self.instructions)} instruksi')

    # TODO: TASK E
    def on_status(self, msg):
        # Simpan laporan di self.last_status, lalu panggil self.send_instructions().
        self.last_status = msg
        self.send_instructions()

    def send_instructions(self):
        # Kirim instruksi mulai dari self.sent_count sampai done_id + DEFAULT_INSTRUCTIONS_AHEAD log tiap pengiriman
        # Jangan kirim jika rute belum ada, Miru belum lapor, atau belum ada subscriber (get_subscription_count() masih 0)
        if (
            not self.instructions
            or self.last_status is None
            or self.instruction_publisher.get_subscription_count() == 0
        ):
            return

        ahead = self.node.get_parameter(INSTRUCTIONS_AHEAD_PARAM).value
        limit = min(len(self.instructions), self.last_status.done_id + ahead)

        while self.sent_count < limit:
            inst = self.instructions[self.sent_count]
            self.instruction_publisher.publish(inst)
            self.sent_count += 1
            turn_name = TURN_NAMES.get(inst.turn, str(inst.turn))
            self.node.get_logger().info(
                f'kirim instruksi {inst.id}: maju {inst.distance}, {turn_name}'
            )

    # TODO: TASK F
    def on_parameter_change(self, parameters):
        # Tolak instructions_ahead di luar MIN_INSTRUCTIONS_AHEAD sampai MAX_INSTRUCTIONS_AHEAD, selain itu terima.
        #makes a parameter to accept values from 1 to 5
        for parameter in parameters:
            if parameter.name == INSTRUCTIONS_AHEAD_PARAM:
                if (
                    not isinstance(parameter.value, int)
                    or isinstance(parameter.value, bool)
                    or not (MIN_INSTRUCTIONS_AHEAD <= parameter.value <= MAX_INSTRUCTIONS_AHEAD)
                ):
                    return SetParametersResult(
                        successful=False,
                        reason='instructions_ahead must be between 1 and 5',
                    )

        return SetParametersResult(successful=True)
