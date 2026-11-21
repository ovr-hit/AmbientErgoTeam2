import cv2
import mediapipe as mp
import time
from pathlib import Path


class Camera:
    POSTURE_LANDMARKS = {
        "nose": 0,
        "left_ear": 7,
        "right_ear": 8,
        "left_shoulder": 11,
        "right_shoulder": 12,
        "left_hip": 23,
        "right_hip": 24
    }

    def __init__(self, camera_index=0):

        base_dir = Path(__file__).resolve().parent
        pose_model = base_dir / "models" / "pose_landmarker_lite.task"

        if not pose_model.exists():
            raise FileNotFoundError(
                f"Pose model not found: {pose_model}"
            )

        BaseOptions = mp.tasks.BaseOptions
        RunningMode = mp.tasks.vision.RunningMode
        pose_options = mp.tasks.vision.PoseLandmarkerOptions(
            base_options=BaseOptions(
                model_asset_path=str(pose_model)
            ),
            running_mode=RunningMode.VIDEO,
            num_poses=1
        )

        self.pose_detector = (
            mp.tasks.vision.PoseLandmarker.create_from_options(
                pose_options
            )
        )

        self.cap = cv2.VideoCapture(camera_index)

        if not self.cap.isOpened():
            self.cap.release()
            self.pose_detector.close()
            raise RuntimeError("Could not open webcam")

        self.start_time = time.monotonic()
        self.last_timestamp_ms = -1

    def get_data(self):

        success, frame = self.cap.read()

        if not success: 
            return None

        frame = cv2.flip(frame, 1)

        rgb_frame = cv2.cvtColor(
            frame,
            cv2.COLOR_BGR2RGB
        )

        mp_image = mp.Image(
            image_format=mp.ImageFormat.SRGB,
            data=rgb_frame
        )

        timestamp_ms = int(
            (time.monotonic() - self.start_time) * 1000
        )

        timestamp_ms = max(
            timestamp_ms,
            self.last_timestamp_ms + 1
        )

        self.last_timestamp_ms = timestamp_ms

        pose_result = self.pose_detector.detect_for_video(
            mp_image,
            timestamp_ms
        )

        posture = None

        if pose_result.pose_landmarks:

            landmarks = pose_result.pose_landmarks[0]

            posture = {
                name: {
                    "x": landmarks[index].x,
                    "y": landmarks[index].y,
                    "z": landmarks[index].z,
                    "visibility": landmarks[index].visibility
                }
                for name, index in self.POSTURE_LANDMARKS.items()
            }

        return {
            "timestamp_ms": timestamp_ms,
            "posture": posture
        }

    def close(self):
        self.cap.release()
        self.pose_detector.close()