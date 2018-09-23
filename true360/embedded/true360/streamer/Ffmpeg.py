from StreamerInterface import StreamerInterface
import subprocess
from threading import Thread


class Ffmpeg(StreamerInterface, Thread):

    def __init__(self):
        super(Ffmpeg, self).__init__()
        self._p = None
        self._running = False
        self._command = None
        self._on_success = None
        self._on_error = None

    def start_stream_handler(self, rtmp_key, vertical_resolution, duration, command, on_success, on_error):
        self._on_success = on_success
        self._on_error = on_error
        self._command = command

        self.start()

    def stop_stream_handler(self):
        if self._running:
            self._p.kill()

    def _close_fd(self):
        self._p.stdout.close()
        self._p.stderr.close()
        self._p.stdin.close()

    def run(self):
        self._running = True
        print("streaming started")
        try:
            self._p = subprocess.Popen(self._command.split(), stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                       stderr=subprocess.PIPE)
            stderr = self._p.communicate()[1].split('\n')
            if self._p.returncode == 0 or self._p.returncode == -9:
                self._on_success()
            elif "already exists. Overwrite ?" in stderr[len(stderr) - 2]:
                print("file already exists")
                self._on_error()
            else:
                try:
                    with open("./streamer-log.txt", "w") as log:
                        subprocess.check_output(self._command.split(), stderr=log)
                except subprocess.CalledProcessError as e:
                    self._on_error()
            self._close_fd()
        except OSError as ose:
            print("ffmpeg not found")
        self._running = False
        print("streaming stopped")
