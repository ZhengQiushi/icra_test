#!/usr/bin/env python
# -*- coding: utf-8 -*-
import rospy
from roborts_msgs.msg import GimbalAngle
from roborts_msgs.srv import FricWhl,ShootCmd
import sys, select, termios, tty
import threading
import time

pub = rospy.Publisher('/cmd_gimbal_angle',GimbalAngle,queue_size=5)
current_yaw = 0.0
current_pitch = 0.0
FricWhlState = False    #摩擦轮状态
useKey = ['w','a','s','d','r','f','p']
"""
GIMBAL CONTROL TEST
W/S     pitch up/down
A/D      yaw up/down
"""

def getKey():
    tty.setraw(sys.stdin.fileno())
    rlist, _, _ = select.select([sys.stdin], [], [], 0.1)
    if rlist:
        key = sys.stdin.read(1)
    else:
        key = ''
    # print "key:",key
    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
    return key

def publish_angle(yaw,pitch):
    msg = GimbalAngle()
    msg.yaw_mode = False
    msg.pitch_mode = False
    msg.yaw_angle = yaw
    msg.pitch_angle = pitch
    pub.publish(msg)

def base_main():
    global current_yaw,current_pitch
    while True:
        publish_angle(current_yaw, current_pitch)
        time.sleep(0.025)

def FricWhlChange():
    global FricWhlState
    FricWhlState = not FricWhlState
    rospy.wait_for_service("cmd_fric_wheel")
    try:
        FricSrv = rospy.ServiceProxy('cmd_fric_wheel',FricWhl)
        res = FricSrv(FricWhlState)
    except rospy.ServiceException,e:
        print "Service call failed:%s"%e

def ShootOnce():
    rospy.wait_for_service("cmd_shoot")
    try:
        ShootSrv = rospy.ServiceProxy('cmd_shoot',ShootCmd)
        res = ShootSrv(1,2)
        print(res)
    except rospy.ServiceException,e:
        print "Service call failed:%s"%e        

if __name__ == "__main__":
    settings = termios.tcgetattr(sys.stdin)
    rospy.init_node('gimbal_test')
    base = threading.Thread(target=base_main)
    base.setDaemon(True)
    base.start()
    scale = 0.03
    # global current_yaw,current_pitch
    try:
        while not rospy.is_shutdown():
            key = getKey()
            print "yaw:"+str(current_yaw)+"   pitch:"+str(current_pitch)
            if key == "w":
                current_pitch += scale
            elif key == "s":
                current_pitch -= scale
            elif key == "a":
                current_yaw -= scale
            elif key == "d":
                current_yaw += scale
            elif key == "p":
                current_pitch = 0
                current_yaw = 0
            elif key == "r":
                ShootOnce()
            elif key == "f":
                FricWhlChange()
            elif key == "q":
                break

            current_yaw = min(current_yaw,1.57/2)
            current_yaw = max(current_yaw,-1.57/2)
            current_pitch = min(current_pitch,1.57/2)
            current_pitch = max(current_pitch,-1.57/2)
            time.sleep(0.02)
    except Exception as e:
        print e
        
        
    finally:
        current_yaw = 0
        current_pitch = 0

    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)



