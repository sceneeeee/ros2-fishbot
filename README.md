# ros2-fishbot-description

一个基于 ROS 2 的 FishBot 机器人描述练习项目，用于学习 URDF/Xacro 建模、机器人结构模块化拆分，以及在 RViz 中显示机器人模型。

---

## 项目简介

这是我在学习 ROS 2 过程中完成的一个机器人描述项目。  
项目的主要目标是：

- 学习 URDF 的基本建模方法
- 学习使用 Xacro 对机器人描述进行模块化拆分
- 为机器人添加常见传感器模块
- 通过 launch 文件加载并显示机器人模型
- 为后续仿真与功能扩展打基础

当前仓库以一个 ROS 2 workspace 的形式组织，其中核心功能包为：

- `src/fishbot_description`

---

## 项目结构

```text
ros2-fishbot-description/
├── src/
│   └── fishbot_description/
│       ├── config/
│       ├── launch/
│       │   └── display_robot.launch.py
│       ├── urdf/
│       │   ├── first_robot.gv
│       │   ├── first_robot.pdf
│       │   ├── first_robot.urdf
│       │   ├── first_robot.xacro
│       │   └── fishbot/
│       │       ├── actuator/
│       │       ├── sensor/
│       │       │   ├── camera.urdf.xacro
│       │       │   ├── imu.urdf.xacro
│       │       │   └── laser.urdf.xacro
│       │       ├── base.urdf.xacro
│       │       ├── common_inertial.xacro
│       │       └── fishbot.urdf.xacro
│       ├── CMakeLists.txt
│       ├── package.xml
│       └── LICENSE
├── .gitignore
└── README.md
```

---

## 功能说明

### 1. 基础机器人描述

项目中包含基础版本的机器人描述文件：

* `first_robot.urdf`
* `first_robot.xacro`

这部分适合用于练习：

* URDF 基本语法
* link 和 joint 的组织方式
* 从 URDF 过渡到 Xacro 的写法

### 2. 模块化 FishBot 描述

在 `urdf/fishbot/` 目录中，机器人被拆分为多个模块，便于维护和扩展：

* `base.urdf.xacro`：机器人主体结构
* `common_inertial.xacro`：惯性参数相关内容
* `fishbot.urdf.xacro`：整机装配入口文件

这种写法更接近实际项目中的机器人描述组织方式。

### 3. 传感器模块

`sensor/` 目录中包含多个常见传感器描述：

* `camera.urdf.xacro`
* `imu.urdf.xacro`
* `laser.urdf.xacro`

这部分用于练习如何把不同传感器模块挂载到机器人本体上。

### 4. Launch 文件

项目提供了机器人显示用的 launch 文件：

* `launch/display_robot.launch.py`

用于在 ROS 2 环境下启动机器人模型显示流程。

---

## 适合学习的内容

这个项目适合练习以下内容：

* ROS 2 机器人描述功能包结构
* URDF 建模
* Xacro 宏与参数化
* 机器人结构模块化拆分
* 传感器挂载
* launch 文件组织
* RViz 中的机器人模型显示

---

## 环境要求

建议环境：

* Ubuntu 22.04 / 24.04
* ROS 2 Humble / Jazzy
* colcon
* rviz2
* robot_state_publisher
* joint_state_publisher
* xacro

---

## 构建方法

在工作区根目录下执行：

```bash
colcon build
```

编译完成后加载环境：

```bash
source install/setup.bash
```

---

## 运行方法

启动机器人模型显示：

```bash
ros2 launch fishbot_description display_robot.launch.py
```

如果本地环境配置不同，可能需要根据实际情况调整 launch 文件或相关路径。

--

## 项目特点

这个项目更偏向于学习与练习，重点不在于做成完整产品，而在于逐步掌握 ROS 2 机器人描述建模的方法，包括：

* 从简单 URDF 到模块化 Xacro 的过程
* 从单体模型到传感器扩展的过程
* 为后续仿真、控制、导航等内容打基础

---

## 后续可改进方向

后续可以继续完善的内容包括：

* 增加更完整的底盘与执行器结构
* 添加 RViz 配置文件
* 增加模型显示截图
* 完善 package.xml 中的描述信息
* 适配 Gazebo / Ignition / Harmonic 仿真
* 增加 TF、robot_state_publisher、joint_state_publisher 的说明

---

## License

本项目包含 `LICENSE` 文件，当前使用 Apache-2.0 License。

