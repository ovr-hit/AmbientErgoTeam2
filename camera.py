import cv2
import mediapipe as mp
import time
from pathlib import Path

# ==========================================
# MODEL PATHS
# ==========================================

BASE_DIR = Path(__file__).resolve().parent

POSE_MODEL = BASE_DIR / "models" / "pose_landmarker_lite.task"
FACE_MODEL = BASE_DIR / "models" / "face_landmarker.task"

# ==========================================
# MEDIAPIPE SETUP
# ==========================================

BaseOptions = mp.tasks.BaseOptions

PoseLandmarker = mp.tasks.vision.PoseLandmarker
PoseLandmarkerOptions = mp.tasks.vision.PoseLandmarkerOptions

FaceLandmarker = mp.tasks.vision.FaceLandmarker
FaceLandmarkerOptions = mp.tasks.vision.FaceLandmarkerOptions

RunningMode = mp.tasks.vision.RunningMode

# Pose options
pose_options = PoseLandmarkerOptions(
    base_options=BaseOptions(
        model_asset_path=str(POSE_MODEL)
    ),
    running_mode=RunningMode.VIDEO,
    num_poses=1
)

# Face options
face_options = FaceLandmarkerOptions(
    base_options=BaseOptions(
        model_asset_path=str(FACE_MODEL)
    ),
    running_mode=RunningMode.VIDEO,
    num_faces=1
)

# ==========================================
# POSE CONNECTIONS
# ==========================================

POSE_CONNECTIONS = [
    (0, 1), (1, 2), (2, 3), (3, 7),
    (0, 4), (4, 5), (5, 6), (6, 8),
    (11, 12),
    (11, 13), (13, 15),
    (12, 14), (14, 16),
    (11, 23), (12, 24),
    (23, 24),
    (23, 25), (25, 27),
    (24, 26), (26, 28),
    (27, 29), (29, 31),
    (28, 30), (30, 32)
]

# ==========================================
# OPEN WEBCAM
# ==========================================

cap = cv2.VideoCapture(0)

if not cap.isOpened():
    raise RuntimeError("Could not open webcam")

# ==========================================
# START BOTH MODELS
# ==========================================

with PoseLandmarker.create_from_options(pose_options) as pose_detector, \
     FaceLandmarker.create_from_options(face_options) as face_detector:

    start_time = time.monotonic()
    last_timestamp_ms = -1

    while True:

        success, frame = cap.read()

        if not success:
            break

        # Mirror webcam
        frame = cv2.flip(frame, 1)

        height, width, _ = frame.shape

        # Convert BGR to RGB
        rgb_frame = cv2.cvtColor(
            frame,
            cv2.COLOR_BGR2RGB
        )

        # Convert to MediaPipe image
        mp_image = mp.Image(
            image_format=mp.ImageFormat.SRGB,
            data=rgb_frame
        )

        # Timestamp for VIDEO mode (strictly increasing)
        timestamp_ms = int(
            (time.monotonic() - start_time) * 1000
        )
        timestamp_ms = max(timestamp_ms, last_timestamp_ms + 1)
        last_timestamp_ms = timestamp_ms

        # ==================================
        # RUN BOTH MODELS
        # ==================================

        pose_result = pose_detector.detect_for_video(
            mp_image,
            timestamp_ms
        )

        face_result = face_detector.detect_for_video(
            mp_image,
            timestamp_ms
        )

        # ==================================
        # DRAW POSE LANDMARKS (GREEN)
        # ==================================

        if pose_result.pose_landmarks:

            landmarks = pose_result.pose_landmarks[0]

            # Draw body connections
            for start, end in POSE_CONNECTIONS:

                x1 = int(landmarks[start].x * width)
                y1 = int(landmarks[start].y * height)

                x2 = int(landmarks[end].x * width)
                y2 = int(landmarks[end].y * height)

                cv2.line(
                    frame,
                    (x1, y1),
                    (x2, y2),
                    (0, 255, 0),
                    2
                )

            # Draw body landmarks
            for landmark in landmarks:

                x = int(landmark.x * width)
                y = int(landmark.y * height)

                cv2.circle(
                    frame,
                    (x, y),
                    4,
                    (0, 255, 0),
                    -1
                )

        # ==================================
        # DRAW FACE LANDMARKS (RED)
        # ==================================

        if face_result.face_landmarks:

            face_landmarks = face_result.face_landmarks[0]

            for landmark in face_landmarks:

                x = int(landmark.x * width)
                y = int(landmark.y * height)

                cv2.circle(
                    frame,
                    (x, y),
                    1,
                    (0, 0, 255),
                    -1
                )

        # ==================================
        # DISPLAY
        # ==================================

        cv2.putText(
            frame,
            "Green = Pose | Red = Face",
            (10, 30),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (255, 255, 255),
            2
        )

        cv2.imshow(
            "UTEK - Face & Pose Tracking",
            frame
        )

        # Press Q to quit
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

cap.release()
cv2.destroyAllWindows()