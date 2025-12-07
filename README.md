# Bot-Q TMS Simulator (Gazebo)

[![README in English](https://img.shields.io/badge/English-d9d9d9)](./README.md)
[![日本語版 README](https://img.shields.io/badge/日本語-d9d9d9)](./README_JA.md)

<p style="display: inline">
  <img src="https://img.shields.io/badge/-Ubuntu_22.04_LTS-555555.svg?style=flat&logo=ubuntu">  
  <img src="https://img.shields.io/badge/-Gazebo Fortress-orange.svg?style=flat&logo=gazebo&logoColor=white">
  <img src="https://img.shields.io/badge/-ROS2 Humble-%2322314E?style=flat&logo=ROS&logoColor=white">
  <img src="https://img.shields.io/badge/-Python 3.10-3776AB.svg?logo=python&style=flat&logoColor=white">
  <img src="https://img.shields.io/badge/License-Apache--2.0-60C060.svg?style=flat">
</p>

## Table of Contents
1. [**What is Bot-Q TMS?**](#what-is-bot-q-tms)
2. [**Prerequisites**](#prerequisites)
3. [**Installation**](#installation)
    1. [Clone Repository](#clone-repository)
    2. [Install Dependencies](#install-dependencies)
4. [**Usage**](#usage)
    1. [Build & Source](#build--source)
    2. [Launch Simulation (Gazebo)](#launch-simulation-gazebo)
    3. [Launch Real Robot](#launch-real-robot)
    4. [Visualization](#visualization)
5. [**Topics & Interface**](#topics--interface)
6. [**License**](#license)

---

## What is Bot-Q TMS?
Bot-Q TMS is a tether management system for the Q-bot docking tasks involving cable or filament handling. It features a 3-DoF spool/extruder mechanism.

This repository provides the ROS 2 packages required to simulate the robot in Gazebo (using `ros_gz`) and control the real hardware via `ros2_control` (for Dynamixel).

## Prerequisites
In order to use this project, you need to get ready the following environment.

|  Package  |         Version         |
| --------- | ----------------------- |
|   Ubuntu  | 22.04 (Jammy Jellyfish) |
|   Gazebo  | Fortress                |
|    ROS    | Humble Hawksbill        |
|   Python  | 3.10 <=                 |

## Installation

### Clone Repository
Make a workspace if you do not have one already.
```bash
mkdir -p ~/bot_q_tms_ws/src
cd ~/bot_q_tms_ws/src
```

Clone this package into your workspace.
```bash
git clone https://github.com/sd-robotics/bot-q_tms.git
```

### Install Dependencies
Install the required ROS 2 packages and dependencies.

```bash
cd ~/bot_q_tms_ws/src/bot-q_tms
bash install.sh
```

## Usage

### Build & Source
Build the packages and source your workspace.
```bash
cd ~/bot_q_tms_ws
colcon build --symlink-install
source install/setup.bash
```

### Launch Simulation (Gazebo)
To launch the robot in the Gazebo simulation environment with RViz visualization:

```bash
ros2 launch bot_q_tms_bringup gz_minimal.launch.py
```

This will spawn the robot (including the carrier mechanism) in an empty Gazebo world and bridge the necessary topics.

### Launch Real Robot
To launch the drivers for the physical robot (Dynamixel hardware interface):

```bash
ros2 launch bot_q_tms_bringup real_minimal.launch.py
```

### Visualization
To visualize the URDF model and joint states without running the full physics simulation:

```bash
ros2 launch bot_q_tms_description display.launch.py use_gui:=True
```

## Topics & Interface

### Sensors
The simulation and real robot publish the following sensor data:

| Sensor Type | Topic Name | Description |
|---|---|---|
| **Joints** | `/bot_q_tms/joint_states` | Current position and velocity of joints. |

### Control
The robot utilizes `ros2_control` to move the three actuators attached to the TMS.

| Controller | Type | Description |
|---|---|---|
| `velocity_controller` | `JointGroupVelocityController` | Controls the spool, guider, and extruder gears. |

## License
This repository is licensed under the Apache License 2.0. See the [LICENSE](./LICENSE) file for details.
