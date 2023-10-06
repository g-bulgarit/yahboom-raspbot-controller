import cv2
from loguru import logger
import numpy as np
import numpy.typing as npt

from packages.image_operations.text_overlay import (
    font,
    font_debug_color,
    font_size,
    origin,
    thickness,
)

from packages.image_operations.image_state import ImageState

CameraImage = npt.NDArray[np.uint8]
RTSP_STREAM_URL: str = "rtsp://192.168.1.197:8554/test"


def draw_hud(frame: CameraImage, state: ImageState, draw_frame_number: bool = False):
    if draw_frame_number:
        frame = cv2.putText(
            frame,
            f"{state.frame_counter}",
            origin,
            font,
            font_size,
            font_debug_color,
            thickness,
        )
    return frame


def launch_camera_stream():
    state = ImageState(frame_counter=0)
    frame_counter: np.uint64 = 0
    logger.debug("Camera listener running.")
    vcap = cv2.VideoCapture(RTSP_STREAM_URL)
    if not vcap.isOpened():
        print("Failed to open stream")
        exit(0)

    while 1:
        ret, frame = vcap.read()
        if not ret:
            logger.warning(f"Skipped frame {state.frame_counter}")
            continue
        state.frame_counter += 1
        frame = draw_hud(frame, state, draw_frame_number=True)

        cv2.imshow("Camera Stream", frame)
        cv2.waitKey(1)


if __name__ == "__main__":
    pass
