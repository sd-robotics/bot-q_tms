#!/bin/bash

# Keep track of the current directory
DIR=`pwd`
cd ..

# Go back to previous directory
cd ${DIR}

# Download required dependencies
python3 -m pip install \
    transforms3d

# Download ROS packages
sudo apt-get update
sudo apt-get install -y \
    ros-$ROS_DISTRO-ros2-control \
    ros-$ROS_DISTRO-ros2-controllers \
    ros-$ROS_DISTRO-control-toolbox \
    ros-$ROS_DISTRO-controller-interface \
    ros-$ROS_DISTRO-controller-manager \
    ros-$ROS_DISTRO-velocity-controllers \
    ros-$ROS_DISTRO-joint-state-publisher \
    ros-$ROS_DISTRO-joint-state-publisher-gui \
    ros-$ROS_DISTRO-joint-state-broadcaster \
    ros-$ROS_DISTRO-joint-limits \
    ros-$ROS_DISTRO-robot-controllers \
    ros-$ROS_DISTRO-robot-controllers-interface \
    ros-$ROS_DISTRO-robot-state-publisher \
    ros-$ROS_DISTRO-hardware-interface \
    ros-$ROS_DISTRO-transmission-interface \
    ros-$ROS_DISTRO-urdf \
    ros-$ROS_DISTRO-urdf-launch \
    ros-$ROS_DISTRO-xacro \
    ros-$ROS_DISTRO-std-msgs \
    ros-$ROS_DISTRO-geometry-msgs \
    ros-$ROS_DISTRO-sensor-msgs \
    ros-$ROS_DISTRO-nav-msgs \
    ros-$ROS_DISTRO-trajectory-msgs \
    ros-$ROS_DISTRO-tf2-geometry-msgs \
    ros-$ROS_DISTRO-tf2-ros \
    ros-$ROS_DISTRO-tf2 \
    ros-$ROS_DISTRO-joy-linux \
    ros-$ROS_DISTRO-launch \
    ros-$ROS_DISTRO-launch-ros

# Install Gazebo Harmonic with binaries
# sudo apt-get update
# sudo apt-get install -y \
#     curl \
#     lsb-release gnupg

# sudo curl https://packages.osrfoundation.org/gazebo.gpg --output /usr/share/keyrings/pkgs-osrf-archive-keyring.gpg
# echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/pkgs-osrf-archive-keyring.gpg] http://packages.osrfoundation.org/gazebo/ubuntu-stable $(lsb_release -cs) main" | sudo tee /etc/apt/sources.list.d/gazebo-stable.list > /dev/null
# sudo apt-get update
# sudo apt-get install -y \
#     gz-harmonic


# Install Gazebo Fortress with binaries
sudo apt-get install -y \
    ros-${ROS_DISTRO}-ros-gz \
    ros-${ROS_DISTRO}-ign-ros2-control \
    ros-${ROS_DISTRO}-ign-ros2-control-demos


# # Setting up Dynamixel USB configuration (Bot-Q TMS: Head and Arm Robot Mechanism)
echo "SUBSYSTEM==\"tty\", ATTRS{idVendor}==\"0403\", ATTRS{idProduct}==\"6014\", ATTRS{serial}==\"FT8ISSV2\", SYMLINK+=\"ttyUSB-DXL_light\", MODE=\"0666\", GROUP:=\"dialout\"," | sudo tee /etc/udev/rules.d/dxl_light.rules
sudo usermod -aG dialout $USER

# # Reload udev rules
sudo udevadm control --reload-rules

# # Trigger the new rules
sudo udevadm trigger

# Go back to previous directory
cd ${DIR}
