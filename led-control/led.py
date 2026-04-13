# 导入I/O引脚控制模块
from machine import Pin

# 创建GPIO对象，配置引脚为输出、浮空模式，默认高电平
gpio1 = Pin(Pin.GPIO29, Pin.OUT, Pin.PULL_DISABLE, 1)

# 设置高电平，红亮灯
gpio1.write(1)
print("LED is on")