# Install script for directory: /home/lingxiao/master/Sim2Real_py2/Sim2Real_py2/src/niryo_robot_hardware_stack/conveyor_interface

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
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/conveyor_interface/msg" TYPE FILE FILES
    "/home/lingxiao/master/Sim2Real_py2/Sim2Real_py2/src/niryo_robot_hardware_stack/conveyor_interface/msg/ConveyorFeedback.msg"
    "/home/lingxiao/master/Sim2Real_py2/Sim2Real_py2/src/niryo_robot_hardware_stack/conveyor_interface/msg/ConveyorFeedbackArray.msg"
    )
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/conveyor_interface/srv" TYPE FILE FILES
    "/home/lingxiao/master/Sim2Real_py2/Sim2Real_py2/src/niryo_robot_hardware_stack/conveyor_interface/srv/ControlConveyor.srv"
    "/home/lingxiao/master/Sim2Real_py2/Sim2Real_py2/src/niryo_robot_hardware_stack/conveyor_interface/srv/SetConveyor.srv"
    )
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/conveyor_interface/cmake" TYPE FILE FILES "/home/lingxiao/master/Sim2Real_py2/Sim2Real_py2/build/niryo_robot_hardware_stack/conveyor_interface/catkin_generated/installspace/conveyor_interface-msg-paths.cmake")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/include" TYPE DIRECTORY FILES "/home/lingxiao/master/Sim2Real_py2/Sim2Real_py2/devel/include/conveyor_interface")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/roseus/ros" TYPE DIRECTORY FILES "/home/lingxiao/master/Sim2Real_py2/Sim2Real_py2/devel/share/roseus/ros/conveyor_interface")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/common-lisp/ros" TYPE DIRECTORY FILES "/home/lingxiao/master/Sim2Real_py2/Sim2Real_py2/devel/share/common-lisp/ros/conveyor_interface")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/gennodejs/ros" TYPE DIRECTORY FILES "/home/lingxiao/master/Sim2Real_py2/Sim2Real_py2/devel/share/gennodejs/ros/conveyor_interface")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  execute_process(COMMAND "/usr/bin/python2" -m compileall "/home/lingxiao/master/Sim2Real_py2/Sim2Real_py2/devel/lib/python2.7/dist-packages/conveyor_interface")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/python2.7/dist-packages" TYPE DIRECTORY FILES "/home/lingxiao/master/Sim2Real_py2/Sim2Real_py2/devel/lib/python2.7/dist-packages/conveyor_interface")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/pkgconfig" TYPE FILE FILES "/home/lingxiao/master/Sim2Real_py2/Sim2Real_py2/build/niryo_robot_hardware_stack/conveyor_interface/catkin_generated/installspace/conveyor_interface.pc")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/conveyor_interface/cmake" TYPE FILE FILES "/home/lingxiao/master/Sim2Real_py2/Sim2Real_py2/build/niryo_robot_hardware_stack/conveyor_interface/catkin_generated/installspace/conveyor_interface-msg-extras.cmake")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/conveyor_interface/cmake" TYPE FILE FILES
    "/home/lingxiao/master/Sim2Real_py2/Sim2Real_py2/build/niryo_robot_hardware_stack/conveyor_interface/catkin_generated/installspace/conveyor_interfaceConfig.cmake"
    "/home/lingxiao/master/Sim2Real_py2/Sim2Real_py2/build/niryo_robot_hardware_stack/conveyor_interface/catkin_generated/installspace/conveyor_interfaceConfig-version.cmake"
    )
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/conveyor_interface" TYPE FILE FILES "/home/lingxiao/master/Sim2Real_py2/Sim2Real_py2/src/niryo_robot_hardware_stack/conveyor_interface/package.xml")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  if(EXISTS "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/libconveyor_interface.so" AND
     NOT IS_SYMLINK "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/libconveyor_interface.so")
    file(RPATH_CHECK
         FILE "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/libconveyor_interface.so"
         RPATH "")
  endif()
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib" TYPE SHARED_LIBRARY FILES "/home/lingxiao/master/Sim2Real_py2/Sim2Real_py2/devel/lib/libconveyor_interface.so")
  if(EXISTS "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/libconveyor_interface.so" AND
     NOT IS_SYMLINK "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/libconveyor_interface.so")
    file(RPATH_CHANGE
         FILE "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/libconveyor_interface.so"
         OLD_RPATH "/home/lingxiao/master/Sim2Real_py2/Sim2Real_py2/devel/lib:/opt/ros/melodic/lib:"
         NEW_RPATH "")
    if(CMAKE_INSTALL_DO_STRIP)
      execute_process(COMMAND "/usr/bin/strip" "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/libconveyor_interface.so")
    endif()
  endif()
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  if(EXISTS "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/conveyor_interface/conveyor_interface_node" AND
     NOT IS_SYMLINK "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/conveyor_interface/conveyor_interface_node")
    file(RPATH_CHECK
         FILE "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/conveyor_interface/conveyor_interface_node"
         RPATH "")
  endif()
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/conveyor_interface" TYPE EXECUTABLE FILES "/home/lingxiao/master/Sim2Real_py2/Sim2Real_py2/devel/lib/conveyor_interface/conveyor_interface_node")
  if(EXISTS "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/conveyor_interface/conveyor_interface_node" AND
     NOT IS_SYMLINK "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/conveyor_interface/conveyor_interface_node")
    file(RPATH_CHANGE
         FILE "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/conveyor_interface/conveyor_interface_node"
         OLD_RPATH "/home/lingxiao/master/Sim2Real_py2/Sim2Real_py2/devel/lib:/opt/ros/melodic/lib:"
         NEW_RPATH "")
    if(CMAKE_INSTALL_DO_STRIP)
      execute_process(COMMAND "/usr/bin/strip" "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/conveyor_interface/conveyor_interface_node")
    endif()
  endif()
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/include/conveyor_interface" TYPE DIRECTORY FILES "/home/lingxiao/master/Sim2Real_py2/Sim2Real_py2/src/niryo_robot_hardware_stack/conveyor_interface/include/conveyor_interface/")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/conveyor_interface/launch" TYPE DIRECTORY FILES "/home/lingxiao/master/Sim2Real_py2/Sim2Real_py2/src/niryo_robot_hardware_stack/conveyor_interface/launch/")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/conveyor_interface/config" TYPE DIRECTORY FILES "/home/lingxiao/master/Sim2Real_py2/Sim2Real_py2/src/niryo_robot_hardware_stack/conveyor_interface/config/")
endif()

