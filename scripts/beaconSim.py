#!/usr/bin/env python

# @author: Devon Daley

# SUBSCRIBER:   NONE
# PUBLISHER:    String object to 'perceptions' node.

import rospy
from std_msgs.msg import String
import time
from pathFinder import *

# Simple test tool that allows you to transmit fake beacon location updates. You start by typing out the full path, then it steps through said path as you press enter.

# Main program
def rosMain():
        # Init the node and setup publisher
        rospy.init_node('RobotTester', anonymous=True)
        perceptionsPublisher = rospy.Publisher('perceptions', String, queue_size=10)
        
        while not rospy.is_shutdown():
            inp = raw_input("Type a series of node letters with spaces between (eg 'A B C'): ")
            inp = inp.split()
            
            for node in inp:
                raw_input("Press enter when @ node " + node)   
                out = 'node: ' + node + ' 0.3'  # Prepare message saying we are 0.3 m away from beacon
                perceptionsPublisher.publish(out)
        
        
if __name__ == '__main__':
    try:
        rosMain()
    except rospy.ROSInterruptException:
        pass
