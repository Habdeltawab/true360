from true360.enums import CameraType, ConnectionType, StreamType
from true360.exceptions import ConfigNotSetException
from true360.connection import Connection
from true360.streamer import Streamer
from true360.camera import Camera
import threading


def bootstrap(config, camera_type=CameraType.VIRB, connection_type=ConnectionType.PUSHER,
              stream_type=StreamType.FFMPEG):
    if not config:
        raise ConfigNotSetException("Configuration file is not set properly")

    camera_object = Camera(camera_type)
    streamer_object = Streamer(stream_type, camera_object)
    connection_object = Connection(connection_type, streamer_object, config)

    if not connection_object.is_registered():
        connection_object.register()
    connection_object.listen()

    while True:
        for t in threading.enumerate():
            if t.getName() == "connection-thread":
                t.join()
                break
        break
