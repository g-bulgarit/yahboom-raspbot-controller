import cv2


def launch_camera_stream():
    vcap = cv2.VideoCapture("rtsp://192.168.1.197:8554/test")
    fps = vcap.get(cv2.CAP_PROP_FPS)
    print(fps)
    if not vcap.isOpened():
        print("Failed to open stream")
        exit(0)

    while 1:
        ret, frame = vcap.read()
        cv2.imshow("VIDEO", frame)
        cv2.waitKey(1)


if __name__ == "__main__":
    pass
