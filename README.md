# ros2-fishbot-description

一个基于 **ROS 2 Humble** 的 FishBot 学习项目，围绕 **URDF/Xacro 机器人描述建模、模块化结构组织、Gazebo 仿真、传感器集成，以及 ros2_control 差速控制** 展开。

这个仓库记录了我从基础 URDF/Xacro 入门，到构建一个可在 Gazebo 中运行、可通过 `/cmd_vel` 控制的二轮差速机器人模型的学习过程。它既适合作为机器人描述入门项目，也适合作为后续学习导航、SLAM、控制与系统集成的基础。

---

## Features

- 基础 URDF / Xacro 建模练习
- 模块化 FishBot 机器人描述结构
- 传感器模块化集成
  - Camera
  - IMU
  - Laser
- Gazebo 仿真支持
- `ros2_control` 接入
- `joint_state_broadcaster` 状态发布
- `diff_drive_controller` 差速控制
- RViz 模型显示
- 自定义 world 场景资源

---

## Repository Structure

```text
ros2-fishbot-description/
├── README.md
├── .gitignore
└── src/
    └── fishbot_description/
        ├── CMakeLists.txt
        ├── package.xml
        ├── LICENSE
        ├── config/
        │   ├── display_robot_model.rviz
        │   └── fishbot_ros2_controller.yaml
        ├── launch/
        │   ├── display_robot.launch.py
        │   └── gazebo_sim.launch.py
        ├── urdf/
        │   ├── first_robot.urdf
        │   ├── first_robot.xacro
        │   └── fishbot/
        │       ├── base.urdf.xacro
        │       ├── common_inertial.xacro
        │       ├── fishbot.urdf.xacro
        │       ├── fishbot.ros2_control.xacro
        │       ├── actuator/
        │       │   ├── wheel.urdf.xacro
        │       │   └── caster.urdf.xacro
        │       ├── sensor/
        │       │   ├── camera.urdf.xacro
        │       │   ├── imu.urdf.xacro
        │       │   └── laser.urdf.xacro
        │       └── plugins/
        │           ├── gazebo_control_plugin.xacro
        │           └── gazebo_sensor_plugin.xacro
        └── world/
            ├── custom_room.world
            └── room/
```

---

## Environment

推荐环境：

- Ubuntu 22.04
- ROS 2 Humble
- colcon
- xacro
- rviz2
- Gazebo + gazebo_ros
- gazebo_ros2_control
- ros2_controllers

如果缺少仿真与控制相关依赖，可以参考：

```bash
sudo apt update
sudo apt install \
  ros-humble-gazebo-ros-pkgs \
  ros-humble-gazebo-ros2-control \
  ros-humble-ros2-controllers \
  ros-humble-xacro
```

---

## Build

在工作区根目录执行：

```bash
colcon build
source install/setup.bash
```

---

## Quick Start

### 1. 在 RViz 中显示默认模型

```bash
ros2 launch fishbot_description display_robot.launch.py
```

### 2. 在 RViz 中显示模块化 FishBot

```bash
ros2 launch fishbot_description display_robot.launch.py \
  model:=$PWD/src/fishbot_description/urdf/fishbot/fishbot.urdf.xacro
```

### 3. 启动 Gazebo 仿真

```bash
ros2 launch fishbot_description gazebo_sim.launch.py
```

该 launch 会完成以下流程：

- 通过 `xacro` 生成 `robot_description`
- 启动 Gazebo 场景
- 将 FishBot 实体生成到仿真环境中
- 加载 `fishbot_joint_state_broadcaster`
- 加载 `fishbot_diff_drive_controller`

---

## Control the Robot

仿真启动成功后，可以向 `/cmd_vel` 发布速度指令控制机器人：

```bash
ros2 topic pub /cmd_vel geometry_msgs/msg/Twist \
  "{linear: {x: 0.2}, angular: {z: 0.0}}" -r 10
```

原地旋转示例：

```bash
ros2 topic pub /cmd_vel geometry_msgs/msg/Twist \
  "{linear: {x: 0.0}, angular: {z: 0.5}}" -r 10
```

查看控制器状态：

```bash
ros2 control list_controllers
```

---

## What This Project Covers

### 1. Basic URDF / Xacro Practice

保留了基础单文件练习内容：

- `urdf/first_robot.urdf`
- `urdf/first_robot.xacro`

适合练习：

- link / joint 组织方式
- 几何体与材质
- 惯性参数
- Xacro 参数化与宏

### 2. Modular FishBot Description

`urdf/fishbot/fishbot.urdf.xacro` 作为整机装配入口，统一组合：

- base
- sensors
- actuators
- Gazebo plugins
- ros2_control

### 3. Sensors

已集成的传感器模块：

- Camera
- IMU
- Laser

适合继续扩展传感器挂载、位姿调整和仿真输出。

### 4. Actuators

当前底盘执行器模块包括：

- left / right wheel
- caster wheels

### 5. ros2_control Integration

通过以下文件完成控制链路：

- `urdf/fishbot/fishbot.ros2_control.xacro`
- `config/fishbot_ros2_controller.yaml`
- `launch/gazebo_sim.launch.py`

当前已配置：

- `fishbot_joint_state_broadcaster`
- `fishbot_diff_drive_controller`
- `fishbot_effort_controller`（已预留）

---

## Milestone

当前项目已经从 **“机器人描述学习项目”** 演进为 **“具备 Gazebo 仿真 + ros2_control 差速控制能力的 FishBot 基础平台”**。

相较于早期版本，现在已经具备：

- 更完整的模块化组织
- Gazebo 场景启动能力
- 传感器仿真基础
- 控制器加载流程
- 差速底盘控制闭环入口

这也意味着项目已经可以作为下一阶段内容的基础：

- SLAM
- Nav2
- 路径规划
- 巡航 / 避障
- 多传感器融合

---

## Suggested Next Steps

后续可以继续扩展：

- 添加里程计与 TF 验证
- 接入 Nav2
- 接入 SLAM Toolbox
- 补充键盘控制节点
- 增加更完整的 Gazebo 场景和障碍物
- 补充项目截图 / 动图 / 仿真录屏

---

## License

Apache-2.0
