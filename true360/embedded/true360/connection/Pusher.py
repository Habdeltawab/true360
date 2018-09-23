from ConnectionInterface import ConnectionInterface
import pysher
import json
import logging
import time


class Pusher(ConnectionInterface):

    def __init__(self, streamer, config):
        self._config = config

        self._deviceName = self._config.getstr("DEFAULT", "devicename")
        self._zooId = self._config.getstr("DEFAULT", "zooid")
        self._deviceId = self._config.getstr("DEFAULT", "deviceid")
        self._pusherKey = self._config.getstr("PUSHER", "key")
        self._pusherSecret = self._config.getstr("PUSHER", "secret")
        self._pusherHost = self._config.getstr("PUSHER", "host")

        self._logfile = open("./true360/logs/pusher-log.txt", "w")
        self._log_handler(self._logfile)
        self._pusher = pysher.Pusher(key=self._pusherKey,
                                     secret=self._pusherSecret,
                                     custom_host=self._pusherHost,
                                     name="connection-thread")
        self._channel = None
        self._connection = None
        self._connected = False

        self._registration_channel = "private-%s" % self._deviceId
        self._device_channel = None

        self._streamer = streamer

    @staticmethod
    def _log_handler(log_file):
        logging.getLogger("pysher.connection").addHandler(logging.StreamHandler(log_file))

    def _connect(self):
        self._pusher.connection.bind("pusher:connection_established", self._connection)
        self._pusher.connect()
        self._connected = True

    def _stream_success_handler(self):
        print("success")

    def _stream_error_handler(self):
        print("error")

    def _start_stream_event_listener(self, *args):
        response = json.loads(args[0])
        self._streamer.start_stream_handler(response["rtmp_key"],
                                            response["vertical_resolution"],
                                            response["duration"],
                                            on_success=self._stream_success_handler,
                                            on_error=self._stream_error_handler)

    def _stop_stream_event_listener(self, *args):
        self._streamer.stop_stream_handler()

    def _terminate_event_listener(self, *args):
        self.close()

    def _device_channel_connection(self, data):
        self._channel = self._pusher.subscribe(self._device_channel)
        self._channel.bind("start-stream", self._start_stream_event_listener)
        self._channel.bind("stop-stream", self._stop_stream_event_listener)
        self._channel.bind("terminate", self._terminate_event_listener)

    def _save_device_name(self, devicename, zooid):
        self._config.set("DEFAULT", "devicename", devicename)
        self._config.set("DEFAULT", "zooid", zooid)
        self._config.save()
        self._deviceName = devicename
        self._zooId = zooid

    def _new_name_event_listener(self, *args):
        response = json.loads(args[0])
        self._save_device_name(response["name"], response["zoo_id"])
        self._pusher.unsubscribe(self._registration_channel)

    def _registration_channel_connection(self, data):
        self._channel = self._pusher.subscribe(self._registration_channel)
        self._channel.bind('new-name', self._new_name_event_listener)

    def is_registered(self):
        return self._deviceName

    def register(self):
        self._connection = self._registration_channel_connection
        self._connect()
        while not self._deviceName:
            print("Waiting for registration...")
            time.sleep(1)
        print("Registered as %s" % self._deviceName)

    def listen(self):
        self._device_channel = "private-%s-%s" % (self._zooId, self._deviceName)
        if not self._connected:
            self._connection = self._device_channel_connection
            self._connect()
        else:
            self._device_channel_connection(None)
        print("Listening for commands...")

    def close(self):
        self._pusher.unsubscribe(self._device_channel)
        self._pusher.connection.disconnect()
        self._pusher.disconnect()
