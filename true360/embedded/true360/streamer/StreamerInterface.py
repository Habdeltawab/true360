from abc import ABCMeta, abstractmethod


class StreamerInterface:
    __metaclass__ = ABCMeta

    @abstractmethod
    def start_stream_handler(self, rtmp_key, vertical_resolution, duration, command, on_success, on_error):
        pass

    @abstractmethod
    def stop_stream_handler(self):
        pass
