#!/usr/bin/env roseus
(require "models/arrow-object.l")
(load "package://robot_assembler/euslisp/assembled-robot-interface.l")
(assembled-robot-init)
(setq *robot* (instance tmp2_robot-robot :init))
(objects (list *robot*))


(ros::load-ros-manifest "jsk_recognition_msgs")
(defvar *topic-name* "/depth_cam/boxes")

;;ros::init
(ros::roseus "boundingboxarray_subscriber")

(defun bounding-box-array-cb (msg)
  ;; boxesは、BoundingBoxのArray(Euslispではlist)
    (setq *bounding-box-list* (send msg :boxes)) 
    (when *bounding-box-list*
      (let* ((b (elt *bounding-box-list* 0))
             (cam->obj-coords (ros::tf-pose->coords (send b :pose)))
	     (cam-coords (send (send *robot* :head_depth) :copy-worldcoords)))
	;; camera -> optical frame
	(send cam-coords :rotate pi/2 :y)
	(send cam-coords :rotate -pi/2 :z)
        (setq *obj-pos* (send (send cam-coords :transform cam->obj-coords) :worldpos))
        (setq *found-obj* t))))

(ros::subscribe *topic-name* jsk_recognition_msgs::BoundingBoxArray #'bounding-box-array-cb 1)

(setq *found-obj* nil)
(setq *obj-pos* nil)
(setq *target-coords* nil)

(until *found-obj*
  (x::window-main-one) ;; IRT viewerの視点を変えられる。見にくければ変えよう
  (ros::spin-once)
  (ros::sleep))

(when (and *found-obj* *obj-pos*)
  (setq *target-coords* (make-coords :pos *obj-pos*  :rpy #f(0 1.54 1.54)))
  (send *robot* :rarm :inverse-kinematics *target-coords* :rotation-axis nil)
  (objects (list *robot* *target-coords*)))
(send *ri* :angle-vector (send *robot* :angle-vector))
(send *ri* :wait-interpolation)


