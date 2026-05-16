# About ros2-fishbot

## One-line description

ROS 2 Humble FishBot workspace for URDF/Xacro modeling, Gazebo simulation, ros2_control differential drive, Nav2 navigation, and autopatrol demos.

## 中文简介

`ros2-fishbot` 是一个面向移动机器人学习与实践的 ROS 2 Humble 工作区。它围绕 FishBot 构建了一条从机器人建模到仿真控制、从 Nav2 导航到自动巡逻应用的完整基础链路。

项目适合作为 ROS 2 移动机器人入门项目，也适合作为后续学习 SLAM、Nav2 参数调试、路径规划、自动巡逻、任务编排和多传感器融合的实验起点。

## English summary

`ros2-fishbot` is a ROS 2 Humble workspace for learning and experimenting with a simulated FishBot mobile robot. It includes robot description files, Gazebo simulation, ros2_control differential-drive control, Nav2 bringup, Python navigation demos, a custom speech service interface, and a configurable autopatrol workflow.

## Recommended GitHub About

Description:

```text
ROS 2 Humble FishBot workspace with URDF/Xacro, Gazebo, ros2_control, Nav2, Python navigation demos, and autopatrol examples.
```

Topics:

```text
ros2
ros2-humble
fishbot
gazebo
gazebo-classic
urdf
xacro
ros2-control
navigation2
nav2
mobile-robot
robotics
autonomous-navigation
autopatrol
rviz2
```

## Included packages

| Package | Purpose |
|---|---|
| `fishbot_description` | Robot description, RViz display, Gazebo world, and ros2_control configuration |
| `fishbot_navigation2` | Nav2 launch files, map, navigation parameters, and RViz startup |
| `fishbot_application` | Python examples for initial pose, goal navigation, waypoint following, and pose lookup |
| `autopatrol_interfaces` | Custom service interfaces for the autopatrol workflow |
| `autopatrol_robot` | Configurable patrol node, speech service integration, and image capture |

## Audience

- ROS 2 beginners who want a complete mobile robot workspace.
- Students learning URDF, Xacro, Gazebo, and Nav2.
- Developers experimenting with differential-drive robot simulation.
- Learners who want to extend a simple robot into patrol, SLAM, and task-level applications.

## Current status

The workspace is usable as a simulation-first learning project. It can launch the FishBot model in Gazebo, control the robot with `ros2_control`, bring up Nav2 with an existing map, and run Python navigation and autopatrol demos.

The next useful improvements are SLAM integration, richer patrol task state, cleaner structured patrol configuration, CI/lint coverage, and visual demo assets in the README.
