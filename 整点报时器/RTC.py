from machine import RTC
import audio
import utime
from machine import RTC

rtc = RTC()
tts = audio.TTS(0)

while True:
    data=rtc.datetime()
    
    if data[6] == 00:
        print("当前时间：%04d-%02d-%02d %02d:%02d:%02d" % (data[0], data[1], data[2], data[4], data[5], data[6]))
        str1 = "当前时间是：%04d年%02d月%02d日 %02d点%02d分%02d秒" % (data[0], data[1], data[2], data[4], data[5], data[6])
        tts.play(4,0,2,str1)
    
    utime.sleep(1)    
