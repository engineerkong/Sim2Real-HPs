#!/bin/sh

if [ -n "$DESTDIR" ] ; then
    case $DESTDIR in
        /*) # ok
            ;;
        *)
            /bin/echo "DESTDIR argument must be absolute... "
            /bin/echo "otherwise python's distutils will bork things."
            exit 1
    esac
fi

echo_and_run() { echo "+ $@" ; "$@" ; }

echo_and_run cd "/home/lingxiao/master/github/ros_deploy/Sim2Real-HPs/rosDeploy/src/niryo_robot_vision"

# ensure that Python install destination exists
echo_and_run mkdir -p "$DESTDIR/home/lingxiao/master/github/ros_deploy/Sim2Real-HPs/rosDeploy/install/lib/python2.7/dist-packages"

# Note that PYTHONPATH is pulled from the environment to support installing
# into one location when some dependencies were installed in another
# location, #123.
echo_and_run /usr/bin/env \
    PYTHONPATH="/home/lingxiao/master/github/ros_deploy/Sim2Real-HPs/rosDeploy/install/lib/python2.7/dist-packages:/home/lingxiao/master/github/ros_deploy/Sim2Real-HPs/rosDeploy/build/lib/python2.7/dist-packages:$PYTHONPATH" \
    CATKIN_BINARY_DIR="/home/lingxiao/master/github/ros_deploy/Sim2Real-HPs/rosDeploy/build" \
    "/usr/bin/python2" \
    "/home/lingxiao/master/github/ros_deploy/Sim2Real-HPs/rosDeploy/src/niryo_robot_vision/setup.py" \
    egg_info --egg-base /home/lingxiao/master/github/ros_deploy/Sim2Real-HPs/rosDeploy/build/niryo_robot_vision \
    build --build-base "/home/lingxiao/master/github/ros_deploy/Sim2Real-HPs/rosDeploy/build/niryo_robot_vision" \
    install \
    --root="${DESTDIR-/}" \
    --install-layout=deb --prefix="/home/lingxiao/master/github/ros_deploy/Sim2Real-HPs/rosDeploy/install" --install-scripts="/home/lingxiao/master/github/ros_deploy/Sim2Real-HPs/rosDeploy/install/bin"
