# Low Latency Streaming (GStreamer with `rpicamsrc` over rtsp)

## Failed attempts

After trying multiple solutions using the video-for-linux(-2) driver as a source (`v4l2src`), I have not managed to get a good video stream with low latency - the best result was achieved with the following pipeline, cropping the original sensor resolution of `2592x1944` to `640x480` (corner):

```
v4l2src device=/dev/video0 ! video/x-raw, width=640, height=480, framerate=30/1, crop-left=0, crop-right=1952, crop-top=1464, crop-bottom=0 ! videoconvert ! x264enc tune=zerolatency speed-preset=superfast ! rtph264pay name=pay0 pt=96 aggregate-mode=zero-latency
```

## Success, `rpicamsrc`

Compiling the following plugin for gstreamer [as seen in the instructions here](https://github.com/thaytan/gst-rpicamsrc) and using it as a source provides a very good quality, low-latency stream :)

Working pipeline:
```
rpicamsrc num-buffers=-1 ! video/x-raw, width=640, height=480, framerate=30/1 ! jpegenc ! rtpjpegpay name=pay0 pt=96
```

A version with manual controls running through `gst-rtsp-server` looks like this:

```
./test-launch --gst-debug=3 "( rpicamsrc num-buffers=-1 awb-mode=1 exposure-mode=0 shutter-speed=33333 video-stabilisation=0 ! video/x-raw, width=640, height=480, framerate=30/1 ! jpegenc ! rtpjpegpay name=pay0 pt=96 )"
```