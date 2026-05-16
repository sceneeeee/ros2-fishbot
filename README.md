# ros2-fishbot

`ros2-fishbot` 是一个基于 **ROS 2 Humble** 的 FishBot 移动机器人学习与实践工作区。项目把机器人描述、Gazebo 仿真、`ros2_control` 差速底盘控制、Nav2 导航、Python 导航示例、自定义服务接口和自动巡逻应用放在同一个 ROS 2 workspace 中，适合用来系统练习移动机器人软件栈的完整链路。

当前仓库已经从单一的 `fishbot_description` 学习包扩展为一个可运行、可继续迭代的 FishBot 实验平台。你可以用它学习 URDF / Xacro 建模、传感器挂载、仿真控制、地图导航、航点任务、语音播报和巡逻图像采集。

> 当前包版本：`2.0.0`
>
> 推荐运行环境：Ubuntu 22.04 + ROS 2 Humble + Gazebo Classic

---

## 项目能做什么

- 使用 URDF / Xacro 描述 FishBot 机器人本体、轮子、万向轮和传感器模块。
- 在 RViz 中查看机器人模型和 TF 关系。
- 在 Gazebo Classic 中加载室内房间场景并生成 FishBot。
- 通过 `ros2_control` 加载 `joint_state_broadcaster` 和 `diff_drive_controller`。
- 向 `/cmd_vel` 发布速度指令，驱动仿真机器人移动。
- 使用 Nav2 加载地图、定位、规划路径并执行导航任务。
- 使用 Python 示例调用 `nav2_simple_commander` 完成初始位姿设置、单点导航、航点跟随和当前位姿查询。
- 使用自定义 `SpeechText.srv` 服务完成巡逻过程中的中文语音播报。
- 按参数文件配置自动巡逻点，并在巡逻过程中保存相机图像。

---

## 工作区结构

```text
ros2-fishbot/
├── README.md
├── ABOUT.md
├── img_*.png
└── src/
    ├── fishbot_description/
    │   ├── config/
    │   ├── launch/
    │   ├── urdf/
    │   └── world/
    ├── fishbot_navigation2/
    │   ├── config/
    │   ├── launch/
    │   └── maps/
    ├── fishbot_application/
    │   └── fishbot_application/
    ├── autopatrol_interfaces/
    │   └── srv/
    └── autopatrol_robot/
        ├── autopatrol_robot/
        ├── config/
        └── launch/
```

根目录下的 `img_*.png` 是自动巡逻图像采集流程生成或保留的示例图片。

---

## ROS 2 包说明

| Package | 类型 | 主要职责 |
|---|---|---|
| `fishbot_description` | `ament_cmake` | FishBot 机器人描述、RViz 模型显示、Gazebo 场景、`ros2_control` 配置 |
| `fishbot_navigation2` | `ament_cmake` | Nav2 bringup、地图加载、导航参数、RViz 导航界面 |
| `fishbot_application` | `ament_python` | `nav2_simple_commander` 示例：初始位姿、单点导航、航点跟随、位姿查询 |
| `autopatrol_interfaces` | `ament_cmake` | 自动巡逻用自定义服务接口，当前包含 `SpeechText.srv` |
| `autopatrol_robot` | `ament_python` | 自动巡逻节点、语音服务客户端、相机图像保存流程 |

---

## 运行链路

### 仿真与控制链路

```text
fishbot_description
  -> xacro 生成 robot_description
  -> robot_state_publisher 发布机器人模型
  -> gazebo_ros 生成 FishBot 实体
  -> gazebo_ros2_control 加载控制插件
  -> joint_state_broadcaster 发布关节状态
  -> diff_drive_controller 订阅 /cmd_vel 并发布里程计
```

### 导航与应用链路

```text
fishbot_navigation2
  -> Nav2 bringup 加载地图和参数
  -> RViz 显示导航状态
  -> fishbot_application 调用 BasicNavigator
  -> autopatrol_robot 根据巡逻点循环导航
  -> autopatrol_interfaces 提供语音播报服务接口
```

---

## 环境要求

建议使用以下环境：

- Ubuntu 22.04
- ROS 2 Humble Desktop
- Gazebo Classic
- `colcon`
- `rosdep`
- `xacro`
- `rviz2`
- Navigation2

核心 ROS 依赖包括：

- `gazebo_ros`
- `gazebo_ros2_control`
- `controller_manager`
- `joint_state_broadcaster`
- `diff_drive_controller`
- `nav2_bringup`
- `nav2_simple_commander`
- `tf2_ros`
- `tf_transformations`
- `cv_bridge`

自动巡逻语音播报还需要系统 `espeak-ng` 引擎和 Python `espeakng` 模块。

---

## 安装依赖

先安装常用 ROS 依赖：

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

如果你要运行语音播报：

```bash
sudo apt install espeak-ng
pip install espeakng
```

也可以在工作区根目录使用 `rosdep` 补齐依赖：

```bash
rosdep install --from-paths src --ignore-src -r -y
```

---

## 克隆与构建

```bash
git clone https://github.com/sceneeeee/ros2-fishbot.git
cd ros2-fishbot
colcon build --symlink-install
source install/setup.bash
```

如果你的浏览器可以访问 GitHub，但终端 `git clone` 卡住，通常是终端没有走代理。可以临时指定代理后再克隆：

```bash
git -c http.proxy=socks5h://127.0.0.1:7897 clone https://github.com/sceneeeee/ros2-fishbot.git
```

把端口换成你本机代理软件实际监听的端口。

---

## 快速开始

下面的命令默认你已经在工作区根目录执行过：

```bash
source install/setup.bash
```

### 1. 在 RViz 中显示机器人模型

```bash
ros2 launch fishbot_description display_robot.launch.py
```

显示模块化 FishBot 模型：

```bash
ros2 launch fishbot_description display_robot.launch.py \
  model:=$(ros2 pkg prefix fishbot_description)/share/fishbot_description/urdf/fishbot/fishbot.urdf.xacro
```

### 2. 启动 Gazebo 仿真

```bash
ros2 launch fishbot_description gazebo_sim.launch.py
```

该 launch 文件会加载 `custom_room.world`，生成 FishBot，并依次启动：

- `fishbot_joint_state_broadcaster`
- `fishbot_diff_drive_controller`

### 3. 发布速度指令

前进：

```bash
ros2 topic pub /cmd_vel geometry_msgs/msg/Twist \
  "{linear: {x: 0.2}, angular: {z: 0.0}}" -r 10
```

原地旋转：

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

先保持 Gazebo 仿真运行，然后在新的终端中进入工作区并加载环境：

```bash
source install/setup.bash
ros2 launch fishbot_navigation2 navigation2.launch.py
```

默认会使用：

- `use_sim_time=true`
- `src/fishbot_navigation2/maps/room.yaml`
- `src/fishbot_navigation2/config/nav2_params.yaml`
- Nav2 默认 RViz 配置

### 设置初始位姿

```bash
ros2 run fishbot_application init_robot_pose
```

### 单目标点导航

```bash
ros2 run fishbot_application nav_to_pose
```

默认示例目标点为：

- `x = 2.0`
- `y = 1.0`

### 航点跟随

```bash
ros2 run fishbot_application waypoint_follower
```

### 查询当前位姿

```bash
ros2 run fishbot_application get_robot_pose
```

该节点会查询 `map -> base_footprint` 的 TF 变换，并输出机器人当前位姿。

---

## 自动巡逻

`autopatrol_robot` 会读取巡逻点参数，循环调用 Nav2 导航，并通过 `SpeechText.srv` 调用语音播报服务。到达巡逻点后，节点会尝试保存 `/camera_sensor/image_raw` 的最新图像。

### 1. 启动基础环境

先确保以下部分已经运行正常：

- Gazebo 仿真
- Nav2 导航
- 地图定位
- 机器人初始位姿

### 2. 启动语音服务节点

```bash
ros2 run autopatrol_robot speaker
```

### 3. 启动巡逻节点

```bash
ros2 run autopatrol_robot patrol_node \
  --ros-args \
  --params-file $(ros2 pkg prefix autopatrol_robot)/share/autopatrol_robot/config/patrol_config.yaml
```

### 4. 巡逻参数

参数文件位于：

```text
src/autopatrol_robot/config/patrol_config.yaml
```

当前参数包括：

| 参数 | 说明 |
|---|---|
| `initial_point` | 初始位姿，格式为 `[x, y, yaw]` |
| `patrol_points` | 巡逻点序列，格式为 `[x1, y1, yaw1, x2, y2, yaw2, ...]` |
| `use_sim_time` | 是否使用仿真时间，建议和 Gazebo / Nav2 的时间配置保持一致 |

`patrol_node.py` 还支持 `img_save_path` 参数。设置后，巡逻图像会保存到对应路径；不设置时会使用当前运行目录。

---

## Nav2 参数说明

导航参数位于：

```text
src/fishbot_navigation2/config/nav2_params.yaml
```

当前配置重点是把局部路径跟随器调整为 **RPP（Regulated Pure Pursuit）**。相比早期 DWB 配置，RPP 在室内走廊、墙边和巡逻任务中的路径跟随更平滑，也更适合作为这个 FishBot 仿真实验的默认局部控制器。

如果你要继续调参，可以优先关注：

- 机器人 footprint / inflation radius
- controller server 的局部控制器配置
- planner server 的全局规划器配置
- AMCL 与地图坐标系配置
- `use_sim_time` 是否和 Gazebo / Nav2 一致

---

## 常见问题

### 浏览器能打开 GitHub，但终端 clone 卡住

通常是浏览器走了代理，但终端没有继承代理配置。可以检查本地代理端口：

```bash
lsof -nP -iTCP -sTCP:LISTEN | grep -E "7890|7897|1080|1087"
```

临时使用代理 clone：

```bash
git -c http.proxy=socks5h://127.0.0.1:7897 clone https://github.com/sceneeeee/ros2-fishbot.git
```

长期使用可以设置 Git 代理：

```bash
git config --global http.proxy socks5h://127.0.0.1:7897
git config --global https.proxy socks5h://127.0.0.1:7897
```

取消代理：

```bash
git config --global --unset http.proxy
git config --global --unset https.proxy
```

### Gazebo 中机器人不动

检查控制器是否正常加载：

```bash
ros2 control list_controllers
```

确认 `fishbot_diff_drive_controller` 处于 `active` 状态，并确认 `/cmd_vel` 有速度消息。

### Nav2 不动或定位不稳定

优先检查：

- Gazebo 是否仍在运行
- 所有终端是否都执行了 `source install/setup.bash`
- `use_sim_time` 是否一致
- RViz 中初始位姿是否设置正确
- `map -> odom -> base_footprint` TF 是否连续

### 自动巡逻不播报

确认 `speaker` 节点已经运行，且系统安装了 `espeakng` Python 模块。也可以检查服务是否存在：

```bash
ros2 service list | grep speech_text
```

### 巡逻图片没有保存

确认相机话题存在：

```bash
ros2 topic list | grep camera
```

如果需要固定保存目录，请给 `patrol_node` 配置 `img_save_path`，并确保目录存在且可写。

---

## 适合继续扩展的方向

- 接入 SLAM Toolbox，补齐建图与保存地图流程。
- 增加键盘遥控或手柄遥控节点。
- 为巡逻任务增加暂停、恢复、取消和任务状态反馈。
- 把巡逻点从一维数组升级为更清晰的结构化配置。
- 使用行为树编排巡逻、播报、拍照和异常处理。
- 增加更复杂的 Gazebo 场景、障碍物和传感器噪声。
- 补充 CI、格式化、lint 和基础测试。
- 为 README 增加截图、录屏或 GIF。

---

## License

Apache-2.0
