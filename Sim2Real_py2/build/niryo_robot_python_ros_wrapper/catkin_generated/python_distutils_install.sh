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

echo_and_run cd "/home/lingxiao/master/Sim2Real_py2/Sim2Real_py2/src/niryo_robot_python_ros_wrapper"

# ensure that Python install destination exists
echo_and_run mkdir -p "$DESTDIR/home/lingxiao/master/Sim2Real_py2/Sim2Real_py2/install/lib/python2.7/dist-packages"

# Note that PYTHONPATH is pulled from the environment to support installing
# into one location when some dependencies were installed in another
# location, #123.
echo_and_run /usr/bin/env \
    PYTHONPATH="/home/lingxiao/master/Sim2Real_py2/Sim2Real_py2/install/lib/python2.7/dist-packages:/home/lingxiao/master/Sim2Real_py2/Sim2Real_py2/build/lib/python2.7/dist-packages:$PYTHONPATH" \
    CATKIN_BINARY_DIR="/home/lingxiao/master/Sim2Real_py2/Sim2Real_py2/build" \
    "/usr/bin/python2" \
    "/home/lingxiao/master/Sim2Real_py2/Sim2Real_py2/src/niryo_robot_python_ros_wrapper/setup.py" \
    egg_info --egg-base /home/lingxiao/master/Sim2Real_py2/Sim2Real_py2/build/niryo_robot_python_ros_wrapper \
    build --build-base "/home/lingxiao/master/Sim2Real_py2/Sim2Real_py2/build/niryo_robot_python_ros_wrapper" \
    install \
    --root="${DESTDIR-/}" \
    --install-layout=deb --prefix="/home/lingxiao/master/Sim2Real_py2/Sim2Real_py2/install" --install-scripts="/home/lingxiao/master/Sim2Real_py2/Sim2Real_py2/install/bin"
