import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Point

from xarm_toolkit.targets.mock_click import MockClickTarget
from xarm_toolkit.targets.target_source import TargetSelectionCancelled

"""" This file was made with assistance from LLLM """

def main():
    rclpy.init()
    node = Node('target_publisher')
    pub = node.create_publisher(Point, '/xarm/target', 10)
    source = MockClickTarget()
    rclpy.spin_once(node, timeout_sec=1.0)
    try:
        while rclpy.ok():
            x, y = source.get_target()
            pub.publish(Point(x=x, y=y, z=0.0))
            node.get_logger().info(f'target ({x:.0f}, {y:.0f})')
            rclpy.spin_once(node, timeout_sec=0.1)
    except TargetSelectionCancelled:
        pass
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()