import os
import time
import cv2
from djitellopy import Tello

PIPE_PATH = "/tmp/tello_pipe"
TARGET_W, TARGET_H = 960, 720   # Tello typical usable size; matches ffmpeg scaling


def safe_open_pipe(path):
    """Open pipe only after a reader (ffmpeg) is connected."""
    while True:
        try:
            pipe = open(path, "wb")
            print("Pipe opened successfully (reader is connected).")
            return pipe
        except OSError:
            print("Pipe has no reader yet. Waiting for ffmpeg...")
            time.sleep(0.3)


def main():
    # Make sure named pipe exists
    if not os.path.exists(PIPE_PATH):
        raise SystemExit(f"Named pipe {PIPE_PATH} not found. Run: mkfifo {PIPE_PATH}")

    drone = Tello()
    print("Connecting to Tello...")
    drone.connect()
    print("Connected, turning stream on...")
    drone.streamon()

    fr = drone.get_frame_read()

    time.sleep(1.0)  # let frames start

    print(f"Waiting for ffmpeg to attach to pipe: {PIPE_PATH}")
    pipe = safe_open_pipe(PIPE_PATH)   # <-- FIXED

    try:
        while True:
            frame = fr.frame
            if frame is None:
                time.sleep(0.01)
                continue

            frame_resized = cv2.resize(frame, (TARGET_W, TARGET_H))

            ok, jpeg = cv2.imencode(".jpg", frame_resized)
            if not ok:
                continue

            try:
                pipe.write(jpeg.tobytes())
                pipe.flush()
            except BrokenPipeError:
                print("!! Broken pipe: ffmpeg closed. Waiting for it to reconnect...")
                pipe.close()
                pipe = safe_open_pipe(PIPE_PATH)
                continue

            # Optional preview
            cv2.imshow("Tello (writer)", frame_resized)
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

    except KeyboardInterrupt:
        print("Keyboard interrupt")
    finally:
        try:
            pipe.close()
        except:
            pass

        cv2.destroyAllWindows()
        drone.end()
        print("Shutdown complete")


if __name__ == "__main__":
    main()
