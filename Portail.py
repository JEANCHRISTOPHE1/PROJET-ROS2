import rclpy
from rclpy.node import Node
from std_srvs.srv import Trigger


class PortailServer(Node):
    def __init__(self):
        super().__init__('portail_server')
        self.srv = self.create_service(Trigger, 'bouton', self.portail_callback)
        self.etat = True
    
    def portail_callback(self, request, response):
        response.success = True
        if not self.etat:
            self.get_logger().info('Portail Fermé')
            self.etat = True
        else:
            self.get_logger().info('Portail Ouvert')
            self.etat = False
        return response
    

def main(args=None):
    rclpy.init(args=args)
    node = PortailServer()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
# TYRANNOSAURE
