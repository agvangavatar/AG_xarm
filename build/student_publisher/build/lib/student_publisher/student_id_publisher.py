import rclpy
from rclpy.node import Node
import random #

"""This file's creation used research based from Claude desktop"""

from std_msgs.msg import String

STUDENT_ID_LAST4 = "3477"

class StudentPublisher(Node):

    def __init__(self):
        super().__init__('student_publisher')
        self.publisher_ = self.create_publisher(String, 'student_data', 10)
        timer_period = 1.0  # 1 second
        self.timer = self.create_timer(timer_period, self.timer_callback)

    def timer_callback(self):
        msg = String()
        msg.data = f'STUD_{STUDENT_ID_LAST4}: {random.randint(1, 1000)}' #
        self.publisher_.publish(msg)
        self.get_logger().info('Publishing %s: "%s"' % (STUDENT_ID_LAST4, msg.data))

def main(args=None):
    rclpy.init(args=args)

    student_publisher = StudentPublisher()

    rclpy.spin(student_publisher)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    student_publisher.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
