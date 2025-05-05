import rclpy
from subprocess import run
from subprocess import call
from rclpy.node import Node
from time import sleep

from dimits import Dimits

from std_msgs.msg import String

dt = Dimits('en_GB-southern_english_female-low')

class MainSubscriber(Node):

    def __init__(self):
        super().__init__('main_subscriber')
        self.subscription = self.create_subscription(
            String,
            'voice',
            self.listener_callback,
            10)
        self.subscription  # prevent unused variable warning
        self.opencvpublisher_ = self.create_publisher(String, 'opencv', 10)
        self.servopublisher_ = self.create_publisher(String, 'servo', 10)        
    def listener_callback(self, msg):
        self.get_logger().info('      Publishing Main Voice data "%s"' % msg.data)
        # Turn off the microphone
        sleep(2)
        run(["amixer", "-D", "default", "set", "Capture", "nocap"], check=True)
#        call(["pactl", "set-source-mute", "0", "toggle"])
#        # Execute espeak using subprocess.run()
        dt.text_2_speech("Incoming Data", engine="aplay")
#        call(["espeak", "-ven-us+f3", msg.data])
        sleep(2)
        #Turn on the microphone
        run(["amixer", "-D", "default", "set", "Capture", "cap"], check=True)
#        call(["pactl", "set-source-mute", "0", "toggle"])
        if (msg.data == "home"):
            servo_msg = String()
            servo_msg.data = '%s' % msg.data
            self.servopublisher_.publish(servo_msg)
            self.get_logger().info('Main to servo: "%s"' % servo_msg.data)
        elif (msg.data == "reach"):
            servo_msg = String()
            servo_msg.data = '%s' % msg.data
            self.servopublisher_.publish(servo_msg)
            self.get_logger().info('Main to servo: "%s"' % servo_msg.data)
        elif (msg.data == "wave"):
            servo_msg = String()
            servo_msg.data = '%s' % msg.data
            self.servopublisher_.publish(servo_msg)
            self.get_logger().info('Main to servo: "%s"' % servo_msg.data)      
        elif (msg.data == "find"):
            opencv_msg = String()
            opencv_msg.data = '%s' % msg.data
            self.opencvpublisher_.publish(opencv_msg)
            self.get_logger().info('Main to Opencv: "%s"' % opencv_msg.data)

def main(args=None):
    rclpy.init(args=args)

    main_subscriber = MainSubscriber()
    dt.text_2_speech("Welcome to my robot", engine="aplay")
    rclpy.spin(main_subscriber)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    main_subscriber.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
