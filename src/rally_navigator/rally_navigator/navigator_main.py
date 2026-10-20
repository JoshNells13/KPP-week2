from rally_navigator.node.navigator_node import NavigatorNode
import rclpy
from rclpy.executors import ExternalShutdownException
from rclpy.node import Node

def main():
    rclpy.init()

    node = Node('navigator')
    navigator_node = NavigatorNode(node)

    try:
        rclpy.spin(node)
    except (KeyboardInterrupt, ExternalShutdownException):
        pass

    del navigator_node
    node.destroy_node()
    rclpy.try_shutdown()

if __name__ == '__main__':
    main()
