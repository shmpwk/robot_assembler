#!/usr/bin/env python
# -*- coding: utf-8 -*-

import rospy
import actionlib
import math
from trajectory_msgs.msg import JointTrajectory
from trajectory_msgs.msg import JointTrajectoryPoint
from control_msgs.msg import FollowJointTrajectoryAction, FollowJointTrajectoryGoal
from sensor_msgs.msg import LaserScan

i = 0

def callback(msg):
    ## see descripton
    ## http://docs.ros.org/melodic/api/sensor_msgs/html/msg/LaserScan.html
    rospy.loginfo('min %f -(%f)-> max %f'%(msg.angle_min, msg.angle_increment, msg.angle_max))
    #msg.range_min
    #msg.range_max
    #msg.ranges
    
    # トピック名,メッセージ型を使って ActionLib client を定義
    client = actionlib.SimpleActionClient('/fullbody_controller/follow_joint_trajectory', FollowJointTrajectoryAction)
    client.wait_for_server() # ActionLib のサーバと通信が接続されることを確認
    # gen msg
    traj_msg = FollowJointTrajectoryGoal()
    traj_msg.trajectory = JointTrajectory()
    traj_msg.trajectory.header.stamp = rospy.Time.now() + rospy.Duration(0.2)
    traj_msg.trajectory.joint_names = ['JOINT0', 'JOINT1', 'JOINT2', 'JOINT3', 'JOINT4', 'JOINT5', 'JOINT6', 'JOINT7']

    global i
    val = int(-msg.angle_min / msg.angle_increment)
    if (msg.ranges[val] < 100):
        i += 1
        traj_msg.trajectory.points.append(JointTrajectoryPoint(positions=[0, 0, 0, 0, 0, i, 0], time_from_start = rospy.Duration(1.0 + i)))
        #目標姿勢をゴールとして送信
        client.send_goal(traj_msg)
        rospy.loginfo("wait for goal ...")
        client.wait_for_result() #ロボットの動作が終わるまで待つ
        rospy.loginfo("done")


if __name__ == '__main__':
    rospy.init_node('range_listener', anonymous=True)
    rospy.Subscriber("/range_sensor", LaserScan, callback)
    rospy.spin()
