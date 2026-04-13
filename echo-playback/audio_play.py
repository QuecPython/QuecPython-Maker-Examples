# -*- coding: UTF-8 -*-
#录音流
import audio
from machine import Pin
import utime
'''
外接喇叭播放，参数选择0
'''

pa_enable_pin = Pin(Pin.GPIO33, Pin.OUT, Pin.PULL_DISABLE, 1)
pa_enable_pin.write(1)

rec = audio.Record(0)
aud = audio.Audio(0)

record_time = 5 #录音时间，单位秒
buf = bytearray(0) #空buff用来缓存音频
aud_type = rec.AMRNB

aud.setVolume(10)#设置音量，范围0-11，0为静音，11为最大

def stream_rec_cb(para):
    global buf
    # print("para:", para)
    if(para[0] == 'stream'):
        if(para[2] == 1):
            read_buf = bytearray(para[1])
            rec.stream_read(read_buf,para[1])
            buf += read_buf
            del read_buf
        elif (para[2] == 3):
            pass
            aud.stopPlayStream()
            aud.playStream(aud_type, buf)

if __name__ == "__main__":
    rec.end_callback(stream_rec_cb)
    print("record after 5s")
    utime.sleep(5)
    print("record start")
    rec.stream_start(aud_type, 8000, record_time)
    utime.sleep(5)
    print("record end")
 
