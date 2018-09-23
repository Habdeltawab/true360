from abc import ABCMeta, abstractmethod


class CameraInterface:
    __metaclass__ = ABCMeta

    @abstractmethod
    def get_ffmpeg(self, rtmp_key, vertical_resolution, duration):
        pass