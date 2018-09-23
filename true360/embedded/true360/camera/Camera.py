from true360.exceptions import UnknownCameraException
from true360.enums import CameraType
from true360.camera import Virb
from true360.camera import Mock


class Camera:

    def __init__(self, camera_type):
        if camera_type == CameraType.VIRB:
            self._bridge = Virb()
        elif camera_type == CameraType.RICOH:
            print("Ricoh Not implemented")
        elif camera_type == CameraType.MOCK:
            self._bridge = Mock()
        else:
            raise UnknownCameraException("Unrecognized Camera")

    def get_ffmpeg(self, rtmp_key, vertical_resolution, duration):
        return self._bridge.get_ffmpeg(rtmp_key, vertical_resolution, duration)
