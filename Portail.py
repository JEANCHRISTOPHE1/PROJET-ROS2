import rclpy
from rclpy.node import Node
from std_msgs.msg import String


class PortailSubscriber(Node):

    def __init__(self):
        super().__init__('portail_subscriber')
        self.subscription = self.create_subscription(Pose,'/turtle1/pose',self.listener_callback,10)
        self.subscription  # prevent unused variable warning

    def listener_callback(self, msg):
        self.get_logger().info('I heard: "%s"' % msg.data)


def main(args=None):
    rclpy.init(args=args)

    portail_subscriber = PortailSubscriber()

    rclpy.spin(portail_subscriber)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    portail_subscriber.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
