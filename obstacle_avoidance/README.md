# EC800X Duino  开发板火焰检测

## 项目介绍

基于移远**EC800X Duino 开发板**，通过 GPIO 外部中断实现红外避障传感器的障碍物检测，适用于物联网终端、智能安防、智能小车避障等嵌入式开发场景。

## 硬件信息

- 主控平台：移远 EC800X Duino 开发板

  红外避障传感器引脚：GPIO31（支持外部中断）

## 代码实现

```python
from machine import Pin,ExtInt
import utime

# 全局标志位：标记是否检测到障碍物
human_detected = False

# 配置GPIO31为输入模式，启用上拉电阻
gpio = Pin(Pin.GPIO31, Pin.IN, Pin.PULL_PU)

def irq_handler(args):
    """中断处理函数：检测到障碍物时置位标志位"""
    global human_detected, gpio
    # 红外避障传感器检测到障碍时输出低电平（0），触发标志位
    if gpio.read() == 0:
        human_detected = True

if __name__ == '__main__':
    # 注册外部中断：GPIO31、下降沿触发（1→0表示有障碍物）、上拉电阻、绑定中断处理函数
    ext = ExtInt(ExtInt.GPIO31, ExtInt.IRQ_FALLING, ExtInt.PULL_PU, irq_handler)
    
    print("Waiting for human detection...")
    ext.enable()  # 启用外部中断
    
    # 主循环：轮询标志位并打印检测结果
    while True:
        if human_detected:
            print("有障碍物")
            human_detected = False  # 清除标志位，等待下一次检测
        else:
            print("无障碍")
        utime.sleep(1)  # 检测间隔1秒，可按需调整
```

## 代码说明

1. **导入模块**：引入 Pin（GPIO 控制）、ExtInt（外部中断）、utime（延时）核心模块；

2. **全局标志位**：`human_detected` 用于标记是否检测到障碍物，跨中断函数和主循环共享状态；

3. **GPIO 配置**：将 GPIO31 配置为输入模式并启用上拉电阻，适配红外避障传感器的电平逻辑；

4. **中断处理函数**：传感器检测到障碍物输出低电平时，置位 `human_detected` 标志位；

5. **中断注册与启用**：绑定 GPIO31 为下降沿触发中断（传感器从高电平变低电平表示检测到障碍），并启用中断；

6. **主循环逻辑**：轮询标志位，打印 “有障碍物 / 无障碍” 结果，每次检测后重置标志位，实现持续检测。


## 注意事项

- 确保硬件接线正确：

  - 红外避障传感器的信号引脚接 EC800X Duino 开发板 GPIO31；
  - 传感器电源、地线需对应接开发板的 3.3V/5V 和 GND；

  

- 电平逻辑适配：若传感器检测到障碍时输出高电平，需将中断触发方式改为 `ExtInt.IRQ_RISING`，并调整 `irq_handler` 中判断条件为 `gpio.read() == 1`；

- 检测间隔：主循环中 `utime.sleep(1)` 可根据实际需求调整（如改为 0.5 秒提升检测灵敏度）；

- 中断防抖：实际部署时，可在中断处理函数中增加短延时（如 `utime.sleep_ms(20)`），避免传感器电平抖动导致误触发。