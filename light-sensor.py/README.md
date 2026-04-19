# 移远 EC800X Duino 开发板光照传感器体验

## 项目介绍

基于移远**EC800X Duino 开发板**，通过 ADC 模拟信号采集实现光敏电阻传感器的光线强度检测，结合 GPIO 控制 LED 灯的亮灭，适用于物联网终端、智能照明、环境光感监测等嵌入式开发场景。

## 硬件信息

- 主控平台：移远 EC800X Duino 开发板

  光敏电阻传感器：

  - 模拟信号输出引脚接 EC800X Duino 开发板 ADC1 通道
  - LED 控制引脚：GPIO31（输出模式）

  电源：光敏电阻传感器接开发板 3.3V/5V，地线接 GND

## 代码实现

```python

from misc import ADC
from machine import Pin
import _thread
import utime
from misc import PWM_V2

def fun():
    while True:
        num=adc.read(adc.ADC1)
        utime.sleep(1)#出现具体电压值，通过电压值控制占空比
        print(num)
        return num

def LED_SW(num):
    if num<50:
        LED.write(1)
        print("光线较强")
    else:
        LED.write(0)
        print("光线较弱")

if __name__=='__main__':
    LED=Pin(Pin.GPIO31,Pin.OUT,Pin.PULL_DISABLE,0)
    adc = ADC()
    adc.open()
    _thread.start_new_thread(fun,())
    while True:
        num=fun()        
        LED_SW(num)

```

## 代码说明

**导入模块**：引入 Pin（GPIO 控制）、ADC（模拟信号采集）、utime（延时）、_thread（多线程）核心模块；

**核心函数 - read_light_intensity**：

- 循环读取 ADC1 通道的模拟值（光敏电阻的电压转换值）；
- 数值越小表示光线越强（光敏电阻阻值随光线增强而减小，对应电压降低）；
- 1 秒采集一次数据，可根据需求调整采样频率；

**核心函数 - LED_control**：

- 接收 ADC 采集值，通过阈值（50）判断光线强度；
- 光线较强（num < 50）：LED 关闭（GPIO31 输出 1）；
- 光线较弱（num ≥ 50）：LED 打开（GPIO31 输出 0）；

**初始化配置**：

- LED 引脚（GPIO31）配置为输出模式，禁用上下拉电阻，初始电平 0；
- 初始化并打开 ADC 模块，用于采集光敏电阻的模拟信号；

**主循环逻辑**：

- 启动子线程辅助读取光线强度（可选，单线程也可运行）；
- 主循环持续读取光线值，调用 LED 控制函数，实现光线强度与 LED 联动。

## 注意事项

1. **硬件接线**：

   - 光敏电阻传感器的模拟输出引脚必须接开发板 ADC1 通道（需确认开发板 ADC 通道定义）；
   - LED 正极串接限流电阻（如 220Ω）后接 GPIO31，负极接 GND；
   - 确保传感器电源、地线接线牢固，避免接触不良导致数据异常；

2. **阈值调整**：

   - 代码中阈值 50 为参考值，需根据实际硬件（光敏电阻型号、分压电路）调整；
   - 可通过串口打印的 ADC 值，测试不同光线环境下的数值范围，再优化阈值；

3. **ADC 数值与电压转换**：

   - EC800X Duino 的 ADC 量程通常为 0-4095（12 位），对应电压 0-3.3V；
   - 电压计算公式：实际电压 = (ADC 数值 / 4095) * 3.3，可根据电压值更精准控制；

4. **多线程说明**：

   - 代码中启用了子线程读取数据，若无需多线程，可直接删除 `_thread.start_new_thread` 相关代码，仅保留主循环调用；

5. **采样频率**：

   - `utime.sleep(1)` 控制采样间隔，缩短延时（如 0.5 秒）可提升检测灵敏度，但会增加串口打印频率；

6. **防抖处理**：

   - 若光线检测出现频繁跳变，可在 

     ```
     read_light_intensity
     ```

      中增加多次采样取平均值的逻辑，示例：

     ```python
     def read_light_intensity():
         global adc
         total = 0
         # 连续采集5次取平均值
         for _ in range(5):
             total += adc.read(adc.ADC1)
             utime.sleep_ms(20)
         num = total // 5
         utime.sleep(1)
         print("当前光线ADC值（平均值）："，num)
         return num
     ```