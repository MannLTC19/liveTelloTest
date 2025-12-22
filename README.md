#liveTelloTest: ORB-SLAM2 for DJI Tello

liveTelloTest is a real-time Simultaneous Localization and Mapping (SLAM) implementation for the DJI Tello drone. It bridges high-performance C++ SLAM (ORB-SLAM2) with Python-based drone control (djitellopy) using Pybind11.

This project allows you to stream live video from a Tello drone, feed it directly into the ORB-SLAM2 system, and visualize the camera trajectory and sparse point cloud in real-time using Pangolin.
🌟 Features

    Real-time SLAM: Runs ORB-SLAM2 Monocular mode on the Tello's video feed.

Python/C++ Integration: Custom ORBSLAMRunner C++ class wrapped for Python using Pybind11 for efficient image processing.

Live Stream Handling: Includes "watchdog" logic to restart the video stream if frames stall.

Evaluation Tools: Includes calc.py to calculate Weighted Absolute Percentage Error (WAPE) and trajectory difference margins for accuracy analysis.

Alternative Streaming: Includes liveTelloViaPipe.py to stream video to a named pipe (useful for FFmpeg integration).

🛠️ Prerequisites

    OS: Linux (Tested on Ubuntu/Debian based systems)

    Python: 3.x

    C++ Libraries:

        ORB-SLAM2 (Built and installed)

        Pangolin (Required by ORB-SLAM2)

        OpenCV (C++ and Python versions)

        Eigen3

    Python Libraries:
    Bash

    pip install djitellopy opencv-python pandas numpy pybind11

📦 Installation & Build

Since this project uses a C++ extension for SLAM, you must compile the orbslam_runner module before running the Python scripts.

    Clone the repository:
    Bash

git clone https://github.com/MannLTC19/liveTelloTest.git
cd liveTelloTest

Compile the C++ Binding: You need to compile orbslam_runner.cpp into a shared object (.so) file. Ensure you have the ORB-SLAM2 source code available.

Example CMake approach (create a CMakeLists.txt or use g++ directly):
Bash

# Example g++ command (adjust paths to your ORB_SLAM2 installation)
c++ -O3 -Wall -shared -std=c++11 -fPIC \
$(python3 -m pybind11 --includes) \
-I/path/to/ORB_SLAM2/include \
-I/path/to/ORB_SLAM2 \
orbslam_runner.cpp \
-L/path/to/ORB_SLAM2/lib -lORB_SLAM2 \
-lopencv_core -lopencv_imgproc -lopencv_highgui -lopencv_videoio \
-o orbslam_runner$(python3-config --extension-suffix)

Ensure the resulting .so file is in the same directory as liveTest.py.

Configure Paths: Edit liveTest.py (or liveTest1.py) to point to your specific ORB-SLAM2 vocabulary and calibration files:
Python

    # Inside liveTest.py
    ORB_VOCAB = "/path/to/ORB_SLAM2/Vocabulary/ORBvoc.txt"
    ORB_YAML  = "./Tello.yaml" 

🚀 Usage
1. Run Real-time SLAM

Connect your computer to the Tello's Wi-Fi and run:
Bash

python liveTest.py

This will:

    Connect to the Tello drone.

Start the video stream.

Launch the Pangolin viewer (from ORB-SLAM2) to show the map and drone pose.

2. Camera Calibration (Tello.yaml)

The file Tello.yaml contains the intrinsic parameters for the Tello camera. If you change the resolution in the script (default 960x720), update this file accordingly.

YAML

Camera.width: 960
Camera.height: 720
Camera.fx: 920.0
# ...

3. Trajectory Analysis

If you have saved trajectory data (CSV), you can use calc.py to compare actual vs. forecast positions:
Bash

python calc.py

Note: Update the file_name variable in calc.py to match your data file.

📂 Project Structure

    liveTest.py: Main script for running SLAM with Tello.

    orbslam_runner.cpp: C++ source for the Python wrapper.

    Tello.yaml: Calibration file for ORB-SLAM2.

    calc.py: Script for calculating WAPE and position error metrics.

    liveTelloViaPipe.py: Utility to push Tello video to a named system pipe.

    screencap.py: Utility for capturing screen regions (using mss).

⚠️ Troubleshooting

    "Frame stalled": The script includes a watchdog that attempts to restart the stream if frames are lost. Ensure Wi-Fi interference is minimal.

Shared Object Error: If Python cannot import orbslam_runner, ensure the .so file was compiled for the exact Python version you are using.
