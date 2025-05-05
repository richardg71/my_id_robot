from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    ld = LaunchDescription()

    main_node = Node(
        package="my_id_robot",
        executable="main_subscriber",
        name="main"
    )

    opencv_node = Node(
        package="my_id_robot",
        executable="opencv_subscriber",
        name="opencv"
    )

    servo_node = Node(
        package="my_id_robot",
        executable="servo_subscriber",
        name="servo"
    )

    voice_node = Node(
        package="my_id_robot",
        executable="voice_publisher",
        name="voice",
        output="screen"
    )   

    ld.add_action(main_node)
    ld.add_action(servo_node)
    ld.add_action(voice_node)
    ld.add_action(opencv_node)
    return ld
