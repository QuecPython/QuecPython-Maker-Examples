# 趣味进阶体验：让【C4-PO1开发板】成为智能药盒！

本文介绍基于 C4-PO1 开发板实现 “智能药箱” 的项目设计，包含定时开盖、外部中断关盖、音频播报（可选扩展）等核心功能，帮助初学者快速上手基于 QuecPython 的智能硬件开发。

## 项目介绍

本项目实现基于 C4-PO1 开发板的智能药箱核心功能：

1. 定时触发：每秒检测系统时间，当秒数为 1 时自动打开药盒（PWM 驱动执行器）；

2. 外部中断：通过 GPIO20 下降沿触发中断，关闭药盒；

3. 可扩展音频播报（基于 QuecPython audio 模块）：如开盖 / 关盖语音提示、定时服药提醒等；

   

   涵盖硬件控制、定时器、外部中断、多线程编程全流程，为智慧医疗、居家智能提醒类设备开发提供参考。

## 核心代码讲解

```python
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
```

## 代码说明

1. 硬件控制层

   - PWM_V2 驱动药箱开关执行器，`pwm.open(频率, 占空比)` 控制开盖 / 关盖动作；
   - ExtInt 外部中断（GPIO17）检测外部触发信号（如按键），实现手动关盖；

   

2. 定时逻辑层

   - 多线程运行时间检测函数，每秒获取系统时间，当秒数为 1 时触发开盖；

   

3. 扩展功能（音频播报）

   - 集成 audio 模块，可通过 URL 播放语音提示（如服药提醒、开关盒提示），复用 QuecPython 音频播放逻辑；

   

4. 稳定性设计

   - 外部中断添加 50ms 防抖过滤，避免误触发；
   - 多线程分离时间检测与主循环，保证中断响应实时性。

   

## 工程测试

1. 硬件连接：

   - PWM0 引脚连接药箱执行器，GPIO17 连接外部触发按键（如关盖按钮）；
   - 音频模块（如 VS1053）按 SPI 引脚连接，实现语音播报；

   

2. 测试步骤：

   - 通过 [QPYcom脚本下载教程](https://developer.quectel.com/doc/quecpython/Getting_started/zh/4G/first_python.html) 将代码下载到 C4-PO1 开发板；
   - 运行脚本，终端实时打印系统时间；
   - 当秒数为 1 时，观察药箱是否自动开盖，终端打印 “已打开药盒”；
   - 按下 GPIO17 外接按键，触发中断，药箱关闭，终端打印 “外部中断触发，关闭药盒”；

   

3. 调试要点：

   - 若定时不触发，检查系统时间同步 /utime.localtime () 返回值；
   - 若中断误触发，调整 filter_time 防抖参数；
   - 若音频不播放，检查 PA 使能引脚、音频 URL 有效性。

   

## 运行效果

- 终端实时打印：`当前时间：2024-05-20 14:30:01`，同时药箱自动开盖，打印 “已打开药盒”；
- 按下关盖按键，终端打印：`外部中断触发，关闭药盒`，药箱执行关盖动作；
- （扩展）音频模块同步播放 “药盒已打开 / 关闭” 语音提示。

## 总结

本文基于 C4-PO1 开发板实现了智能药箱核心功能，涵盖 PWM 驱动、定时任务、外部中断、多线程、音频播报等关键技术点，适配居家智能服药提醒、老年看护等场景。开发者可基于此扩展：

- 多时段定时服药提醒（按分时 / 分天配置）；
- 4G 远程控制药箱开关；
- 服药记录上传云端；
- 低电量提醒、异常开盖报警等功能。