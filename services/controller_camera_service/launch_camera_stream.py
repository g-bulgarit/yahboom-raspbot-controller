import subprocess


def launch_camera_stream():
    subprocess.run(
        [
            "start",
            r"D:\Code\robot-controller\services\controller_camera_service\launch_gst.bat",
        ],
        shell=True,
    )

    while True:
        pass


if __name__ == "__main__":
    launch_camera_stream()
