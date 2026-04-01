# 导入I/O引脚控制模块
from machine import Pin

# 创建GPIO对象，配置引脚为输出、浮空模式，默认高电平
gpio1 = Pin(Pin.GPIO19, Pin.OUT, Pin.PULL_DISABLE, 1)

# 设置低电平，LED亮灯
gpio1.write(0)