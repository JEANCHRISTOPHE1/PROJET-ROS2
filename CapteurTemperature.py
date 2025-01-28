import rclpy
from rclpy.node import Node

from std_msgs.msg import Float64


class TempPublisher(Node):

    def __init__(self):
        super().__init__('temp_publisher')
        self.publisher_ = self.create_publisher(Float64, 'temperature', 10)
        timer_period = 0.5  # seconds
        self.timer = self.create_timer(timer_period, self.timer_callback)
        self.i = 20.0

    def timer_callback(self):
    	if self.i >= 42.0:
    		self.i = 42.0
    	else :
    		self.i += 0.1
    	msg = Float64()
    	msg.data = self.i
    	self.publisher_.publish(msg)
    	self.get_logger().info('Publishing: "%lf"' % msg.data)


def main(args=None):
    rclpy.init(args=args)

    temp_publisher = TempPublisher()

    rclpy.spin(temp_publisher)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    temp_publisher.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
