# Install script for directory: /home/lingxiao/master/github/ros_deploy/Sim2Real-HPs/rosDeploy/src/niryo_robot_reports

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
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/niryo_robot_reports/msg" TYPE FILE FILES "/home/lingxiao/master/github/ros_deploy/Sim2Real-HPs/rosDeploy/src/niryo_robot_reports/msg/Service.msg")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/niryo_robot_reports/srv" TYPE FILE FILES
    "/home/lingxiao/master/github/ros_deploy/Sim2Real-HPs/rosDeploy/src/niryo_robot_reports/srv/CheckConnection.srv"
    "/home/lingxiao/master/github/ros_deploy/Sim2Real-HPs/rosDeploy/src/niryo_robot_reports/srv/RunAutoDiagnosis.srv"
    )
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  include("/home/lingxiao/master/github/ros_deploy/Sim2Real-HPs/rosDeploy/build/niryo_robot_reports/catkin_generated/safe_execute_install.cmake")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/niryo_robot_reports/cmake" TYPE FILE FILES "/home/lingxiao/master/github/ros_deploy/Sim2Real-HPs/rosDeploy/build/niryo_robot_reports/catkin_generated/installspace/niryo_robot_reports-msg-paths.cmake")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/include" TYPE DIRECTORY FILES "/home/lingxiao/master/github/ros_deploy/Sim2Real-HPs/rosDeploy/devel/include/niryo_robot_reports")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/roseus/ros" TYPE DIRECTORY FILES "/home/lingxiao/master/github/ros_deploy/Sim2Real-HPs/rosDeploy/devel/share/roseus/ros/niryo_robot_reports")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/common-lisp/ros" TYPE DIRECTORY FILES "/home/lingxiao/master/github/ros_deploy/Sim2Real-HPs/rosDeploy/devel/share/common-lisp/ros/niryo_robot_reports")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/gennodejs/ros" TYPE DIRECTORY FILES "/home/lingxiao/master/github/ros_deploy/Sim2Real-HPs/rosDeploy/devel/share/gennodejs/ros/niryo_robot_reports")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  execute_process(COMMAND "/usr/bin/python2" -m compileall "/home/lingxiao/master/github/ros_deploy/Sim2Real-HPs/rosDeploy/devel/lib/python2.7/dist-packages/niryo_robot_reports")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/python2.7/dist-packages" TYPE DIRECTORY FILES "/home/lingxiao/master/github/ros_deploy/Sim2Real-HPs/rosDeploy/devel/lib/python2.7/dist-packages/niryo_robot_reports" REGEX "/\\_\\_init\\_\\_\\.py$" EXCLUDE REGEX "/\\_\\_init\\_\\_\\.pyc$" EXCLUDE)
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/python2.7/dist-packages" TYPE DIRECTORY FILES "/home/lingxiao/master/github/ros_deploy/Sim2Real-HPs/rosDeploy/devel/lib/python2.7/dist-packages/niryo_robot_reports" FILES_MATCHING REGEX "/home/lingxiao/master/github/ros_deploy/Sim2Real-HPs/rosDeploy/devel/lib/python2\\.7/dist-packages/niryo_robot_reports/.+/__init__.pyc?$")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/pkgconfig" TYPE FILE FILES "/home/lingxiao/master/github/ros_deploy/Sim2Real-HPs/rosDeploy/build/niryo_robot_reports/catkin_generated/installspace/niryo_robot_reports.pc")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/niryo_robot_reports/cmake" TYPE FILE FILES "/home/lingxiao/master/github/ros_deploy/Sim2Real-HPs/rosDeploy/build/niryo_robot_reports/catkin_generated/installspace/niryo_robot_reports-msg-extras.cmake")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/niryo_robot_reports/cmake" TYPE FILE FILES
    "/home/lingxiao/master/github/ros_deploy/Sim2Real-HPs/rosDeploy/build/niryo_robot_reports/catkin_generated/installspace/niryo_robot_reportsConfig.cmake"
    "/home/lingxiao/master/github/ros_deploy/Sim2Real-HPs/rosDeploy/build/niryo_robot_reports/catkin_generated/installspace/niryo_robot_reportsConfig-version.cmake"
    )
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/niryo_robot_reports" TYPE FILE FILES "/home/lingxiao/master/github/ros_deploy/Sim2Real-HPs/rosDeploy/src/niryo_robot_reports/package.xml")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/niryo_robot_reports" TYPE PROGRAM FILES "/home/lingxiao/master/github/ros_deploy/Sim2Real-HPs/rosDeploy/build/niryo_robot_reports/catkin_generated/installspace/reports_node.py")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/niryo_robot_reports" TYPE PROGRAM FILES "/home/lingxiao/master/github/ros_deploy/Sim2Real-HPs/rosDeploy/build/niryo_robot_reports/catkin_generated/installspace/auto_diagnosis.py")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/niryo_robot_reports/scripts" TYPE PROGRAM FILES "/home/lingxiao/master/github/ros_deploy/Sim2Real-HPs/rosDeploy/src/niryo_robot_reports/pub_new_day.sh")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/niryo_robot_reports/scripts" TYPE PROGRAM FILES
    "/home/lingxiao/master/github/ros_deploy/Sim2Real-HPs/rosDeploy/src/niryo_robot_reports/pub_new_day.sh"
    "/home/lingxiao/master/github/ros_deploy/Sim2Real-HPs/rosDeploy/src/niryo_robot_reports/scripts/auto_diagnosis.py"
    )
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/niryo_robot_reports/launch" TYPE DIRECTORY FILES "/home/lingxiao/master/github/ros_deploy/Sim2Real-HPs/rosDeploy/src/niryo_robot_reports/launch/")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/niryo_robot_reports/config" TYPE DIRECTORY FILES "/home/lingxiao/master/github/ros_deploy/Sim2Real-HPs/rosDeploy/src/niryo_robot_reports/config/")
endif()

