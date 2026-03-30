# ros2-fishbot-description

一个基于 **ROS 2 Humble** 的 FishBot 学习与实践工作区，覆盖了从 **URDF / Xacro 机器人描述建模**、**Gazebo 仿真**、**ros2_control 差速控制**，到 **Nav2 导航** 与 **自动巡逻应用** 的完整基础链路。

这个仓库最初从 `fishbot_description` 起步，现在已经扩展为一个包含多个 ROS 2 包的工作区，适合作为移动机器人方向的入门项目，也可以作为后续继续学习 **SLAM、Nav2、路径规划、自动巡逻、多传感器融合** 的实验基础。

---

## 项目概览

当前工作区包含以下几个核心包：

| Package | 作用 |
|---|---|
| `fishbot_description` | FishBot 机器人模型描述、RViz 显示、Gazebo 场景与 `ros2_control` 配置 |
| `fishbot_navigation2` | Nav2 启动文件、地图与导航参数 |
| `fishbot_application` | 基于 `nav2_simple_commander` 的应用示例，如设置初始位姿、单点导航、航点跟随、获取机器人位姿 |
| `autopatrol_robot` | 基于参数配置的自动巡逻节点 |

---

## 功能特性

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
- Nav2 导航基础集成
- 单目标导航与航点跟随示例
- 基于参数文件的自动巡逻节点

---

## 目录结构

```text
ros2-fishbot-description/
├── README.md
├── src/
│   ├── fishbot_description/
│   │   ├── config/
│   │   ├── launch/
│   │   ├── urdf/
│   │   └── world/
│   ├── fishbot_navigation2/
│   │   ├── config/
│   │   ├── launch/
│   │   └── maps/
│   ├── fishbot_application/
│   │   └── fishbot_application/
│   └── autopatrol_robot/
│       ├── autopatrol_robot/
│       └── config/
└── .gitignore
```

---

## 推荐环境

- Ubuntu 22.04
- ROS 2 Humble
- colcon
- xacro
- rviz2
- Gazebo Classic + `gazebo_ros`
- `gazebo_ros2_control`
- `ros2_controllers`
- Navigation2
- `nav2_simple_commander`
- `tf_transformations`

---

## 依赖安装

如果你使用的是 ROS 2 Humble 桌面版环境，仍建议补充以下依赖：

```bash
sudo apt update
sudo apt install \
  ros-humble-gazebo-ros-pkgs \
  ros-humble-gazebo-ros2-control \
  ros-humble-ros2-controllers \
  ros-humble-navigation2 \
  ros-humble-nav2-bringup \
  ros-humble-nav2-simple-commander \
  ros-humble-tf-transformations \
  ros-humble-xacro
```

---

## 构建

在工作区根目录执行：

```bash
colcon build
source install/setup.bash
```

---

## 快速开始

### 1. 在 RViz 中显示默认模型

```bash
ros2 launch fishbot_description display_robot.launch.py
```

### 2. 在 RViz 中显示模块化 FishBot 模型

```bash
ros2 launch fishbot_description display_robot.launch.py \
  model:=$(ros2 pkg prefix fishbot_description)/share/fishbot_description/urdf/fishbot/fishbot.urdf.xacro
```

### 3. 启动 Gazebo 仿真

```bash
ros2 launch fishbot_description gazebo_sim.launch.py
```

该启动文件会自动完成以下流程：

- 通过 `xacro` 生成 `robot_description`
- 启动 Gazebo 世界
- 将 FishBot 实体生成到仿真环境中
- 加载 `fishbot_joint_state_broadcaster`
- 加载 `fishbot_diff_drive_controller`

### 4. 控制机器人移动

Gazebo 仿真启动后，可以向 `/cmd_vel` 发布速度指令：

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

## Nav2 导航

### 1. 启动导航栈

确保 Gazebo 仿真已经运行，然后在新的终端执行：

```bash
source install/setup.bash
ros2 launch fishbot_navigation2 navigation2.launch.py
```

该启动文件默认会：

- 使用仿真时间 `use_sim_time=true`
- 加载 `maps/room.yaml`
- 加载 `config/nav2_params.yaml`
- 启动 Nav2 bringup 和 RViz

### 2. 设置机器人初始位姿

```bash
source install/setup.bash
ros2 run fishbot_application init_robot_pose
```

### 3. 单目标点导航

```bash
source install/setup.bash
ros2 run fishbot_application nav_to_pose
```

默认示例目标点为：

- `x = 2.0`
- `y = 1.0`

### 4. 航点跟随

```bash
source install/setup.bash
ros2 run fishbot_application waypoint_follower
```

该示例会依次下发多个 `PoseStamped` 航点，用于验证基础巡航能力。

### 5. 获取当前机器人位姿

```bash
source install/setup.bash
ros2 run fishbot_application get_robot_pose
```

该节点会通过 TF 查询 `map -> base_footprint` 变换，并输出当前位姿信息。

---

## 导航调试与问题总结

项目初期，局部路径跟随器使用的是 **DWB**。但在室内导航过程中，机器人在靠近墙边行驶时经常会出现卡住的问题。为了解决这个现象，我花了较长时间反复调试相关参数，但始终无法稳定修复。

后来我将局部控制器从 **DWB** 更换为 **RPP（Regulated Pure Pursuit）**。切换之后，这个靠墙卡住的问题得到了明显改善，机器人的路径跟随表现也更加平滑、稳定，更适合室内导航与巡逻场景。

这次调整也说明了一个比较重要的实践经验：相比于反复调节一个不太适合当前场景的控制器参数，直接选择更合适的局部控制器，往往会更有效。

---

## 自动巡逻

`autopatrol_robot` 提供了一个基于参数文件的自动巡逻节点。

### 1. 启动自动巡逻

```bash
source install/setup.bash
ros2 run autopatrol_robot patrol_node \
  --ros-args \
  --params-file $(ros2 pkg prefix autopatrol_robot)/share/autopatrol_robot/config/patrol_config.yaml
```

### 2. 巡逻参数说明

`patrol_config.yaml` 中包含：

- `initial_point`：机器人初始位姿 `[x, y, yaw]`
- `patrol_points`：巡逻点序列，按 `[x1, y1, yaw1, x2, y2, yaw2, ...]` 组织

你可以根据自己的地图修改巡逻路线。

---

## fishbot_description 包说明

`fishbot_description` 是当前工作区的基础包，核心内容包括：

### 1. 基础建模练习

保留了基础 URDF / Xacro 学习文件：

- `urdf/first_robot.urdf`
- `urdf/first_robot.xacro`

### 2. 模块化整机装配

`urdf/fishbot/fishbot.urdf.xacro` 作为整机装配入口，统一组合：

- base
- sensors
- actuators
- Gazebo plugins
- ros2_control

### 3. 已集成传感器

- Camera
- IMU
- Laser

### 4. 已集成执行器

- left / right wheel
- caster wheels

### 5. 控制链路

通过以下文件完成控制链路接入：

- `urdf/fishbot/fishbot.ros2_control.xacro`
- `config/fishbot_ros2_controller.yaml`
- `launch/gazebo_sim.launch.py`

当前已配置：

- `fishbot_joint_state_broadcaster`
- `fishbot_diff_drive_controller`
- `fishbot_effort_controller`（已预留）

---

## 当前阶段

当前仓库已经从单纯的“机器人描述学习项目”演进为一个具备以下能力的 FishBot ROS 2 工作区：

- 机器人模型描述
- Gazebo 仿真
- ros2_control 差速底盘控制
- Nav2 导航基础运行
- Python 应用层导航调用
- 参数化自动巡逻

这意味着它已经可以作为下一阶段继续扩展的基础平台。

---

## 后续可扩展方向

- 接入 SLAM Toolbox
- 完善地图构建与保存流程
- 增加键盘遥控节点
- 增加更复杂的 Gazebo 场景和障碍物
- 补充项目截图、录屏和动图
- 引入行为树任务编排
- 补充更多应用层导航示例
- 进一步完善包级元数据与文档说明

---

## License

Apache-2.0
