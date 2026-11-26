import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Point
from std_msgs.msg import String

"""" This file was made with assistance from LLLM """


class ArmSubscriber(Node):
    def __init__(self):
        super().__init__('arm_subscriber')
        self.sub = self.create_subscription(Point, '/xarm/target', self.on_target, 10)
        self.cmd = self.create_publisher(String, '/xarm/command', 10)

    def on_target(self, msg):
        pan = max(0, min(1000, int(msg.x / 800 * 1000)))
        lift = max(0, min(1000, int((1 - msg.y / 600) * 1000)))
        out = String()
        out.data = f'0/500/500/500/{lift}/{pan}'
        self.cmd.publish(out)
        self.get_logger().info(f'target ({msg.x:.0f},{msg.y:.0f}) -> {out.data}')


def main():
    rclpy.init()
    node = ArmSubscriber()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()