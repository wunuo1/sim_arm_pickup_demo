from launch import LaunchDescription
from launch_ros.actions import Node
from moveit_configs_utils import MoveItConfigsBuilder
from ament_index_python.packages import get_package_share_directory
import yaml
import os

def load_file(package_name, file_path):
    package_path = get_package_share_directory(package_name)
    absolute_file_path = os.path.join(package_path, file_path)
    try:
        with open(absolute_file_path, 'r') as file:
            return file.read()
    except EnvironmentError:
        # parent of IOError, OSError *and* WindowsError where available.
        return None
# LOAD YAML:
def load_yaml(package_name, file_path):
    package_path = get_package_share_directory(package_name)
    absolute_file_path = os.path.join(package_path, file_path)
    try:
        with open(absolute_file_path, 'r') as file:
            return yaml.safe_load(file)
    except EnvironmentError:
        # parent of IOError, OSError *and* WindowsError where available.
        return None
    
def generate_launch_description():
    
    robot_description_semantic_config = load_file("panda_ros2_moveit2", "config/panda.srdf")
    robot_description_semantic = {"robot_description_semantic": robot_description_semantic_config }
    
    # Kinematics.yaml file:
    kinematics_yaml = load_yaml("panda_ros2_moveit2", "config/kinematics.yaml")
    robot_description_kinematics = {"robot_description_kinematics": kinematics_yaml}

    joint_limits_yaml = load_yaml("panda_ros2_moveit2", "config/joint_limits.yaml")
    robot_description_limits = {"robot_description_planning": joint_limits_yaml}

    ompl_planning_pipeline_config = {
        "ompl": {
            "planning_plugin": "ompl_interface/OMPLPlanner",
            "request_adapters": """default_planner_request_adapters/AddTimeOptimalParameterization default_planner_request_adapters/FixWorkspaceBounds default_planner_request_adapters/FixStartStateBounds default_planner_request_adapters/FixStartStateCollision default_planner_request_adapters/FixStartStatePathConstraints""",
            "start_state_max_bounds_error": 0.1,
        }
    }
    ompl_planning_yaml = load_yaml("panda_ros2_moveit2", "config/ompl_planning.yaml")
    ompl_planning_pipeline_config["ompl"].update(ompl_planning_yaml)

    # MTC Demo node
    pick_place_demo = Node(
        package="sim_arm_pickup_control",
        executable="arm_pickup_test",
        output="screen",
        parameters=[
            # moveit_config.planning_pipelines,
            ompl_planning_pipeline_config,
            robot_description_semantic_config,
            robot_description_semantic,
            kinematics_yaml,
            robot_description_kinematics,
            joint_limits_yaml,
            robot_description_limits,
            {"use_sim_time": True},
            {"ox": 0.0},
            {"oy": 0.707},
            {"oz": 0.0},
            {"ow": 0.707},
            {"px": 0.3},
            {"py": -0.4},
            {"pz": 0.045},
        ],
    )

    return LaunchDescription([pick_place_demo])
