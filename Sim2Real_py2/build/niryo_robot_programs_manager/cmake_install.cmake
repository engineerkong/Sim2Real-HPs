# Install script for directory: /home/lingxiao/master/Sim2Real_py2/Sim2Real_py2/src/niryo_robot_programs_manager

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
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/niryo_robot_programs_manager/msg" TYPE FILE FILES
    "/home/lingxiao/master/Sim2Real_py2/Sim2Real_py2/src/niryo_robot_programs_manager/msg/ProgramIsRunning.msg"
    "/home/lingxiao/master/Sim2Real_py2/Sim2Real_py2/src/niryo_robot_programs_manager/msg/ProgramLanguage.msg"
    "/home/lingxiao/master/Sim2Real_py2/Sim2Real_py2/src/niryo_robot_programs_manager/msg/ProgramLanguageList.msg"
    "/home/lingxiao/master/Sim2Real_py2/Sim2Real_py2/src/niryo_robot_programs_manager/msg/ProgramList.msg"
    )
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/niryo_robot_programs_manager/srv" TYPE FILE FILES
    "/home/lingxiao/master/Sim2Real_py2/Sim2Real_py2/src/niryo_robot_programs_manager/srv/ExecuteProgram.srv"
    "/home/lingxiao/master/Sim2Real_py2/Sim2Real_py2/src/niryo_robot_programs_manager/srv/GetProgram.srv"
    "/home/lingxiao/master/Sim2Real_py2/Sim2Real_py2/src/niryo_robot_programs_manager/srv/GetProgramAutorunInfos.srv"
    "/home/lingxiao/master/Sim2Real_py2/Sim2Real_py2/src/niryo_robot_programs_manager/srv/GetProgramList.srv"
    "/home/lingxiao/master/Sim2Real_py2/Sim2Real_py2/src/niryo_robot_programs_manager/srv/ManageProgram.srv"
    "/home/lingxiao/master/Sim2Real_py2/Sim2Real_py2/src/niryo_robot_programs_manager/srv/SetProgramAutorun.srv"
    )
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  include("/home/lingxiao/master/Sim2Real_py2/Sim2Real_py2/build/niryo_robot_programs_manager/catkin_generated/safe_execute_install.cmake")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/niryo_robot_programs_manager/cmake" TYPE FILE FILES "/home/lingxiao/master/Sim2Real_py2/Sim2Real_py2/build/niryo_robot_programs_manager/catkin_generated/installspace/niryo_robot_programs_manager-msg-paths.cmake")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/include" TYPE DIRECTORY FILES "/home/lingxiao/master/Sim2Real_py2/Sim2Real_py2/devel/include/niryo_robot_programs_manager")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/roseus/ros" TYPE DIRECTORY FILES "/home/lingxiao/master/Sim2Real_py2/Sim2Real_py2/devel/share/roseus/ros/niryo_robot_programs_manager")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/common-lisp/ros" TYPE DIRECTORY FILES "/home/lingxiao/master/Sim2Real_py2/Sim2Real_py2/devel/share/common-lisp/ros/niryo_robot_programs_manager")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/gennodejs/ros" TYPE DIRECTORY FILES "/home/lingxiao/master/Sim2Real_py2/Sim2Real_py2/devel/share/gennodejs/ros/niryo_robot_programs_manager")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  execute_process(COMMAND "/usr/bin/python2" -m compileall "/home/lingxiao/master/Sim2Real_py2/Sim2Real_py2/devel/lib/python2.7/dist-packages/niryo_robot_programs_manager")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/python2.7/dist-packages" TYPE DIRECTORY FILES "/home/lingxiao/master/Sim2Real_py2/Sim2Real_py2/devel/lib/python2.7/dist-packages/niryo_robot_programs_manager" REGEX "/\\_\\_init\\_\\_\\.py$" EXCLUDE REGEX "/\\_\\_init\\_\\_\\.pyc$" EXCLUDE)
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/python2.7/dist-packages" TYPE DIRECTORY FILES "/home/lingxiao/master/Sim2Real_py2/Sim2Real_py2/devel/lib/python2.7/dist-packages/niryo_robot_programs_manager" FILES_MATCHING REGEX "/home/lingxiao/master/Sim2Real_py2/Sim2Real_py2/devel/lib/python2\\.7/dist-packages/niryo_robot_programs_manager/.+/__init__.pyc?$")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/pkgconfig" TYPE FILE FILES "/home/lingxiao/master/Sim2Real_py2/Sim2Real_py2/build/niryo_robot_programs_manager/catkin_generated/installspace/niryo_robot_programs_manager.pc")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/niryo_robot_programs_manager/cmake" TYPE FILE FILES "/home/lingxiao/master/Sim2Real_py2/Sim2Real_py2/build/niryo_robot_programs_manager/catkin_generated/installspace/niryo_robot_programs_manager-msg-extras.cmake")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/niryo_robot_programs_manager/cmake" TYPE FILE FILES
    "/home/lingxiao/master/Sim2Real_py2/Sim2Real_py2/build/niryo_robot_programs_manager/catkin_generated/installspace/niryo_robot_programs_managerConfig.cmake"
    "/home/lingxiao/master/Sim2Real_py2/Sim2Real_py2/build/niryo_robot_programs_manager/catkin_generated/installspace/niryo_robot_programs_managerConfig-version.cmake"
    )
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/niryo_robot_programs_manager" TYPE FILE FILES "/home/lingxiao/master/Sim2Real_py2/Sim2Real_py2/src/niryo_robot_programs_manager/package.xml")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/niryo_robot_programs_manager" TYPE PROGRAM FILES "/home/lingxiao/master/Sim2Real_py2/Sim2Real_py2/build/niryo_robot_programs_manager/catkin_generated/installspace/programs_manager_node.py")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/niryo_robot_programs_manager/launch" TYPE DIRECTORY FILES "/home/lingxiao/master/Sim2Real_py2/Sim2Real_py2/src/niryo_robot_programs_manager/launch/")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/niryo_robot_programs_manager/config" TYPE DIRECTORY FILES "/home/lingxiao/master/Sim2Real_py2/Sim2Real_py2/src/niryo_robot_programs_manager/config/")
endif()

