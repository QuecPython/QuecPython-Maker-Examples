from misc import PWM_V2
import audio
from machine import Pin,ExtInt
import utime
import _thread

pwm=PWM_V2(PWM_V2.PWM0, 100.0, 15)
aud = audio.Audio(2)
Pin(Pin.GPIO10,Pin.OUT,Pin.PULL_DISABLE,1)
def test():
    print("已打开药盒")
    pwm.open(100.0,5)
    aud.play(2, 1, 'U:/music.mp3')

    
def print_time():
    while True:
        tupe_t=utime.localtime()
        print("当前时间：%04d-%02d-%02d %02d:%02d:%02d" % (tupe_t[0], tupe_t[1], tupe_t[2], tupe_t[3], tupe_t[4], tupe_t[5]))
        if tupe_t[5]==1:
            test()
        utime.sleep(1)
        
def func(args):
    print("外部中断触发，关闭药盒")
    pwm.open(100.0,15)


if __name__ == "__main__":
    ext_int=ExtInt(ExtInt.GPIO20, ExtInt.IRQ_FALLING, ExtInt.PULL_PU, func,filter_time=50)
    thread=_thread.start_new_thread(print_time, ())
    ext_int.enable()
    while True:
        utime.sleep(1)