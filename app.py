import rclpy
from rclpy.node import Node
from std_msgs.msg import Float64
from flask import Flask, send_from_directory,send_file
from flask_socketio import SocketIO
import threading
import os

# Initialisation de Flask et WebSocket
app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

class RosSubscriber(Node):
    """ Noeud ROS2 qui souscrit aux topics température et humidité """
    def __init__(self):
        super().__init__('ros_subscriber')
        self.create_subscription(Float64, 'temperature', self.temp_callback, 10)
        self.create_subscription(Float64, 'humidite', self.humi_callback, 10)

    def temp_callback(self, msg):
        self.get_logger().info(f'Température reçue: {msg.data}')
        socketio.emit('temperature_update', {'temperature': msg.data})  # Envoi WebSocket

    def humi_callback(self, msg):
        self.get_logger().info(f'Humidité reçue: {msg.data}')
        socketio.emit('humidity_update', {'humidity': msg.data})  # Envoi WebSocket

@app.route('/')
def index():
    """ Sert le fichier HTML principal """
    return send_file('index.html')

@app.route('/java.js')
def javascript():
    """ Sert le fichier JavaScript """
    return send_from_directory(os.getcwd(), 'java.js')

@app.route('/style.css')
def css():
    """ Sert le fichier CSS """
    return send_from_directory(os.getcwd(), 'style.css')

def ros_spin():
    """ Exécute le noeud ROS2 en parallèle """
    rclpy.init()
    node = RosSubscriber()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

def main():
    """ Point d'entrée ROS2 """
    global ros_thread
    ros_thread = threading.Thread(target=ros_spin, daemon=True)
    ros_thread.start()
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)

if __name__ == '__main__':
    main()

