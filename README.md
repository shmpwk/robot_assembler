# robot-assembler
assemble robot using GUI

## Document
https://github.com/agent-system/robot_assembler/blob/master/doc/Robot_Assembler%E8%AA%AC%E6%98%8E.pdf


**************************
editor : shumpei wakabayashi 

## How to run

### Move arm when range sensor finds a object. 

Launch FIXED_ARM_1 sample on gazebo.
```
source ~/YOUR_WORK_SPACE/devel/setup.bash
roslaunch robot_assembler robot_assembler_gazebo.launch model:=$(rospack find robot_assembler)/sample/FIXED_ARM_1.urdf use_xacro:=true paused:=true
```

Move arm when a range sensor finds a object.
```
roscd robot_assembler
python gazebo/range_fixedarm.py 
```

### tips
`roobt_0617_dynamics.urdf` : add damping and friction 
`robot_0617_mass100.urdf` : multiplied mass by 100