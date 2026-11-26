# Copyright 2016 Open Source Robotics Foundation, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""This file's creation used research based from Claude desktop"""

import random #

import rclpy
from rclpy.node import Node

from std_msgs.msg import String
from student_id_publisher import STUDENT_ID_LAST4 #


class StudentSubscriber(Node):

    def __init__(self):
        super().__init__('student_subscriber')
        self.subscription = self.create_subscription(
            String,
            'student_data',
            self.listener_callback,
            10)
        self.subscription  # prevent unused variable warning
        self.count = 0 #
        self.total = 0 #

    def listener_callback(self, msg): #
        try: 
            value = int(msg.data.split(': ')[1]) #
        except (IndexError, ValueError): #
            self.get_logger().error('Received invalid message: "%s"' % msg.data) #
            return #

        self.count += 1 #
        self.total += value #
        average = self.total / self.count #

        self.get_logger().info(f'I heard: "{msg.data}", Count: {self.count}, Average: {average:.2f}') #


def main(args=None):
    rclpy.init(args=args)

    student_subscriber = StudentSubscriber()

    rclpy.spin(student_subscriber)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    student_subscriber.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
