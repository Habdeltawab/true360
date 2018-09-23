from true360.exceptions import UnknownConnectionException
from true360.enums import ConnectionType
from Pusher import Pusher


class Connection:

    def __init__(self, connection_type, streamer, config):
        if connection_type == ConnectionType.PUSHER:
            self._bridge = Pusher(streamer, config)
        else:
            raise UnknownConnectionException("Unrecognized Connection")

    def is_registered(self):
        return self._bridge.is_registered()

    def register(self):
        self._bridge.register()

    def listen(self):
        self._bridge.listen()

    def close(self):
        self._bridge.close()
