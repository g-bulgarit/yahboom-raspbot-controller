D:\gstreamer\1.0\mingw_x86_64\bin\gst-launch-1.0.exe rtspsrc location=rtsp://192.168.1.197:8554/test latency=0 ! rtph264depay ! h264parse ! avdec_h264 ! videoconvert ! glimagesink