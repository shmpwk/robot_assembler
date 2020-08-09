#!/usr/bin/env roseus
;; grasp.l
;; Based on gazebo-grasp-with-recognition.l in jsk-enshu/robot-programming/dxl_armed_turtlebot/euslisp

(load "package://robot_assembler/outputs/0810_robot.l")
(setq *robot* (instance tmp2_robot-robot :init))

(ros::load-ros-manifest "jsk_recognition_msgs")

(defvar *topic-name* "/depth_cam/boxes")
(defvar *bounding-box-list* nil)

(setq found-obj nil)
(setq obj-pos #f(0 0 0))

;;ros::init
(ros::roseus "boundingboxarray_subscriber")

;;callback function
(defun bounding-box-array-cb (msg)
  (setq *bouinding-box-list* (send msg :boxes)) ;boxesは、BoundingBoxのArray(Euslispではlist)
  (when *bounding-box-list*
    (let* ((b (elt *bounding-box-list* 0))
           (cam->obj-coords (ros::tf-pose->coords (send b :pose)))
           (cam-coords (send (send *robot* :head_depth-sensor-coords) :copy-worldcoords)))
      (setq obj-pos (scale 0.001 (send (send cam-coords :transform cam->obj-coords) :worldpos)))
      (setq found-obj t)
      obj-pos))
  )



