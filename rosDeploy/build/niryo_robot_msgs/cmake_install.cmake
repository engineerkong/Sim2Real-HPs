# Install script for directory: /home/lingxiao/master/Sim2Real_py2/Sim2Real_py2/src/niryo_robot_msgs

# Set the install prefix
if(NOT DEFINED CMAKE_INSTALL_PREFIX)
  set(CMAKE_INSTALL_PREFIX "/home/lingxiao/master/Sim2Real_py2/Sim2Real_py2/install")
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
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/niryo_robot_msgs/msg" TYPE FILE FILES
    "/home/lingxiao/master/Sim2Real_py2/Sim2Real_py2/src/niryo_robot_msgs/msg/BusState.msg"
    "/home/lingxiao/master/Sim2Real_py2/Sim2Real_py2/src/niryo_robot_msgs/msg/CommandStatus.msg"
    "/home/lingxiao/master/Sim2Real_py2/Sim2Real_py2/src/niryo_robot_msgs/msg/HardwareStatus.msg"
    "/home/lingxiao/master/Sim2Real_py2/Sim2Real_py2/src/niryo_robot_msgs/msg/MotorHeader.msg"
    "/home/lingxiao/master/Sim2Real_py2/Sim2Real_py2/src/niryo_robot_msgs/msg/ObjectPose.msg"
    "/home/lingxiao/master/Sim2Real_py2/Sim2Real_py2/src/niryo_robot_msgs/msg/RPY.msg"
    "/home/lingxiao/master/Sim2Real_py2/Sim2Real_py2/src/niryo_robot_msgs/msg/RobotState.msg"
    "/home/lingxiao/master/Sim2Real_py2/Sim2Real_py2/src/niryo_robot_msgs/msg/SoftwareVersion.msg"
    )
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/niryo_robot_msgs/srv" TYPE FILE FILES
    "/home/lingxiao/master/Sim2Real_py2/Sim2Real_py2/src/niryo_robot_msgs/srv/AdvertiseShutdown.srv"
    "/home/lingxiao/master/Sim2Real_py2/Sim2Real_py2/src/niryo_robot_msgs/srv/GetBool.srv"
    "/home/lingxiao/master/Sim2Real_py2/Sim2Real_py2/src/niryo_robot_msgs/srv/GetInt.srv"
    "/home/lingxiao/master/Sim2Real_py2/Sim2Real_py2/src/niryo_robot_msgs/srv/GetNameDescriptionList.srv"
    "/home/lingxiao/master/Sim2Real_py2/Sim2Real_py2/src/niryo_robot_msgs/srv/GetString.srv"
    "/home/lingxiao/master/Sim2Real_py2/Sim2Real_py2/src/niryo_robot_msgs/srv/GetStringList.srv"
    "/home/lingxiao/master/Sim2Real_py2/Sim2Real_py2/src/niryo_robot_msgs/srv/Ping.srv"
    "/home/lingxiao/master/Sim2Real_py2/Sim2Real_py2/src/niryo_robot_msgs/srv/SetBool.srv"
    "/home/lingxiao/master/Sim2Real_py2/Sim2Real_py2/src/niryo_robot_msgs/srv/SetFloat.srv"
    "/home/lingxiao/master/Sim2Real_py2/Sim2Real_py2/src/niryo_robot_msgs/srv/SetInt.srv"
    "/home/lingxiao/master/Sim2Real_py2/Sim2Real_py2/src/niryo_robot_msgs/srv/SetString.srv"
    "/home/lingxiao/master/Sim2Real_py2/Sim2Real_py2/src/niryo_robot_msgs/srv/Trigger.srv"
    )
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/niryo_robot_msgs/cmake" TYPE FILE FILES "/home/lingxiao/master/Sim2Real_py2/Sim2Real_py2/build/niryo_robot_msgs/catkin_generated/installspace/niryo_robot_msgs-msg-paths.cmake")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/include" TYPE DIRECTORY FILES "/home/lingxiao/master/Sim2Real_py2/Sim2Real_py2/devel/include/niryo_robot_msgs")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/roseus/ros" TYPE DIRECTORY FILES "/home/lingxiao/master/Sim2Real_py2/Sim2Real_py2/devel/share/roseus/ros/niryo_robot_msgs")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/common-lisp/ros" TYPE DIRECTORY FILES "/home/lingxiao/master/Sim2Real_py2/Sim2Real_py2/devel/share/common-lisp/ros/niryo_robot_msgs")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/gennodejs/ros" TYPE DIRECTORY FILES "/home/lingxiao/master/Sim2Real_py2/Sim2Real_py2/devel/share/gennodejs/ros/niryo_robot_msgs")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  execute_process(COMMAND "/usr/bin/python2" -m compileall "/home/lingxiao/master/Sim2Real_py2/Sim2Real_py2/devel/lib/python2.7/dist-packages/niryo_robot_msgs")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/python2.7/dist-packages" TYPE DIRECTORY FILES "/home/lingxiao/master/Sim2Real_py2/Sim2Real_py2/devel/lib/python2.7/dist-packages/niryo_robot_msgs")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/pkgconfig" TYPE FILE FILES "/home/lingxiao/master/Sim2Real_py2/Sim2Real_py2/build/niryo_robot_msgs/catkin_generated/installspace/niryo_robot_msgs.pc")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/niryo_robot_msgs/cmake" TYPE FILE FILES "/home/lingxiao/master/Sim2Real_py2/Sim2Real_py2/build/niryo_robot_msgs/catkin_generated/installspace/niryo_robot_msgs-msg-extras.cmake")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/niryo_robot_msgs/cmake" TYPE FILE FILES
    "/home/lingxiao/master/Sim2Real_py2/Sim2Real_py2/build/niryo_robot_msgs/catkin_generated/installspace/niryo_robot_msgsConfig.cmake"
    "/home/lingxiao/master/Sim2Real_py2/Sim2Real_py2/build/niryo_robot_msgs/catkin_generated/installspace/niryo_robot_msgsConfig-version.cmake"
    )
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/niryo_robot_msgs" TYPE FILE FILES "/home/lingxiao/master/Sim2Real_py2/Sim2Real_py2/src/niryo_robot_msgs/package.xml")
endif()

