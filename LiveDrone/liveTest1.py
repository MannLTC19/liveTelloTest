import time
import cv2
from djitellopy import Tello
from orbslam_runner import ORBSLAMRunner
import threading


# ORB-SLAM2 paths
ORB_VOCAB = "/home/necroid/ORB_SLAM2/Vocabulary/ORBvoc.txt"
ORB_YAML  = "/home/necroid/ORB_SLAM2/Examples/Monocular/Tello1.yaml"

# Tello safe stream
def safe_stream_on(drone):
    """
    Ensure the drone stream is on and avoid duplicate streams.
    """
    try:
        drone.streamoff()
    except Exception:
        pass
    time.sleep(0.5)
    drone.streamon()
    time.sleep(2.0)  # allow buffer to fill

# Optional: OpenCV preview thread
#def preview_thread(frame_reader, stop_flag):
    #while not stop_flag[0]:
        #frame = frame_reader.frame
        #if frame is not None:
            #cv2.imshow("Tello Preview", frame)
        #if cv2.waitKey(1) & 0xFF == 27:
            #stop_flag[0] = True
        #time.sleep(0.001)
    #cv2.destroyAllWindows()

# Main
def main():
    # Initialize ORB-SLAM2 with Pangolin viewer enabled
    slam = ORBSLAMRunner(
        ORB_VOCAB,
        ORB_YAML,
        use_viewer=True  
    )

    # Initialize Tello
    drone = Tello()
    try:
        drone.connect()
    except Exception as e:
        print(f"[ERROR] Could not connect to Tello: {e}")
        return

    safe_stream_on(drone)
    fr = drone.get_frame_read()

    # Start optional OpenCV preview in separate thread
    #stop_flag = [False]
    #preview = threading.Thread(target=preview_thread, args=(fr, stop_flag))
    #preview.start()
    stop_flag = [False]

    start_time = time.monotonic()

    try:
        while not stop_flag[0]:
            frame = fr.frame

            # Stream watchdog
            if frame is None:
                print("[WARN] Frame stalled — restarting stream")
                safe_stream_on(drone)
                continue

            # Convert to grayscale
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            # SLAM timestamp
            timestamp = time.monotonic() - start_time

            # Process SLAM
            try:
                slam.process(gray, timestamp)
            except Exception as e:
                print(f"[WARN] SLAM process error: {e}")

            # Yield CPU
            time.sleep(0.001)

    except KeyboardInterrupt:
        print("[INFO] Interrupted by user")

    finally:
        stop_flag[0] = True
        #preview.join()
        slam.shutdown()
        drone.end()
        print("[INFO] Shutdown complete")

if __name__ == "__main__":
    main()
