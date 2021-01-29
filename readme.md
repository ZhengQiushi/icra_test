# ICRA for sp2021

## 1 . How to use

### Simulation

```bash
# open the rviz
roslaunch roborts_stage.launch
# enable the navigation 
rosrun roborts_decision behavior_test_node
# choose the goal behavior
# click the 2d nav position in the rviz tab 

```

### Mapping

```bash
# open the mapping function
roslaunch roborts_bringup mapping.launch
# drive around to complete the map
python teleop.py
# save the map
rosrun map_server map_saver -f your_map_name
```

### Navigation

```bash
# open the rviz. Remember to change the args for map!!!
roslaunch roborts_bringup navigation.launch
# click the 2d pos estimate in the rviz tab to relocate the postion of the car
# enable the navigation 
rosrun roborts_decision behavior_test_node
# choose the goal behavior
# click the 2d nav position in the rviz tab 

```

## 2. TODO

当前进度：

只是学会如何调用基本的导航功能，但是还需要学习C板的使用，该套程序并不适用于我们自己的车。

其他任务：

1. 添加自瞄模块
2. 添加裁判系统的通讯模块