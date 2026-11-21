import cv2
import mediapipe as mp
import time
from pathlib import Path

class Camera:

    EYE_INDICES = [
        33, 133, 159, 145,
        362, 263, 386, 374
    ]

    POSTURE_INDICES = [
        0, 7, 8, 11, 12, 23, 24
    ]

    def __init__(self):

        base_dir = Path(__file__).resolve().parent

        pose_model = base_dir / "models" / "pose_landmarker_lite.task"
        face_model = base_dir / "models" / "face_landmarker.task"

        BaseOptions = mp.tasks.BaseOptions
        RunningMode = mp.tasks.vision.RunningMode

        pose_options = mp.tasks.vision.PoseLandmarkerOptions(
            base_options=BaseOptions(
                model_asset_path=str(pose_model)
            ),
            running_mode=RunningMode.VIDEO,
            num_poses=1
        )

        face_options = mp.tasks.vision.FaceLandmarkerOptions(
            base_options=BaseOptions(
                model_asset_path=str(face_model)
            ),
            running_mode=RunningMode.VIDEO,
            num_faces=1
        )

        self.pose_detector = (
            mp.tasks.vision.PoseLandmarker.create_from_options(
                pose_options
            )
        )

        self.face_detector = (
            mp.tasks.vision.FaceLandmarker.create_from_options(
                face_options
            )
        )

        self.cap = cv2.VideoCapture(0)

        if not self.cap.isOpened():
            self.pose_detector.close()
            self.face_detector.close()
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

        face_result = self.face_detector.detect_for_video(
            mp_image,
            timestamp_ms
        )

        # Extract eye landmarks
        eyes = None

        if face_result.face_landmarks:

            landmarks = face_result.face_landmarks[0]

            eyes = {
                i: (
                    landmarks[i].x,
                    landmarks[i].y,
                    landmarks[i].z
                )
                for i in self.EYE_INDICES
            }

        # Extract posture landmarks
        posture = None

        if pose_result.pose_landmarks:

            landmarks = pose_result.pose_landmarks[0]

            posture = {
                i: (
                    landmarks[i].x,
                    landmarks[i].y,
                    landmarks[i].z
                )
                for i in self.POSTURE_INDICES
            }

        return {
            "timestamp_ms": timestamp_ms,
            "eyes": eyes,
            "posture": posture
        }

    def close(self):
        self.cap.release()
        self.pose_detector.close()
        self.face_detector.close()