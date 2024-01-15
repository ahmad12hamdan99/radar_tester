FROM osrf/ros:humble-desktop-full


RUN \
  apt update && \
  apt install -y nano

RUN apt-get update && apt-get install -y --no-install-recommends \
    python3.10 \
    python3-pip 
RUN \
  apt update && \
  apt install -y nano \
  wget curl


WORKDIR /home

RUN git clone https://github.com/ahmad12hamdan99/ars408_driver.git /home/radar_ws/src/ars408_driver/
RUN git clone https://github.com/ros-perception/radar_msgs.git /home/radar_ws/src/radar_msgs/
RUN git clone https://github.com/ahmad12hamdan99/radar_tester /home/radar_ws/src/radar_tester/
RUN git clone https://github.com/ros-industrial/ros2_canopen.git /home/radar_ws/src/ros2_canopen/
RUN rosdep install --from-paths radar_ws/src/ros2_canopen --ignore-src -r -y
RUN apt-get install can-utils


WORKDIR /home/radar_ws
RUN apt-get update
RUN . /opt/ros/humble/setup.sh \
    rosdep update && rosdep install --from-paths src --ignore-src -r -y \
    . /opt/ros/humble/setup.sh && colcon build --packages-select radar_msgs pe_ars408_ros radar_tester
