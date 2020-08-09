#!/usr/bin/env python
# -*- coding: utf-8 -*-

import rospy
import actionlib
import math
from trajectory_msgs.msg import JointTrajectry
from trajectry_msgs.msg import JointTrajectoryPoint
from control_msgs.msg import JointTrajectory
from sensor_msgs.msg import LaserScan

i=0


def callback(msg):
    rospy.loginfo('min %f -(%f)-> max %f'%(msg.angle_min, msg.angle_increment, msg.angle_max))   
    # トピック名,メッセージ型を使って ActionLib client を定義
    client = actionlib.SimpleActionClient('/fullbody_controller/follow_joint_trajectory', FollowJointTrajectoryAction)
    client.wait_for_server() # ActionLib のサーバと通信が接続されることを確認
    # gen msg
    traj_msg = FollowJointTrajectoryGoal()
    traj_msg.trajectory = JointTrajectory()
    traj_msg.trajectory.header.stamp = rospy.Time.now() + rospy.Duration(0.2)
    traj_msg.trajectory.joint_names = ['JOINT0', 'JOINT1', 'JOINT2', 'JOINT3', 'JOINT4', 'JOINT5', 'JOINT6', 'JOINT7', 'JOINT8', 'JOINT9', 'JOINT10', 'JOINT11', 'JOINT12', 'JOINT13', 'JOINT14', 'JOINT15', 'JOINT16', 'JOINT17', 'JOINT18', 'JOINT19', 'JOINT20', 'JOINT21', 'JOINT22', 'JOINT23', 'JOINT24', 'JOINT25', 'JOINT26', 'JOINT27', 'JOINT28', 'JOINT29']

    global i 
    val = int(-msg.angle_min / msg.angle_increment)
    if (msg.ranges[val] < 100):
        i += 1
        traj_msg.trajectory.points.append(JointTrajectoryPoint(positions=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, i, 0, i, 0, 0, 0, 0, i, 0, i], time_from_start = rospy.Duration(1.0 + i)))
        #目標姿勢をゴールとして送信
        client.send_goal(traj_msg)
        rospy.loginfo("wait for goal ...")
        client.wait_for_result() #ロボットの動作が終わるまで待つ
        rospy.loginfo("done")


if __name__ == '__main__':
    rospy.init_node('range_listener', anonymous=True)
    rospy.Subscriber("/range_sensor", LaserScan, callback)
    rospy.spin()
