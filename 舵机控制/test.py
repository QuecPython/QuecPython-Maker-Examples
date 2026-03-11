import utime
from misc import PWM_V2

# 初始化一个 PWM（根据板子调整 PWM0/频率/初始占空比）
start = 15       # 起始占空比（对应中间位置）
min_duty = 5     # 最小占空比（对应一个极限）
max_duty = 25    # 最大占空比（对应另一极限）
delay_ms = 20    # 每步等待时间，控制运动速度

pwm = PWM_V2(PWM_V2.PWM0, 100.0, start)
def smooth_move(pwmx,start0,end,steps=5):
    for i in range(steps+1):
        pwmx.open(100.0,start0+int((end-start0)/(steps)*i)) 
        utime.sleep_ms(20)

if __name__ == "__main__":
    pwm.open(100.0,15)
    utime.sleep_ms(500)
    smooth_move(pwm,start,max_duty,5)
    utime.sleep_ms(500)
    smooth_move(pwm,max_duty,min_duty,5)
    utime.sleep_ms(500)
    smooth_move(pwm,min_duty,start,5)
    utime.sleep_ms(500)
    pwm.close()