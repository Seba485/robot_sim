#!/usr/bin/env python3
import rospy
from geometry_msgs.msg import Twist
import sys, select, termios, tty

def getKey():
    tty.setraw(sys.stdin.fileno())
    select.select([sys.stdin], [], [], 0)
    key = sys.stdin.read(1)
    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
    return key

def keyboard_controller():
    rospy.init_node('keyboard_controller', anonymous=True)

    rospy.loginfo("wasd controller up: contrl with wasd, stop with ' ' and exit with 'x'")

    controller_topic = rospy.get_param("~controller_topic")

    pub = rospy.Publisher(controller_topic, Twist, queue_size=10)
    rate = rospy.Rate(1000)
    twist = Twist()

    while not rospy.is_shutdown():
        key = getKey()
        if key == 'w':
            twist.linear.x = 0.5
        elif key == 's':
            twist.linear.x = -0.5
        elif key == 'a':
            twist.angular.z = 0.5
        elif key == 'd':
            twist.angular.z = -0.5
        elif key == ' ':
            twist.linear.x = 0.0
            twist.angular.z = 0.0
        elif key == 'x':
            rospy.loginfo('Controlller didabled succesfully')
            rospy.signal_shutdown('Controlller didabled succesfully')

        pub.publish(twist)
        rate.sleep()

if __name__ == '__main__':
    settings = termios.tcgetattr(sys.stdin)
    try:
        keyboard_controller()
    except rospy.ROSInterruptException:
        pass
    finally:
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)