#!/usr/bin/env python

import rospy
import re
from std_msgs.msg import String
from std_msgs.msg import Empty
from geometry_msgs.msg import Twist
import time

actionBusy = False

# @author: Simon Yacoub and Devon Daley


# Decode and execute the action
def decodeAction(data, args):
    actionMessage = Twist() #the mess

    # Get the parameters
    action = str(data.data)
    (drivePublisher, dockPublisher, undockPublisher) = args
    rospy.loginfo("Action: " + action)
    
    #handle basic movement commands from actions topic
    if(action == "forward"):
        actionMessage = getTwistMesg("forward")
    elif(action == "backward"):
        actionMessage = getTwistMesg("backward")
    elif(action == "left"): #Does a 45 degree turn left (stops robot first)
        actionMessage = getTwistMesg("left")
        tmp = String()
        tmp.data = "stop"
        decodeAction(tmp, args)
        drivePublisher.publish(actionMessage)
    elif(action == "right"): #Does 45 degree turn right (stops robot first)
        actionMessage = getTwistMesg("right")
        tmp = String()
        tmp.data = "stop"
        decodeAction(tmp, args)
        drivePublisher.publish(actionMessage)
    elif(action == "sright"): #small r + fwd motion for wall following
        actionMessage = getTwistMesg("sright")
        drivePublisher.publish(actionMessage)
    elif(action == "sleft"): #small l + fwd motion for wall following
        actionMessage = getTwistMesg("sleft")
        drivePublisher.publish(actionMessage)
    elif(action == "bleft"):    # big left motion to make space from wall
        actionMessage = getTwistMesg("bleft")
        drivePublisher.publish(actionMessage)
    elif(action == "stop"): #stops the robot
        actionMessage = getTwistMesg("stop")
    else:
        actionMessage = getTwistMesg("idle")

    #publish action
    drivePublisher.publish(actionMessage)

    # Handle the docking station cases
    if action == "dock":
        dockPublisher.publish()
        
        
'''
Get a Twist message which consists of a linear and angular component which can be negative or positive.

linear.x  (+)     Move forward (m/s)
          (-)     Move backward (m/s)

angular.z (+)     Rotate counter-clockwise (rad/s)
         (-)     Rotate clockwise (rad/s)

Limits:
-0.5 <= linear.x <= 0.5 and -4.25 <= angular.z <= 4.25 (4rads = 45deg)
'''
def getTwistMesg(action):
    message = Twist()
    
    if action == "forward":
        message.linear.x = 0.25
        message.angular.z = 0
    elif action == "backward":
        message.linear.x = -0.25
        message.linear.z = 0
    elif action == "left":
        message.linear.x = 0
        message.angular.z = 4
    elif action == "right":
        message.linear.x = 0
        message.angular.z = -4
    elif action == "sleft":
        message.linear.x = 0.1
        message.angular.z = 0.25
    elif action == "sright":
        message.linear.x = 0.1
        message.angular.z = -0.25
    elif action == "bleft":
        message.linear.x = -0.1
        message.angular.z = 0.5
    elif action == "stop":
        message.linear.x = 0
        message.angular.z = 0
    
    return message

# Main execution
def rosMain():
    drivePublisher = rospy.Publisher('cmd_vel', Twist, queue_size=2)
    dockPublisher = rospy.Publisher('dock', Empty, queue_size=1)
    undockPublisher = rospy.Publisher('undock', Empty, queue_size=1)
    #perceptionsPublisher = rospy.Publisher('perceptions', String, queue_size=10)
    rospy.init_node('actionTranslator', anonymous=True)
    rospy.Subscriber('actions', String, decodeAction, (drivePublisher, dockPublisher, undockPublisher))
    
    #publishTurn(perceptionsPublisher)
    rospy.spin()

# Start things up
if __name__ == '__main__':
    try:
        rosMain()
    except rospy.ROSInterruptException:
        pass
