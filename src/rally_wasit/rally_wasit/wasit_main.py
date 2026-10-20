from rally_wasit.wasit_node import WasitNode
import rclpy
from rclpy.executors import ExternalShutdownException
from rclpy.node import Node


def main():
    rclpy.init()

    node = Node('wasit')
    wasit_node = WasitNode(node)

    try:
        if wasit_node.start():
            rclpy.spin(node)
    except (KeyboardInterrupt, ExternalShutdownException):
        pass

    del wasit_node
    node.destroy_node()
    rclpy.try_shutdown()


if __name__ == '__main__':
    main()
