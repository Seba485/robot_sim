#!/usr/bin/env python3
import rospy
from geometry_msgs.msg import Twist
from rosneuro_msgs.msg import*

class neuro_controller_node:

    def __init__(self):
        rospy.init_node('neuro_controller')

        #get param
        self.sub_topic = rospy.get_param("~neuro_topic") #output of the classification
        self.th = rospy.get_param('~threshold')
        self.reset_flag = rospy.get_param("~reset_after_command")
        self.pub_topic = rospy.get_param("~controller_topic") #command cmd_vel
        self.time_of_command = rospy.get_param("~time_of_command")

        #check on param
        if self.reset_flag!=0 and self.reset_flag!=1:
            rospy.logerr("Reset_after_command must be 0 (off) or 1 (on)") 
            rospy.signal_shutdown()
    
        #subpcriber and publisher
        self.pub_event = rospy.Publisher('/events/bus', NeuroEvent, queue_size=1)
        self.pub_cmd = rospy.Publisher(self.pub_topic, Twist, queue_size=1)

        self.sub = rospy.Subscriber(self.sub_topic, NeuroOutput, self.on_receive_data)

        rospy.loginfo('Neuro controller up')

    def on_receive_data(self, msg: NeuroOutput):
        pp = msg.softpredict.data

        cmd = Twist()

        if pp[0]>=self.th[0]: #dx
            if self.reset_flag==1:
                self.reset_integrator()
            
            time_start = rospy.get_time()
            while rospy.get_time()-time_start<=self.time_of_command:
                cmd.angular.z = 0.5
                self.pub_cmd.publish(cmd)
            
        elif pp[1]>=self.th[1]: #rest
            if self.reset_flag==1:
                self.reset_integrator()

            time_start = rospy.get_time()
            while rospy.get_time()-time_start<=self.time_of_command:
                cmd.linear.x = 0.5
                self.pub_cmd.publish(cmd)
            
        elif pp[2]>=self.th[2]: #rest
            if self.reset_flag==1:
                self.reset_integrator()

            time_start = rospy.get_time()
            while rospy.get_time()-time_start<=self.time_of_command:
                cmd.angular.z = -0.5
                self.pub_cmd.publish(cmd)
            
        else:
            cmd.linear.x = 0.0
            cmd.angular.z = 0.0
            self.pub_cmd.publish(cmd)
    
    def reset_integrator(self):
        msg = NeuroEvent()
        msg.event = 781 #reset event for the integrator
        self.pub_event.publish(msg)
    
    def run(self):
        rospy.spin()

if __name__ == '__main__':

    node = neuro_controller_node()
    node.run()
        







