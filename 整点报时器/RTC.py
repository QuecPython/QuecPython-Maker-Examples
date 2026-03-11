from machine import RTC
import audio
import utime
from machine import RTC

rtc = RTC()
tts = audio.TTS(0)
str1 = '大郎，该喝药了' 
while True:
    data=rtc.datetime()
    if data[5] == 0:
        tts.play(4,0,2,str1)
    print("当前时间：%04d-%02d-%02d %02d:%02d:%02d" % (data[0], data[1], data[2], data[4], data[5], data[6]))
    utime.sleep(10)    
