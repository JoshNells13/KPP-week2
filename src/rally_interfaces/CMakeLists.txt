cmake_minimum_required(VERSION 3.8)
project(rally_interfaces)

find_package(ament_cmake REQUIRED)
find_package(rosidl_default_generators REQUIRED)

rosidl_generate_interfaces(${PROJECT_NAME}
  "msg/Instruction.msg"
  "msg/DriverStatus.msg"
  "msg/RaceMap.msg"
  "msg/RaceState.msg")

ament_export_dependencies(rosidl_default_runtime)

ament_package()
