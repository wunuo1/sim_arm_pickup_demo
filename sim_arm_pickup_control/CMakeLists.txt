cmake_minimum_required(VERSION 3.8)
project(sim_arm_pickup_control)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

# find dependencies
find_package(ament_cmake REQUIRED)
find_package(moveit_ros_planning_interface REQUIRED)
find_package(rclcpp REQUIRED)
find_package(moveit_task_constructor_core REQUIRED)
find_package(sim_arm_location_msg REQUIRED)

add_executable(arm_pickup_service src/arm_pickup_service.cpp)

add_executable(arm_pickup_test src/arm_pickup_test.cpp)

target_include_directories(arm_pickup_service PUBLIC
  $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>
  $<INSTALL_INTERFACE:include>)
target_compile_features(arm_pickup_service PUBLIC c_std_99 cxx_std_17)  # Require C99 and C++17


target_include_directories(arm_pickup_test PUBLIC
  $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>
  $<INSTALL_INTERFACE:include>)
target_compile_features(arm_pickup_test PUBLIC c_std_99 cxx_std_17)

ament_target_dependencies(
  arm_pickup_service
  "moveit_ros_planning_interface"
  "rclcpp"
  "moveit_task_constructor_core"
  "sim_arm_location_msg"
)

ament_target_dependencies(
  arm_pickup_test
  "moveit_ros_planning_interface"
  "rclcpp"
  "moveit_task_constructor_core"
)

install(TARGETS arm_pickup_service arm_pickup_test
  DESTINATION lib/${PROJECT_NAME})

  install(
    DIRECTORY 
      launch
    DESTINATION 
      share/${PROJECT_NAME}
  )

if(BUILD_TESTING)
  find_package(ament_lint_auto REQUIRED)
  # the following line skips the linter which checks for copyrights
  # comment the line when a copyright and license is added to all source files
  set(ament_cmake_copyright_FOUND TRUE)
  # the following line skips cpplint (only works in a git repo)
  # comment the line when this package is in a git repo and when
  # a copyright and license is added to all source files
  set(ament_cmake_cpplint_FOUND TRUE)
  ament_lint_auto_find_test_dependencies()
endif()

ament_package()
