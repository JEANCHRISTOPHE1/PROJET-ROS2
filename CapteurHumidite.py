import rclpy
from rclpy.node import Node

from std_msgs.msg import Float64


class HumiPublisher(Node):

    def __init__(self):
        super().__init__('humi_publisher')
        self.publisher_ = self.create_publisher(Float64, 'humidite', 10)
        timer_period = 1  # seconds
        self.timer = self.create_timer(timer_period, self.timer_callback)
        self.i = 40.0

    def timer_callback(self):
    	if self.i > 100:
        	self.i = 10.0
    	else :
    		self.i += 0.5
    	msg = Float64()
    	msg.data = self.i
    	self.publisher_.publish(msg)
    	self.get_logger().info('Publishing: "%lf"' % msg.data)


def main(args=None):
    rclpy.init(args=args)

    humi_publisher = HumiPublisher()

    rclpy.spin(humi_publisher)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    humi_publisher.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
# TYRANNOSAURE
