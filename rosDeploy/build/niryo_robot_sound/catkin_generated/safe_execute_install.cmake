execute_process(COMMAND "/home/lingxiao/master/github/ros_deploy/Sim2Real-HPs/rosDeploy/build/niryo_robot_sound/catkin_generated/python_distutils_install.sh" RESULT_VARIABLE res)

if(NOT res EQUAL 0)
  message(FATAL_ERROR "execute_process(/home/lingxiao/master/github/ros_deploy/Sim2Real-HPs/rosDeploy/build/niryo_robot_sound/catkin_generated/python_distutils_install.sh) returned error code ")
endif()