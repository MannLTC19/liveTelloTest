# liveTelloTest: Real-Time ORB-SLAM2 for DJI Tello

**liveTelloTest** is a project that bridges the **DJI Tello** drone with the **ORB-SLAM2** system. It allows for real-time monocular SLAM (Simultaneous Localization and Mapping) by feeding the drone's live video stream directly into a C++ SLAM backend wrapped for Python.

This repository includes the necessary bindings to run ORB-SLAM2 via Python, scripts to handle the Tello video feed reliably, and tools for trajectory accuracy analysis.

## 🌟 Features

* **Real-time SLAM:** Runs ORB-SLAM2 Monocular mode on live Tello video footage.
* **Python Bindings:** Custom C++ wrapper (`orbslam_runner.cpp`) using **Pybind11** to interface between Python logic and the ORB-SLAM2 C++ library.
* **Stream Stability:** Includes a "watchdog" mechanism in `liveTest.py` to automatically restart the video stream if frames stall.
* **Trajectory Evaluation:** Includes `calc.py` to calculate **WAPE** (Weighted Absolute Percentage Error) and Euclidean distance margins to evaluate tracking accuracy.
* **Video Piping:** `liveTelloViaPipe.py` allows streaming video to a named pipe (FIFO) for integration with other tools like FFmpeg.

## 📂 Project Structure

| File | Description |
| :--- | :--- |
| `liveTest.py` | **Main entry point.** Connects to Tello, initializes SLAM, and processes the video stream. |
| `orbslam_runner.cpp` | C++ source code creating the Python bindings for ORB-SLAM2. |
| `Tello.yaml` | Camera calibration parameters (Intrinsics/Distortion) for the Tello drone. |
| `calc.py` | Metrics script to calculate position/orientation errors (WAPE) from trajectory CSVs. |
| `liveTelloViaPipe.py` | Utility to write video frames to a named pipe (`/tmp/tello_pipe`). |
| `screencap.py` | Utility to capture screen regions (using `mss`). |

## 🛠️ Prerequisites

### Hardware
* **DJI Tello Drone**
* Computer with Wi-Fi (Linux recommended for ORB-SLAM2 compatibility)

### Software
* **Python 3.10+**
* **ORB-SLAM2** (You must have the library built and installed on your system)
* **Pangolin** (Viewer for ORB-SLAM2)
* **OpenCV** (C++ and Python)

### Python Dependencies
Install the required Python packages:
```bash
pip install djitellopy opencv-python pandas numpy pybind11 mss

⚙️ Installation & Setup
1. Compile the C++ Binding

Before running the Python scripts, you must compile orbslam_runner.cpp into a shared object (.so) file that Python can import.

Use the following command (adjust paths to your specific ORB-SLAM2 installation):
Bash

c++ -O3 -Wall -shared -std=c++11 -fPIC \
$(python3 -m pybind11 --includes) \
-I/path/to/ORB_SLAM2/include \
-I/path/to/ORB_SLAM2 \
orbslam_runner.cpp \
-L/path/to/ORB_SLAM2/lib -lORB_SLAM2 \
-lopencv_core -lopencv_imgproc -lopencv_highgui -lopencv_videoio \
-o orbslam_runner$(python3-config --extension-suffix)

Make sure the resulting .so file (e.g., orbslam_runner.cpython-310-x86_64-linux-gnu.so) is in the same directory as liveTest.py.
2. Configure Paths

Open liveTest.py and update the paths to point to your ORB-SLAM2 vocabulary and the Tello.yaml file included in this repo:
Python

# liveTest.py
ORB_VOCAB = "/path/to/YOUR/ORB_SLAM2/Vocabulary/ORBvoc.txt"
ORB_YAML  = "./Tello.yaml"

🚀 Usage
Running Real-Time SLAM

    Power on the Tello drone.

    Connect your computer to the Tello's Wi-Fi network (usually TELLO-XXXXXX).

    Run the main script:
    Bash

    python liveTest.py

        This will launch the Pangolin viewer showing the map and camera pose.

        The drone video stream is processed in real-time.

Evaluating Trajectory Data

If you have a CSV file containing trajectory data (Actual vs Forecast), you can generate error metrics:

    Open calc.py and set the file_name variable to your CSV file path.

    Run the script:
    Bash

    python calc.py

        This generates WAPE_Analysis_Results.csv and Difference_Margins.csv.

🔧 Troubleshooting

    "Frame stalled - restarting stream": The script detects if the video feed freezes and attempts to restart it. If this happens frequently, check for Wi-Fi interference.

    ImportError: No module named 'orbslam_runner': Ensure the .so file is compiled for the exact version of Python you are running.

    Segmentation Fault: This often occurs due to mismatches between the OpenCV version used by ORB-SLAM2 (C++) and the opencv-python library. Ensure they are compatible (preferably the same major version).

Created for the Live Tello SLAM Project.
