#!/usr/bin/env python
# -*- coding: utf-8 -*-
import rospy
import actionlib
from control_msgs.msg import FollowJointTrajectoryAction, FollowJointTrajectoryGoal
from trajectory_msgs.msg import JointTrajectoryPoint

rospy.init_node('send_motion')
act_client = actionlib.SimpleActionClient('/fullbody_controller/follow_joint_trajectory', FollowJointTrajectoryAction)

act_client.wait_for_server()

# gen msg
traj_msg = FollowJointTrajectoryGoal()
traj_msg.trajectory.header.stamp = rospy.Time.now() + rospy.Duration(0.2)
traj_msg.trajectory.joint_names = ['JOINT0', 'JOINT1', 'JOINT2', 'JOINT3', 'JOINT4', 'JOINT5']

##

traj_msg.trajectory.points.append(JointTrajectoryPoint(positions=[0.1, -0.5, 2.0, -0.1, 0.5, -2.0], #姿勢1 構え
                                                       time_from_start = rospy.Duration(2))) ## 前の姿勢から2sec
traj_msg.trajectory.points.append(JointTrajectoryPoint(positions=[0.1, 0.2, 1.4, -0.1, -0.2, -1.4], #姿勢2　はさみに行く
                                                       time_from_start = rospy.Duration(6)))## 前の姿勢から4sec
traj_msg.trajectory.points.append(JointTrajectoryPoint(positions=[0.1, 0.22, 1.4, -0.1, -0.22, -1.4], #姿勢2.5　挟む
                                                       time_from_start = rospy.Duration(10)))## 前の姿勢から4sec
traj_msg.trajectory.points.append(JointTrajectoryPoint(positions=[1.0, 0.22, 1.4, -1.0, -0.22, -1.4], #姿勢3　持ち上げる
                                                       time_from_start = rospy.Duration(14)))## 前の姿勢から4sec
traj_msg.trajectory.points.append(JointTrajectoryPoint(positions=[0.1, 0.22, 1.4, -0.1, -0.22, -1.4], #姿勢2.5　下げる
                                                       time_from_start = rospy.Duration(18)))## 前の姿勢から4sec
traj_msg.trajectory.points.append(JointTrajectoryPoint(positions=[0.1, -0.5, 2.0, -0.1, 0.5, -2.0], #姿勢4　構えに戻る
                                                       time_from_start = rospy.Duration(22)))## 前の姿勢から4sec

#traj_msg.trajectory.points.append(JointTrajectoryPoint(positions=[1], time_from_start = rospy.Duration(2)))

# send to robot arm
act_client.send_goal(traj_msg)

act_client.wait_for_result()

rospy.loginfo("done")
