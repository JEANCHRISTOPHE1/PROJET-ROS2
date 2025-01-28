import rclpy
from rclpy.node import Node
from std_msgs.msg import Float64


class VentiSubscriber(Node):

    def __init__(self):
        super().__init__('venti_subscriber')
        self.humidite = self.create_subscription(Float64,'humidite',self.hear_humi,10)
        self.humidite  # prevent unused variable warning
        self.temperature = self.create_subscription(Float64,'temperature',self.hear_temp,10)
        self.temperature  # prevent unused variable warning

    def hear_humi(self, msg):
    	if msg.data > 60.0 :
    		self.get_logger().info('L humidité est trop elever %lf pourcent, activation de la ventilation' % msg.data)
    	else :
    		self.get_logger().info('L humidité est de %lf pourcent' % msg.data)
        
    def hear_temp(self, msg):
        if msg.data > 30.0 :
        	self.get_logger().info('La temperature est trop elever %lf degres celcus, activation de laventilation' % msg.data)
        else :
        	self.get_logger().info('La temperature est de %lf degres celcus' % msg.data)


def main(args=None):
    rclpy.init(args=args)

    venti_subscriber = VentiSubscriber()

    rclpy.spin(venti_subscriber)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    venti_subscriber.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
