
import rclpy
from rclpy.node import Node
 
from std_msgs.msg import String

from pyax12.connection import Connection
import time
import math

# Connect to the serial port
serial_connection = Connection(port="/dev/ttyUSB0", baudrate=57600)
dynamixel_id = [1, 8, 3, 5]
dynamixel_angle_home = [0, 0, -90, -45]
dynamixel_angle_reach = [0, -80, -90, -45]


def home(serial_connection, dynamixel_id):
    print("Going home")
    serial_connection.goto(dynamixel_id[0], dynamixel_angle_home[0], speed=100, degrees=True)
    time.sleep(2)    # Wait 1 second
    serial_connection.goto(dynamixel_id[1], dynamixel_angle_home[1], speed=100, degrees=True)
    time.sleep(2)    # Wait 1 second
    serial_connection.goto(dynamixel_id[2], dynamixel_angle_home[2], speed=100, degrees=True)
    time.sleep(2)    # Wait 1 second
    serial_connection.goto(dynamixel_id[3], dynamixel_angle_home[3], speed=100, degrees=True)
    time.sleep(2)    # Wait 1 second
    
def reach(serial_connection, dynamixel_id):
    print("Reaching")
    serial_connection.goto(dynamixel_id[0], dynamixel_angle_reach[0], speed=50, degrees=True)
    time.sleep(2)    # Wait 1 second
    serial_connection.goto(dynamixel_id[1], dynamixel_angle_reach[1], speed=50, degrees=True)
    time.sleep(2)    # Wait 1 second
    serial_connection.goto(dynamixel_id[2], dynamixel_angle_reach[2], speed=50, degrees=True)
    time.sleep(2)    # Wait 1 second
    serial_connection.goto(dynamixel_id[3], dynamixel_angle_reach[3], speed=50, degrees=True)
    time.sleep(2)    # Wait 1 second

def position(serial_connection, dynamixel_id, x, y):
    print("Position")
    print(x)
    print(y)
    home(serial_connection, dynamixel_id)
    x_middle = 160 #This is the midpoint of the arm so starting x
    arm_len = 100
    x = x_middle - x
    my_angle = math.atan2(y, x)
    my_angle = math.degrees(my_angle)
    my_angle = (my_angle - 90.0)
    print(my_angle)
    distance = math.sqrt(x**2 + y**2)
    print(distance)
    distance = distance
    arm_angle = math.acos(distance/arm_len)
    arm_angle = math.degrees(arm_angle)
    serial_connection.goto(dynamixel_id[0], my_angle, speed=50, degrees=True)
    time.sleep(2)    # Wait 1 secon
    first_arm_angle = -90 + arm_angle
    print(first_arm_angle)
    serial_connection.goto(dynamixel_id[1], first_arm_angle, speed=50, degrees=True)
    time.sleep(2)    # Wait 1 second
    second_arm_angle =  -90 + 1.5 * arm_angle
    print(second_arm_angle)
    serial_connection.goto(dynamixel_id[2], second_arm_angle, speed=50, degrees=True)
    time.sleep(2)    # Wait 1 second
    serial_connection.goto(dynamixel_id[3], 0, speed=50, degrees=True)
    time.sleep(2)    # Wait 1 second
   
def wave(serial_connection, dynamixel_id):
    print("Wave")
    serial_connection.goto(dynamixel_id[0], dynamixel_angle_home[0], speed=50, degrees=True)
    time.sleep(2)    # Wait 1 second
    serial_connection.goto(dynamixel_id[1], dynamixel_angle_home[1], speed=50, degrees=True)
    time.sleep(2)    # Wait 1 second
    serial_connection.goto(dynamixel_id[2], dynamixel_angle_home[2], speed=50, degrees=True)
    time.sleep(2)    # Wait 1 second
    serial_connection.goto(dynamixel_id[3], dynamixel_angle_home[3], speed=50, degrees=True)
    time.sleep(2)    # Wait 1 second
    serial_connection.goto(dynamixel_id[2], 20, speed=50, degrees=True)
    time.sleep(2)    # Wait 1 second    
    serial_connection.goto(dynamixel_id[2], dynamixel_angle_home[2], speed=50, degrees=True)
    time.sleep(2)    # Wait 1 second
    serial_connection.goto(dynamixel_id[2], 20, speed=50, degrees=True)
    time.sleep(2)    # Wait 1 second
    serial_connection.goto(dynamixel_id[2], dynamixel_angle_home[2], speed=50, degrees=True)
    time.sleep(2)    # Wait 1 second

class ServoSubscriber(Node):
    def __init__(self):
        super().__init__('servo_subscriber')
        self.subscription = self.create_subscription(
            String,
            'servo',
            self.listener_callback,
            10)
        self.subscription  # prevent unused variable warning

    def listener_callback(self, msg):
        self.get_logger().info('Servo message: "%s"' % msg.data)
        if msg.data == "home":
            home(serial_connection, dynamixel_id)
        if msg.data == "reach":
            reach(serial_connection, dynamixel_id)
        if msg.data == "wave":
            wave(serial_connection, dynamixel_id)            
        if (msg.data.find(":") != -1):
            myposition = msg.data.split(':')
            x = int(myposition[1])
            y = int(myposition[2])
            position(serial_connection, dynamixel_id, x, y)
        msg.data=""
            
def main(args=None):
    rclpy.init(args=args)

    servo_subscriber = ServoSubscriber()

    rclpy.spin(servo_subscriber)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    servo_subscriber.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
