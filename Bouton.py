import rclpy
from rclpy.node import Node
from std_srvs.srv import Trigger

# Interruption clavier
import sys
import termios
import tty
import select

class BoutonClient(Node):
    def __init__(self):
        super().__init__('bouton_client')
        self.cli = self.create_client(Trigger, 'bouton')
        
        while not self.cli.wait_for_service(timeout_sec=1.0):
            self.get_logger().warn('Attente du Portail')
        
        self.bouton_state = False

    def send_request(self):
        req = Trigger.Request()
        future = self.cli.call_async(req)
        future.add_done_callback(self.response_callback)
    
    def response_callback(self, future):
        try:
            response = future.result()
            self.get_logger().info(f"Portail : {response.message}")
        except Exception as e:
            self.get_logger().error(f"Échec de la requête : {str(e)}")
    
    def keyboard_listener(self):
        while rclpy.ok():
            key = self.get_key()
            if key == " ":
                self.bouton_state = not self.bouton_state
                self.get_logger().info(f"Bouton simulé : {self.bouton_state}")
                self.send_request()
    
    def get_key(self):
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            select.select([sys.stdin], [], [], 0)
            key = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return key


def main(args=None):
    rclpy.init(args=args)
    bouton_client = BoutonClient()

    try:
        bouton_client.keyboard_listener()
    except KeyboardInterrupt:
        print("\nFermeture du simulateur.")
    
    bouton_client.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
# TYRANNOSAURE
