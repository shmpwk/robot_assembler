#!/usr/bin/env python
# -*- coding: utf-8 -*-

import rospy
import actionlib
import math
from trajectory_msgs.msg import JointTrajectory
from trajectory_msgs.msg import JointTrajectoryPoint
from control_msgs.msg import FollowJointTrajectoryAction, FollowJointTrajectoryGoal

def open():
# トピック名,メッセージ型を使って ActionLib client を定義
    client = actionlib.SimpleActionClient('/fullbody_controller/follow_joint_trajectory', FollowJointTrajectoryAction)
    client.wait_for_server() # ActionLib のサーバと通信が接続されることを確認
    # gen msg
    traj_msg = FollowJointTrajectoryGoal()
    traj_msg.trajectory = JointTrajectory()
    traj_msg.trajectory.header.stamp = rospy.Time.now() + rospy.Duration(0.2)
    traj_msg.trajectory.joint_names = ['JOINT0', 'JOINT1', 'JOINT2', 'JOINT3', 'JOINT4', 'JOINT5', 'JOINT6', 'JOINT7', 'JOINT8', 'JOINT9', 'JOINT10', 'JOINT11', 'JOINT12', 'JOINT13', 'JOINT14', 'JOINT15', 'JOINT16', 'JOINT18', 'JOINT20', 'JOINT22', 'JOINT23', 'JOINT25', 'JOINT27',  'JOINT29']
    traj_msg.trajectory.points.append(JointTrajectoryPoint(positions=[0, 1, 0, 1.5, 1, 0, 0, -1.5, 0, -1.0, 0, -1.5, -1, 0, 0, 0, 0, -0.2, 0, 0, 0, 0.2, 0], time_from_start = rospy.Duration(2.0)))
    client.send_goal(traj_msg)
    rospy.loginfo("wait for open hand ...")
    client.wait_for_result() #ロボットの動作が終わるまで待つ
    rospy.loginfo("done")

if __name__ == '__main__':
    rospy.init_node('open_hand_ctl', anonymous=True)
    open()
