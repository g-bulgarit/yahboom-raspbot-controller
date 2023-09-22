import subprocess

if __name__ == "__main__":
    subprocess.run(
        [
            "start",
            r"D:\Code\robot-controller\services\controller_camera_service\launch_gst.bat",
        ],
        shell=True,
    )

    while True:
        pass
