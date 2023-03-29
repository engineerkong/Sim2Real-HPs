# Install script for directory: /home/lingxiao/master/github/ros_deploy/Sim2Real-HPs/rosDeploy/src/niryo_robot_tools_commander

# Set the install prefix
if(NOT DEFINED CMAKE_INSTALL_PREFIX)
  set(CMAKE_INSTALL_PREFIX "/home/lingxiao/master/github/ros_deploy/Sim2Real-HPs/rosDeploy/install")
endif()
string(REGEX REPLACE "/$" "" CMAKE_INSTALL_PREFIX "${CMAKE_INSTALL_PREFIX}")

# Set the install configuration name.
if(NOT DEFINED CMAKE_INSTALL_CONFIG_NAME)
  if(BUILD_TYPE)
    string(REGEX REPLACE "^[^A-Za-z0-9_]+" ""
           CMAKE_INSTALL_CONFIG_NAME "${BUILD_TYPE}")
  else()
    set(CMAKE_INSTALL_CONFIG_NAME "")
  endif()
  message(STATUS "Install configuration: \"${CMAKE_INSTALL_CONFIG_NAME}\"")
endif()

# Set the component getting installed.
if(NOT CMAKE_INSTALL_COMPONENT)
  if(COMPONENT)
    message(STATUS "Install component: \"${COMPONENT}\"")
    set(CMAKE_INSTALL_COMPONENT "${COMPONENT}")
  else()
    set(CMAKE_INSTALL_COMPONENT)
  endif()
endif()

# Install shared libraries without execute permission?
if(NOT DEFINED CMAKE_INSTALL_SO_NO_EXE)
  set(CMAKE_INSTALL_SO_NO_EXE "1")
endif()

# Is this installation the result of a crosscompile?
if(NOT DEFINED CMAKE_CROSSCOMPILING)
  set(CMAKE_CROSSCOMPILING "FALSE")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/niryo_robot_tools_commander/msg" TYPE FILE FILES
    "/home/lingxiao/master/github/ros_deploy/Sim2Real-HPs/rosDeploy/src/niryo_robot_tools_commander/msg/TCP.msg"
    "/home/lingxiao/master/github/ros_deploy/Sim2Real-HPs/rosDeploy/src/niryo_robot_tools_commander/msg/ToolCommand.msg"
    )
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/niryo_robot_tools_commander/srv" TYPE FILE FILES "/home/lingxiao/master/github/ros_deploy/Sim2Real-HPs/rosDeploy/src/niryo_robot_tools_commander/srv/SetTCP.srv")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/niryo_robot_tools_commander/action" TYPE FILE FILES "/home/lingxiao/master/github/ros_deploy/Sim2Real-HPs/rosDeploy/src/niryo_robot_tools_commander/action/Tool.action")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/niryo_robot_tools_commander/msg" TYPE FILE FILES
    "/home/lingxiao/master/github/ros_deploy/Sim2Real-HPs/rosDeploy/devel/share/niryo_robot_tools_commander/msg/ToolAction.msg"
    "/home/lingxiao/master/github/ros_deploy/Sim2Real-HPs/rosDeploy/devel/share/niryo_robot_tools_commander/msg/ToolActionGoal.msg"
    "/home/lingxiao/master/github/ros_deploy/Sim2Real-HPs/rosDeploy/devel/share/niryo_robot_tools_commander/msg/ToolActionResult.msg"
    "/home/lingxiao/master/github/ros_deploy/Sim2Real-HPs/rosDeploy/devel/share/niryo_robot_tools_commander/msg/ToolActionFeedback.msg"
    "/home/lingxiao/master/github/ros_deploy/Sim2Real-HPs/rosDeploy/devel/share/niryo_robot_tools_commander/msg/ToolGoal.msg"
    "/home/lingxiao/master/github/ros_deploy/Sim2Real-HPs/rosDeploy/devel/share/niryo_robot_tools_commander/msg/ToolResult.msg"
    "/home/lingxiao/master/github/ros_deploy/Sim2Real-HPs/rosDeploy/devel/share/niryo_robot_tools_commander/msg/ToolFeedback.msg"
    )
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  include("/home/lingxiao/master/github/ros_deploy/Sim2Real-HPs/rosDeploy/build/niryo_robot_tools_commander/catkin_generated/safe_execute_install.cmake")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/niryo_robot_tools_commander/cmake" TYPE FILE FILES "/home/lingxiao/master/github/ros_deploy/Sim2Real-HPs/rosDeploy/build/niryo_robot_tools_commander/catkin_generated/installspace/niryo_robot_tools_commander-msg-paths.cmake")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/include" TYPE DIRECTORY FILES "/home/lingxiao/master/github/ros_deploy/Sim2Real-HPs/rosDeploy/devel/include/niryo_robot_tools_commander")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/roseus/ros" TYPE DIRECTORY FILES "/home/lingxiao/master/github/ros_deploy/Sim2Real-HPs/rosDeploy/devel/share/roseus/ros/niryo_robot_tools_commander")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/common-lisp/ros" TYPE DIRECTORY FILES "/home/lingxiao/master/github/ros_deploy/Sim2Real-HPs/rosDeploy/devel/share/common-lisp/ros/niryo_robot_tools_commander")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/gennodejs/ros" TYPE DIRECTORY FILES "/home/lingxiao/master/github/ros_deploy/Sim2Real-HPs/rosDeploy/devel/share/gennodejs/ros/niryo_robot_tools_commander")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  execute_process(COMMAND "/usr/bin/python2" -m compileall "/home/lingxiao/master/github/ros_deploy/Sim2Real-HPs/rosDeploy/devel/lib/python2.7/dist-packages/niryo_robot_tools_commander")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/python2.7/dist-packages" TYPE DIRECTORY FILES "/home/lingxiao/master/github/ros_deploy/Sim2Real-HPs/rosDeploy/devel/lib/python2.7/dist-packages/niryo_robot_tools_commander" REGEX "/\\_\\_init\\_\\_\\.py$" EXCLUDE REGEX "/\\_\\_init\\_\\_\\.pyc$" EXCLUDE)
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/python2.7/dist-packages" TYPE DIRECTORY FILES "/home/lingxiao/master/github/ros_deploy/Sim2Real-HPs/rosDeploy/devel/lib/python2.7/dist-packages/niryo_robot_tools_commander" FILES_MATCHING REGEX "/home/lingxiao/master/github/ros_deploy/Sim2Real-HPs/rosDeploy/devel/lib/python2\\.7/dist-packages/niryo_robot_tools_commander/.+/__init__.pyc?$")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/pkgconfig" TYPE FILE FILES "/home/lingxiao/master/github/ros_deploy/Sim2Real-HPs/rosDeploy/build/niryo_robot_tools_commander/catkin_generated/installspace/niryo_robot_tools_commander.pc")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/niryo_robot_tools_commander/cmake" TYPE FILE FILES "/home/lingxiao/master/github/ros_deploy/Sim2Real-HPs/rosDeploy/build/niryo_robot_tools_commander/catkin_generated/installspace/niryo_robot_tools_commander-msg-extras.cmake")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/niryo_robot_tools_commander/cmake" TYPE FILE FILES
    "/home/lingxiao/master/github/ros_deploy/Sim2Real-HPs/rosDeploy/build/niryo_robot_tools_commander/catkin_generated/installspace/niryo_robot_tools_commanderConfig.cmake"
    "/home/lingxiao/master/github/ros_deploy/Sim2Real-HPs/rosDeploy/build/niryo_robot_tools_commander/catkin_generated/installspace/niryo_robot_tools_commanderConfig-version.cmake"
    )
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/niryo_robot_tools_commander" TYPE FILE FILES "/home/lingxiao/master/github/ros_deploy/Sim2Real-HPs/rosDeploy/src/niryo_robot_tools_commander/package.xml")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/niryo_robot_tools_commander" TYPE PROGRAM FILES "/home/lingxiao/master/github/ros_deploy/Sim2Real-HPs/rosDeploy/build/niryo_robot_tools_commander/catkin_generated/installspace/tool_commander_node.py")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/niryo_robot_tools_commander" TYPE PROGRAM FILES "/home/lingxiao/master/github/ros_deploy/Sim2Real-HPs/rosDeploy/build/niryo_robot_tools_commander/catkin_generated/installspace/tool_ros_command_interface.py")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/niryo_robot_tools_commander" TYPE PROGRAM FILES "/home/lingxiao/master/github/ros_deploy/Sim2Real-HPs/rosDeploy/build/niryo_robot_tools_commander/catkin_generated/installspace/tools_classes.py")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/niryo_robot_tools_commander" TYPE PROGRAM FILES "/home/lingxiao/master/github/ros_deploy/Sim2Real-HPs/rosDeploy/build/niryo_robot_tools_commander/catkin_generated/installspace/transform_handler.py")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/niryo_robot_tools_commander/launch" TYPE DIRECTORY FILES "/home/lingxiao/master/github/ros_deploy/Sim2Real-HPs/rosDeploy/src/niryo_robot_tools_commander/launch/")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/niryo_robot_tools_commander/config" TYPE DIRECTORY FILES "/home/lingxiao/master/github/ros_deploy/Sim2Real-HPs/rosDeploy/src/niryo_robot_tools_commander/config/")
endif()

