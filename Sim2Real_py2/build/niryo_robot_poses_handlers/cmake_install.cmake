# Install script for directory: /home/lingxiao/master/Sim2Real_py2/Sim2Real_py2/src/niryo_robot_poses_handlers

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
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/niryo_robot_poses_handlers/msg" TYPE FILE FILES
    "/home/lingxiao/master/Sim2Real_py2/Sim2Real_py2/src/niryo_robot_poses_handlers/msg/DynamicFrame.msg"
    "/home/lingxiao/master/Sim2Real_py2/Sim2Real_py2/src/niryo_robot_poses_handlers/msg/NiryoPose.msg"
    "/home/lingxiao/master/Sim2Real_py2/Sim2Real_py2/src/niryo_robot_poses_handlers/msg/Workspace.msg"
    )
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/niryo_robot_poses_handlers/srv" TYPE FILE FILES
    "/home/lingxiao/master/Sim2Real_py2/Sim2Real_py2/src/niryo_robot_poses_handlers/srv/GetDynamicFrame.srv"
    "/home/lingxiao/master/Sim2Real_py2/Sim2Real_py2/src/niryo_robot_poses_handlers/srv/GetPose.srv"
    "/home/lingxiao/master/Sim2Real_py2/Sim2Real_py2/src/niryo_robot_poses_handlers/srv/GetTargetPose.srv"
    "/home/lingxiao/master/Sim2Real_py2/Sim2Real_py2/src/niryo_robot_poses_handlers/srv/GetTransformPose.srv"
    "/home/lingxiao/master/Sim2Real_py2/Sim2Real_py2/src/niryo_robot_poses_handlers/srv/GetWorkspaceMatrixPoses.srv"
    "/home/lingxiao/master/Sim2Real_py2/Sim2Real_py2/src/niryo_robot_poses_handlers/srv/GetWorkspacePoints.srv"
    "/home/lingxiao/master/Sim2Real_py2/Sim2Real_py2/src/niryo_robot_poses_handlers/srv/GetWorkspaceRatio.srv"
    "/home/lingxiao/master/Sim2Real_py2/Sim2Real_py2/src/niryo_robot_poses_handlers/srv/GetWorkspaceRobotPoses.srv"
    "/home/lingxiao/master/Sim2Real_py2/Sim2Real_py2/src/niryo_robot_poses_handlers/srv/ManageDynamicFrame.srv"
    "/home/lingxiao/master/Sim2Real_py2/Sim2Real_py2/src/niryo_robot_poses_handlers/srv/ManagePose.srv"
    "/home/lingxiao/master/Sim2Real_py2/Sim2Real_py2/src/niryo_robot_poses_handlers/srv/ManageWorkspace.srv"
    )
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  include("/home/lingxiao/master/Sim2Real_py2/Sim2Real_py2/build/niryo_robot_poses_handlers/catkin_generated/safe_execute_install.cmake")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/niryo_robot_poses_handlers/cmake" TYPE FILE FILES "/home/lingxiao/master/Sim2Real_py2/Sim2Real_py2/build/niryo_robot_poses_handlers/catkin_generated/installspace/niryo_robot_poses_handlers-msg-paths.cmake")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/include" TYPE DIRECTORY FILES "/home/lingxiao/master/Sim2Real_py2/Sim2Real_py2/devel/include/niryo_robot_poses_handlers")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/roseus/ros" TYPE DIRECTORY FILES "/home/lingxiao/master/Sim2Real_py2/Sim2Real_py2/devel/share/roseus/ros/niryo_robot_poses_handlers")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/common-lisp/ros" TYPE DIRECTORY FILES "/home/lingxiao/master/Sim2Real_py2/Sim2Real_py2/devel/share/common-lisp/ros/niryo_robot_poses_handlers")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/gennodejs/ros" TYPE DIRECTORY FILES "/home/lingxiao/master/Sim2Real_py2/Sim2Real_py2/devel/share/gennodejs/ros/niryo_robot_poses_handlers")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  execute_process(COMMAND "/usr/bin/python2" -m compileall "/home/lingxiao/master/Sim2Real_py2/Sim2Real_py2/devel/lib/python2.7/dist-packages/niryo_robot_poses_handlers")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/python2.7/dist-packages" TYPE DIRECTORY FILES "/home/lingxiao/master/Sim2Real_py2/Sim2Real_py2/devel/lib/python2.7/dist-packages/niryo_robot_poses_handlers" REGEX "/\\_\\_init\\_\\_\\.py$" EXCLUDE REGEX "/\\_\\_init\\_\\_\\.pyc$" EXCLUDE)
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/python2.7/dist-packages" TYPE DIRECTORY FILES "/home/lingxiao/master/Sim2Real_py2/Sim2Real_py2/devel/lib/python2.7/dist-packages/niryo_robot_poses_handlers" FILES_MATCHING REGEX "/home/lingxiao/master/Sim2Real_py2/Sim2Real_py2/devel/lib/python2\\.7/dist-packages/niryo_robot_poses_handlers/.+/__init__.pyc?$")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/pkgconfig" TYPE FILE FILES "/home/lingxiao/master/Sim2Real_py2/Sim2Real_py2/build/niryo_robot_poses_handlers/catkin_generated/installspace/niryo_robot_poses_handlers.pc")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/niryo_robot_poses_handlers/cmake" TYPE FILE FILES "/home/lingxiao/master/Sim2Real_py2/Sim2Real_py2/build/niryo_robot_poses_handlers/catkin_generated/installspace/niryo_robot_poses_handlers-msg-extras.cmake")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/niryo_robot_poses_handlers/cmake" TYPE FILE FILES
    "/home/lingxiao/master/Sim2Real_py2/Sim2Real_py2/build/niryo_robot_poses_handlers/catkin_generated/installspace/niryo_robot_poses_handlersConfig.cmake"
    "/home/lingxiao/master/Sim2Real_py2/Sim2Real_py2/build/niryo_robot_poses_handlers/catkin_generated/installspace/niryo_robot_poses_handlersConfig-version.cmake"
    )
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/niryo_robot_poses_handlers" TYPE FILE FILES "/home/lingxiao/master/Sim2Real_py2/Sim2Real_py2/src/niryo_robot_poses_handlers/package.xml")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/niryo_robot_poses_handlers" TYPE PROGRAM FILES "/home/lingxiao/master/Sim2Real_py2/Sim2Real_py2/build/niryo_robot_poses_handlers/catkin_generated/installspace/poses_handlers_node.py")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/niryo_robot_poses_handlers" TYPE PROGRAM FILES "/home/lingxiao/master/Sim2Real_py2/Sim2Real_py2/build/niryo_robot_poses_handlers/catkin_generated/installspace/transform_handler.py")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/niryo_robot_poses_handlers" TYPE PROGRAM FILES "/home/lingxiao/master/Sim2Real_py2/Sim2Real_py2/build/niryo_robot_poses_handlers/catkin_generated/installspace/poses_handlers_node.py")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/niryo_robot_poses_handlers/grips" TYPE DIRECTORY FILES "/home/lingxiao/master/Sim2Real_py2/Sim2Real_py2/src/niryo_robot_poses_handlers/grips/")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/niryo_robot_poses_handlers/config" TYPE DIRECTORY FILES "/home/lingxiao/master/Sim2Real_py2/Sim2Real_py2/src/niryo_robot_poses_handlers/config/")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/niryo_robot_poses_handlers/launch" TYPE DIRECTORY FILES "/home/lingxiao/master/Sim2Real_py2/Sim2Real_py2/src/niryo_robot_poses_handlers/launch/")
endif()

