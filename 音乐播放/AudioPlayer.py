import request
import audio
import _thread
from machine import Pin

aud=audio.Audio(0)
Pin(Pin.GPIO29, Pin.OUT, Pin.PULL_DISABLE, 1)  # PA使能
aud.setVolume(5)

url="https://euai-media.acceleronix.io/hls/music/jp03.mp3"

def inner(url):
    resp = request.get(url)
    print("开始播放")
    for data in resp.content:
        # logger.debug("play audio data length: {}".format(len(data)))
        aud.playStream(3, data.encode())
    aud.stopPlayStream()
    print("播放结束")
t = _thread.start_new_thread(inner, (url,))




# url = "https://euai-media.acceleronix.io/hls/music/jp04.mp3"
# url = "https://euai-media.acceleronix.io/hls/music/ThroughThickandThin.mp3"

# url = "https://euai-media.acceleronix.io/hls/music/HeartofHome.mp3"
# url = "https://euai-media.acceleronix.io/hls/music/ShatteredEchoes.mp3"
# url="https://euai-media.acceleronix.io/hls/music/VelvetHearts.mp3"
# url="https://euai-media.acceleronix.io/hls/music/jp01.mp3"
# url="https://euai-media.acceleronix.io/hls/music/jp02.mp3"