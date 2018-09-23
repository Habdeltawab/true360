from CameraInterface import CameraInterface
import requests
import time
import json


class Virb(CameraInterface):

    @staticmethod
    def _request_live_preview(vertical_resolution):
        print("Requesting live preview URL from Virb...")
        r = requests.post('http://192.168.0.1/virb', data=json.dumps({
            "command": "livePreview",
            "streamType": "rtp",
            "liveStreamActive": "1",
            "maxResolutionVertical": vertical_resolution
        }), timeout=1)
        if r.status_code == 200:
            response = r.json()
            if response["result"] == 1:
                return response["url"], True
            else:
                print("Virb responded with an error")
                return None, False
        else:
            print r.status_code
            return None, False

    def _build_command(self, rtmp_key, vertical_resolution, duration):
        print("Building ffmpeg command...")
        rtsp_live_preview_url, success = self._request_live_preview(vertical_resolution)
        if not success:
            exit(1)

        return 'ffmpeg ' \
               '-f lavfi ' \
               '-i anullsrc ' \
               '-rtsp_transport udp ' \
               '-i {} ' \
               '-tune zerolatency ' \
               '-vcodec libx264 ' \
               '-pix_fmt + ' \
               '-c:v copy ' \
               '-c:a aac ' \
               '-strict experimental ' \
               '-f flv ' \
               'rtmp://a.rtmp.youtube.com/live2/{} ' \
               '../archives/{}.mp4'.format(rtsp_live_preview_url, rtmp_key, time.time())

    def get_ffmpeg(self, rtmp_key, vertical_resolution, duration):
        return self._build_command(rtmp_key, vertical_resolution, duration)
