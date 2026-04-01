# ros2-fishbot

一个基于 **ROS 2 Humble** 的 FishBot 学习与实践工作区，覆盖了从 **URDF / Xacro 机器人描述建模**、**Gazebo 仿真**、**ros2_control 差速控制**，到 **Nav2 导航**、**应用层导航示例** 与 **自动巡逻应用** 的完整基础链路。

> 当前正式发布版本：**v2.0.0**

这个仓库最初从 `fishbot_description` 起步，现在已经扩展为一个包含多个 ROS 2 包的完整工作区，适合作为移动机器人方向的入门项目，也可以作为后续继续学习 **SLAM、Nav2、路径规划、自动巡逻、多传感器融合** 的实验基础。

---

## v2.0.0 版本亮点

- 完整整理项目文档，统一 README 结构与使用说明
- 统一各 ROS 2 包版本号到 `2.0.0`
- 清理多个 `package.xml` / `setup.py` 中的 `TODO` 占位描述
- 补齐关键运行依赖声明，便于 `rosdep` 与后续发布维护
- 明确导航、应用层控制、自动巡逻与自定义接口之间的关系
- 为 GitHub Release 准备独立发布说明与 About 文案

---

## 项目概览

当前工作区包含以下核心包：

| Package | 作用 |
|---|---|
| `fishbot_description` | FishBot 机器人模型描述、RViz 显示、Gazebo 场景与 `ros2_control` 配置 |
| `fishbot_navigation2` | Nav2 启动文件、地图、导航参数与 RViz 启动入口 |
| `fishbot_application` | 基于 `nav2_simple_commander` 的 Python 应用示例，如设置初始位姿、单点导航、航点跟随、获取机器人位姿 |
| `autopatrol_interfaces` | 自动巡逻相关的自定义服务接口，当前包含 `SpeechText.srv` |
| `autopatrol_robot` | 基于参数配置的自动巡逻节点，支持巡逻播报与图像记录 |

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
- 语音播报服务与巡逻图像采集流程

---

## 目录结构

```text
ros2-fishbot/
├── README.md
├── CHANGELOG.md
├── RELEASE_v2.0.0.md
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
│   ├── autopatrol_interfaces/
│   │   └── srv/
│   └── autopatrol_robot/
│       ├── autopatrol_robot/
│       ├── config/
│       └── launch/
└── .gitignore
```

---

## 推荐环境

- Ubuntu 22.04
- ROS 2 Humble
- `colcon`
- `rosdep`
- `xacro`
- `rviz2`
- Gazebo Classic + `gazebo_ros`
- `gazebo_ros2_control`
- `ros2_controllers`
- Navigation2
- `nav2_simple_commander`
- `tf_transformations`

自动巡逻相关功能额外会用到：

- `cv_bridge`
- OpenCV Python
- `espeakng` Python 语音播报模块

---

## 依赖安装

如果你使用的是 ROS 2 Humble 桌面版环境，建议先安装基础依赖：

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
  ros-humble-xacro \
  ros-humble-cv-bridge
```

如需使用自动巡逻中的图像保存与语音播报功能，还需要补充 OpenCV Python 与 `espeakng`。

如果系统已经正确配置 `rosdep`，也可以在工作区根目录执行：

```bash
rosdep install --from-paths src --ignore-src -r -y
```

---

## 构建

在工作区根目录执行：

```bash
colcon build --symlink-install
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

### 5. 获取当前机器人位姿

```bash
source install/setup.bash
ros2 run fishbot_application get_robot_pose
```

该节点会通过 TF 查询 `map -> base_footprint` 变换，并输出当前位姿信息。

---

## 导航调试记录

项目初期，局部路径跟随器使用的是 **DWB**。但在室内导航过程中，机器人在靠近墙边行驶时经常会出现卡住的问题。经过多轮参数调试后，当前版本改为使用 **RPP（Regulated Pure Pursuit）** 作为局部控制器，路径跟随表现更平滑，也更适合当前室内导航与巡逻场景。

这部分参数位于：

```text
src/fishbot_navigation2/config/nav2_params.yaml
```

---

## 自动巡逻

`autopatrol_robot` 提供了一个基于参数文件的自动巡逻节点，结合 `autopatrol_interfaces` 中的 `SpeechText.srv` 可以完成巡逻播报流程。

### 1. 启动导航环境

请先确保以下节点已经正常运行：

- Gazebo 仿真
- Nav2 导航
- 地图定位正常

### 2. 启动语音服务节点

```bash
source install/setup.bash
ros2 run autopatrol_robot speaker
```

### 3. 启动自动巡逻节点

```bash
source install/setup.bash
ros2 run autopatrol_robot patrol_node \
  --ros-args \
  --params-file $(ros2 pkg prefix autopatrol_robot)/share/autopatrol_robot/config/patrol_config.yaml
```

### 4. 巡逻参数说明

`patrol_config.yaml` 中当前包含：

- `initial_point`：机器人初始位姿 `[x, y, yaw]`
- `patrol_points`：巡逻点序列，按 `[x1, y1, yaw1, x2, y2, yaw2, ...]` 组织
- `use_sim_time`：是否使用仿真时间

如果你希望保存巡逻过程中的图像，可以继续在参数中补充 `img_save_path`。

---

## 包说明

### `fishbot_description`

基础包，负责：

- URDF / Xacro 机器人建模
- 传感器与执行器装配
- Gazebo 仿真入口
- `ros2_control` 控制链路接入

### `fishbot_navigation2`

导航包，负责：

- Nav2 启动入口
- 地图与导航参数管理
- RViz 启动配置
- RPP 控制器参数配置

### `fishbot_application`

应用层示例包，负责：

- 设置初始位姿
- 单点导航
- 航点跟随
- TF 获取机器人位姿

### `autopatrol_interfaces`

自定义接口包，当前包含：

- `SpeechText.srv`

### `autopatrol_robot`

自动巡逻包，负责：

- 读取巡逻点参数
- 调用 Nav2 巡逻导航
- 调用语音服务播报
- 记录巡逻过程图像

---

## 当前阶段

当前仓库已经从单纯的“机器人描述学习项目”演进为一个具备以下能力的 FishBot ROS 2 工作区：

- 机器人模型描述
- Gazebo 仿真
- ros2_control 差速底盘控制
- Nav2 导航基础运行
- Python 应用层导航调用
- 参数化自动巡逻
- 自定义服务接口扩展

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
- 将自动巡逻拓展为完整任务链路

---

## License

Apache-2.0
