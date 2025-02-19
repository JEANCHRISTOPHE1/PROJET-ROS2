import rclpy
from rclpy.node import Node
from std_msgs.msg import Float64
from std_srvs.srv import Trigger
from flask import Flask, send_file, jsonify, request
import threading
import os

app = Flask(__name__)
temperature = None
humidite = None

class WebSubscriber(Node):
    def __init__(self):
        super().__init__('web_subscriber')
        self.create_subscription(Float64, 'temperature', self.temp_callback, 10)
        self.create_subscription(Float64, 'humidite', self.humi_callback, 10)

    def temp_callback(self, msg):
        global temperature
        temperature = msg.data
        self.get_logger().info(f'Température: {msg.data}')

    def humi_callback(self, msg):
        global humidite
        humidite = msg.data
        self.get_logger().info(f'Humidité: {msg.data}')


class PortailClient(Node):
    def __init__(self):
        super().__init__('portail_client')
        self.cli = self.create_client(Trigger, 'bouton')

        while not self.cli.wait_for_service(timeout_sec=1.0):
            self.get_logger().warn('Portail non disponible, attente...')

    def send_request(self):
        req = Trigger.Request()
        future = self.cli.call_async(req)
        future.add_done_callback(self.response_callback)

    def response_callback(self, future):
        try:
            response = future.result()
            print(f"Réponse ROS2 : {response.message}")
        except Exception as e:
            print(f"Erreur lors de la requête : {e}")


@app.route('/')
def index():
    return send_file(os.path.join(os.getcwd(), 'index.html'))

@app.route('/data', methods=['GET'])
def get_data():
    return jsonify({'temperature': temperature, 'humidite': humidite})

@app.route('/portail', methods=['POST'])
def bouton():
    node = PortailClient()
    node.send_request()
    return jsonify({"message": "Commande envoyée au portail !"})

def ros_spin():
    rclpy.init()
    node = WebSubscriber()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

def main():
    web_thread = threading.Thread(target=ros_spin, daemon=True)
    web_thread.start()
    app.run(host='0.0.0.0', port=5000, debug=True)

if __name__ == '__main__':
    main()

