#!/usr/bin/env roseus
;; display-bounding-box-array.l
;; Based on display-bounding-box-array.l in jsk-enshu/robot-programming/dxl_armed_turtlebot/euslisp

(load "package://robot_assembler/outputs/0810_robot.l")
(setq *robot* (instance tmp2_robot-robot :init))

(ros::load-ros-manifest "jsk_recognition_msgs")

(defvar *topic-name* "/depth_cam/boxes")

;;ros::init
(ros::roseus "boundingboxarray_subscriber")

;;callback function
(defun bounding-box-array-cb (msg)
  ;; boxesは、BoundingBoxのArray(Euslispではlist)
  (let ((bounding-box-list (send msg :boxes)))
    ;; BoundingBoxがあれば表示する
    (print bounding-box-list)
    (when bounding-box-list 
      ;;(print msg) 
      (send *irtviewer* :draw-objects :flush nil)
      (mapcar #'(lambda (b)
                  ;; BoundingBoxは、dimensions(直方体の幅・奥行き・高さ)をもつ
                  (let* ((dims (ros::tf-point->pos (send b :dimensions)))
                         (bx (make-cube (elt dims 0) (elt dims 1) (elt dims 2)))
                         ;; (1) BoundingBoxのカメラ相対の座標系は、geometry_msgs/Poseという型で得られるので、Euslispのcoordsに変換する
                         (cam->obj-coords (ros::tf-pose->coords (send b :pose)))
                         ;; (2) *robot*モデルがカメラの座標系をもってるので、取得する
                         ;;(cam-coords (send (send *robot* :head_depth :head_depth-sensor-coords) :copy-worldcoords)))
                         (cam-coords (send (send tmp2_robot-robot :head_depth-sensor-coords) :copy-worldcoords)))
		    ;; (3) Euslisp内部でのworld座標系の値にして、そこにmake-cubeの箱を設置する
                    (send bx :newcoords (send cam-coords :transform cam->obj-coords))
                    (send bx :worldcoords)
                    (send bx :draw-on :flush nil :color #f(1 0 0)) ;; 描画
                    bx))
              bounding-box-list)
      (send *irtviewer* :viewer :viewsurface :flush)
      )
    ))

(make-irtviewer)
(ros::subscribe *topic-name* jsk_recognition_msgs::BoundingBoxArray #'bounding-box-array-cb 1)

(do-until-key
 (x::window-main-one) ;; IRT viewerの視点を変えられる。見にくければ変えよう
 (ros::spin-once)
 (ros::sleep)
 )
