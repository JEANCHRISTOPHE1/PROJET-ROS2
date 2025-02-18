import rclpy
from rclpy.node import Node
from std_msgs.msg import Float64
from flask import Flask, render_template
from flask_socketio import SocketIO
import threading

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")  # Active WebSocket

class RosSubscriber(Node):
    def __init__(self):
        super().__init__('ros_subscriber')
        self.subscription_temp = self.create_subscription(Float64, 'temperature', self.temp_callback, 10)
        self.subscription_humi = self.create_subscription(Float64, 'humidite', self.humi_callback, 10)

    def temp_callback(self, msg):
        self.get_logger().info(f'Temperature: {msg.data}')
        socketio.emit('temperature_update', {'temperature': msg.data})  # Envoie via WebSocket

    def humi_callback(self, msg):
        self.get_logger().info(f'Humidité: {msg.data}')
        socketio.emit('humidity_update', {'humidity': msg.data})  # Envoie via WebSocket

@app.route('/')
def index():
    return render_template('index.html')  # Charge la page HTML

def ros_spin():
    rclpy.init()
    node = RosSubscriber()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    ros_thread = threading.Thread(target=ros_spin, daemon=True)
    ros_thread.start()  # Lancer ROS2 en parallèle
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)

