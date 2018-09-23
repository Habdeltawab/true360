from true360 import bootstrap, CameraType, StreamType, ConnectionType
from true360.exceptions import \
    UnknownCameraException, \
    UnknownConnectionException, \
    UnknownStreamerException, \
    ConfigNotSetException
from true360.utils import True360Configs

if __name__ == '__main__':

    _config = True360Configs()

    config_camera_type = _config.getint("CAMERA", "TYPE")
    if not config_camera_type:
        config_camera_type = CameraType.VIRB

    config_stream_type = _config.getint("STREAMER", "TYPE")
    if not config_stream_type:
        config_stream_type = StreamType.FFMPEG

    config_connection_type = _config.getint("CONNECTION", "TYPE")
    if not config_connection_type:
        config_connection_type = ConnectionType.PUSHER

    try:
        bootstrap(
            config=_config,
            camera_type=config_camera_type,
            stream_type=config_stream_type,
            connection_type=config_connection_type
        )
    except UnknownCameraException as camera_exception:
        print(camera_exception)
    except UnknownConnectionException as connection_exception:
        print(connection_exception)
    except UnknownStreamerException as streamer_exception:
        print(streamer_exception)
    except ConfigNotSetException as config_exception:
        print(config_exception)
    except KeyboardInterrupt as keyboard_interrupt:
        pass
