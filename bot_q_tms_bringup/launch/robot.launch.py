import os
from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, ExecuteProcess, OpaqueFunction, IncludeLaunchDescription, RegisterEventHandler
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.event_handlers import OnProcessExit
from launch.substitutions import PathJoinSubstitution, LaunchConfiguration
from launch.conditions import LaunchConfigurationEquals
from launch_ros.substitutions import FindPackageShare
from launch_ros.actions import Node

import xacro

def generate_launch_description():
    arg_robot_name = DeclareLaunchArgument('robot_name', default_value='bot_q_tms')

    arg_robot_coords_x = DeclareLaunchArgument('robot_coords_x', default_value='0')
    arg_robot_coords_y = DeclareLaunchArgument('robot_coords_y', default_value='0')
    arg_robot_coords_z = DeclareLaunchArgument('robot_coords_z', default_value='0')
    arg_robot_coords_X = DeclareLaunchArgument('robot_coords_X', default_value='0')
    arg_robot_coords_Y = DeclareLaunchArgument('robot_coords_Y', default_value='0')
    arg_robot_coords_Z = DeclareLaunchArgument('robot_coords_Z', default_value='0')

    arg_enable_gz = DeclareLaunchArgument('enable_gz', default_value='True')
    arg_enable_carrier = DeclareLaunchArgument('enable_carrier', default_value='True')

    return LaunchDescription([
        arg_robot_name,
        arg_robot_coords_x,
        arg_robot_coords_y,
        arg_robot_coords_z,
        arg_robot_coords_X,
        arg_robot_coords_Y,
        arg_robot_coords_Z,
        arg_enable_gz,
        arg_enable_carrier,
        OpaqueFunction(function = launch_gz),
    ])


def launch_gz(context, *args, **kwargs):
    robot_name = LaunchConfiguration('robot_name').perform(context)

    robot_coords_x = LaunchConfiguration('robot_coords_x').perform(context)
    robot_coords_y = LaunchConfiguration('robot_coords_y').perform(context)
    robot_coords_z = LaunchConfiguration('robot_coords_z').perform(context)
    robot_coords_X = LaunchConfiguration('robot_coords_X').perform(context)
    robot_coords_Y = LaunchConfiguration('robot_coords_Y').perform(context)
    robot_coords_Z = LaunchConfiguration('robot_coords_Z').perform(context)

    enable_gz = LaunchConfiguration('enable_gz').perform(context)
    enable_carrier = LaunchConfiguration('enable_carrier').perform(context)

    robot_description = os.path.join(get_package_share_directory(
        'bot_q_tms_description'), 
        'robots',
        'bot_q_tms_robot.urdf.xacro'
    )
    robot_description_config = xacro.process_file(
        robot_description,
        mappings={
            'enable_gz'      : enable_gz,
            'enable_carrier' : enable_carrier,
            'robot_name'     : robot_name,
        })
    
    if enable_gz == 'False':
        controller_config = os.path.join(get_package_share_directory(
            'bot_q_tms_control'),
            'config',
            'real_controllers.yaml'
        )

        controller_manager = Node(
            package="controller_manager",
            executable="ros2_control_node",
            namespace=robot_name,
            parameters=[
                {"robot_description": robot_description_config.toxml()}, controller_config],
            output="screen",
        )

    joint_state_broadcaster = ExecuteProcess(
        cmd=['ros2', 'control', 'load_controller',
            '--set-state', 'active',
            '--controller-manager', robot_name+'/controller_manager',
            'joint_state_broadcaster'
        ],
        output='screen'
    )

    velocity_controller = ExecuteProcess(
        cmd=['ros2', 'control', 'load_controller',
            '--set-state', 'active',
            '--controller-manager', robot_name+'/controller_manager',
            'velocity_controller'
        ],
        output='screen'
    )

    robot_state_publisher_node = Node(
        package="robot_state_publisher",
        executable="robot_state_publisher",
        name="robot_state_publisher",
        namespace=robot_name,
        parameters=[
            {"frame_prefix": robot_name + '/'},
            {"robot_description": robot_description_config.toxml()},
            {"use_sim_time": True if enable_gz == 'True' else False},
        ],
        output="screen",
    )

    if enable_gz == 'True':
        gz_spawn_entity_node = Node(
            package='ros_gz_sim',
            executable='create',
            namespace=robot_name,
            arguments=[
                '-topic', '/' + robot_name + '/robot_description',
                '-name', robot_name,
                '-x', robot_coords_x,
                '-y', robot_coords_y,
                '-z', robot_coords_z,
                '-X', robot_coords_X,
                '-Y', robot_coords_Y,
                '-Z', robot_coords_Z,
            ],
            output='screen',
        )

        gz_bridge_node = Node(
            package='ros_gz_bridge',
            executable='parameter_bridge',
            namespace=robot_name,
            arguments=[
                        "/" + robot_name + "/joint_states" + "@sensor_msgs/msg/JointState" + "[ignition.msgs.Model",
                    ],
            output='screen'
        )

    if enable_gz == 'False':

        return [
            controller_manager,
            joint_state_broadcaster,
            velocity_controller,
            robot_state_publisher_node,
        ]
    
    else:
        return [
            gz_spawn_entity_node,
            gz_bridge_node,
            RegisterEventHandler(
                event_handler=OnProcessExit(
                    target_action=gz_spawn_entity_node,
                    on_exit=[joint_state_broadcaster],
                )
            ),
            RegisterEventHandler(
                event_handler=OnProcessExit(
                    target_action=joint_state_broadcaster,
                    on_exit=[velocity_controller],
                )
            ),
            robot_state_publisher_node,
        ]
