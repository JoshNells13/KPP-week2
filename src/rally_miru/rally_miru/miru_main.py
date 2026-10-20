from rally_miru.node.miru_node import MiruNode
import rclpy
from rclpy.executors import ExternalShutdownException
from rclpy.node import Node


def main():
    rclpy.init()

    node = Node('miru')
    miru_node = MiruNode(node)

    try:
        rclpy.spin(node)
    except (KeyboardInterrupt, ExternalShutdownException):
        pass

    del miru_node
    node.destroy_node()
    rclpy.try_shutdown()


if __name__ == '__main__':
    main()
