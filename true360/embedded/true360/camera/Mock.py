from CameraInterface import CameraInterface
import time


class Mock(CameraInterface):

    def get_ffmpeg(self, rtmp_key, vertical_resolution, duration):
        return 'ffmpeg ' \
               '-i rtsp://184.72.239.149/vod/mp4:BigBuckBunny_175k.mov ' \
               '-t {} ' \
               './archives/{}.mpg'.format(duration, time.time())
