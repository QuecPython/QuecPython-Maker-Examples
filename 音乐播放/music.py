import request
import utime
import audio
import _thread
from machine import Pin,ExtInt
from queue import Queue

aud=audio.Audio(0)
Pin(Pin.GPIO33, Pin.OUT, Pin.PULL_DISABLE, 1)  # PA使能
Pin(Pin.GPIO29, Pin.OUT, Pin.PULL_DISABLE, 1)  # PA使能
aud.setVolume(5)

flag=True


# url = "https://euai-media.acceleronix.io/hls/music/jp04.mp3"
# url = "https://euai-media.acceleronix.io/hls/music/ThroughThickandThin.mp3"

# url = "https://euai-media.acceleronix.io/hls/music/HeartofHome.mp3"
# url = "https://euai-media.acceleronix.io/hls/music/ShatteredEchoes.mp3"
# url="https://euai-media.acceleronix.io/hls/music/VelvetHearts.mp3"
# url="https://euai-media.acceleronix.io/hls/music/jp01.mp3"
# url="https://euai-media.acceleronix.io/hls/music/jp02.mp3"
url="https://euai-media.acceleronix.io/hls/music/jp03.mp3"


def inner(url):
    resp = request.get(url)
    # utime.sleep(3)
    for data in resp.content:
        # logger.debug("play audio data length: {}".format(len(data)))
        aud.playStream(3, data.encode())
    aud.stopPlayStream()
t = _thread.start_new_thread(inner, (url,))


#-------------------------------------------------------------------



# def download_and_cache(url):
#     """
#     下载音频并缓存到内存中
#     :param url: 音频文件的 URL
#     :return: 缓存的音频数据
#     """
#     print("开始下载音频: {url}")
#     try:
#         resp = request.get(url, stream=True)
#         cache = []
#         chunk_size = 256

#         while True:
#             chunk = resp.raw.read(chunk_size)
#             if not chunk or len(cache)>600:
#                 break
#             cache.append(chunk)

#         print("音频下载完成，缓存大小: {len(cache)} 块",len(cache))
#         return cache
#     except Exception as e:
#         print("下载失败: ",len(cache))
#         return None


# def play_audio_from_cache(cache):
#     """
#     从缓存中播放音频
#     :param cache: 缓存的音频数据
#     """
#     print("开始播放缓存的音频")
#     try:
#         for chunk in cache:
#             aud.playStream(3, chunk)
#         print("音频播放完成")
#     except Exception as e:
#         print("播放失败: ",e)
#     finally:
#         aud.stopPlayStream()


# play_audio_from_cache(download_and_cache(url))

#-------------------------------------------------------------------  

# def inner(url):
#     print("play")
#     flag=True
#     if url == "https://euai-media.acceleronix.io/hls/music/ThroughThickandThin.mp3" or url=="https://euai-media.acceleronix.io/hls/music/jp04.mp3":
#         resp = request.get(url, stream=True)
#         print("play jp04")
#         chunk_size = 1024
#         while True:
#             chunk = resp.raw.read(chunk_size)
#             # print("play audio data length: {}".format(len(chunk)))
#             if not chunk or flag == False:
#                 break
#             aud.playStream(3, chunk)
#     else:
#         resp = request.get(url)
#         print("play other")
#         for data in resp.content:
#         # logger.debug("play audio data length: {}".format(len(data)))
#             aud.playStream(3, data.encode())
#     print("stop")
#     aud.stopPlayStream()

# t = _thread.start_new_thread(inner, (url,))



#-------------------------------------------------------------------  


# aud_flag=False
# def inner(url):
#     global aud_flag
#     que=Queue(1000)
#     try:
#         resp = request.get(url, stream=True)
#         if resp.status_code != 200:
#             print("HTTP请求失败：{}".format(resp.status_code))
#             return
#         aud_flag=True
 
#         for data in resp.content:
#             que.put(data.encode())
#             # if data == None:
            
#         for aa in range(que.size()):
#             data=que.get()
#             if aud_flag:
#                 print(que.size())
#                 print("play audio data length: {}".format(len(data)))
#                 aud_flag=False
#             aud.playStream(3, data.encode())
#         aud.stopPlayStream()
#     except Exception as e:
#         print("Error: {e}",e)
# t = _thread.start_new_thread(inner, (url,))



#-------------------------------------------------------------------  



# aud_flag=False
# que=Queue(1000)
# def inner(url):
#     global aud_flag
#     resp = request.get(url, stream=True)
#     if resp.status_code != 200:
#         print("HTTP请求失败：{}".format(resp.status_code))
#         return
    
#     for data in resp.content:
#         que.put(data.encode())
#         # if data == None:
#         if que.size()>250:
#             aud_flag=True
#             print("存储长度",que.size())
#         elif que.size()<50:
#             aud_flag=False
#             # 

# def play_music():
#     global aud_flag
#     try:
#         while True:
#             if aud_flag == False:
#                 utime.sleep_ms(200)
#                 print(que.size())
#                 aud.stopPlayStream()
#             if aud_flag and que.size()>0:
#                 # print("play audio data length: {}".format(que.size()))
#                 data=que.get()
#                 aud.playStream(3, data.encode())
#     except Exception as e:
#         print("Error: {e}",e)
    
# t = _thread.start_new_thread(inner, (url,))
# b= _thread.start_new_thread(play_music, ())

#-----------------------------------------------------------------------------


# aud_flag=False
# download_paused=False
# que=Queue(500)
# def inner(url):
#     global aud_flag
#     global download_paused
#     resp = request.get(url, stream=True)
#     if resp.status_code != 200:
#         print("HTTP请求失败：{}".format(resp.status_code))
#         return
    
#     for data in resp.content:  # 使用 iter_content 按块读取数据
#         while download_paused:  # 如果下载线程被暂停，则等待
#             utime.sleep_ms(100)
        
#         que.put(data)  # 将数据放入队列
#         if que.size() > 400:  # 当队列接近满时，暂停下载
#             download_paused = True
#         elif que.size() < 200:  # 当队列数据减少到一定程度时，恢复下载
#             download_paused = False

# def play_music():
#     global aud_flag
#     global download_paused
#     try:
#         while True:
#             if que.size() < 50:  # 如果队列数据不足，暂停播放
#                 aud_flag = False
#                 aud.stopPlayStream()
#                 print("队列数据不足，暂停播放",que.size())
#                 utime.sleep_ms(200)
#                 continue
#             aud_flag = True
#             if que.size() > 0:  # 如果队列中有数据，则继续播放
#                 data = que.get()
#                 aud.playStream(3, data)
#                 print("播放音频数据，队列剩余长度: {}".format(que.size()))
#     except Exception as e:
#         print("Error: {e}",e)
    
# t = _thread.start_new_thread(inner, (url,))
# b= _thread.start_new_thread(play_music, ())
