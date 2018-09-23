from true360.exceptions import UnknownStreamerException
from true360.enums import StreamType
from Ffmpeg import Ffmpeg


class Streamer:

    def __init__(self, connection_type, camera):
        if connection_type == StreamType.FFMPEG:
            self._bridge_class = Ffmpeg
        else:
            raise UnknownStreamerException("Unrecognized Streamer")

        self._camera = camera
        self._bridge_object = None

    def start_stream_handler(self, rtmp_key, vertical_resolution, duration, on_success, on_error):
        self._bridge_object = self._bridge_class()
        command = self._camera.get_ffmpeg(rtmp_key, vertical_resolution, duration)

        return self._bridge_object.start_stream_handler(rtmp_key,
                                                        vertical_resolution,
                                                        duration,
                                                        command,
                                                        on_success,
                                                        on_error)

    def stop_stream_handler(self):
        self._bridge_object.stop_stream_handler()
