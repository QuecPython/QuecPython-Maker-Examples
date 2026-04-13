# EC800X Duino  开发板-水位检测传感器

## 项目介绍

基于移远**EC800X Duino 开发板**，通过 ADC 实现火焰检测（火焰传感器信号采集），适用于物联网终端、智能安防等嵌入式开发场景。

## 硬件信息

- 主控平台：移远 EC800X Duino 开发板 
- 火焰传感器引脚：ADC1

## 代码实现

```python
from misc import ADC
from machine import Pin
import _thread
import utime

def fun():
    while True:
        num=adc.read(adc.ADC1)
        utime.sleep(1)
        print(num)

    
if __name__=='__main__':
    adc = ADC()
    adc.open()
    _thread.start_new_thread(fun,())
```

## 代码说明

1. 导入模块

2. 定义循环采集函数

3. 初始化并打开 ADC

4. 用线程后台启动采集

5. 每秒读取并打印 ADC 值


## 注意事项

- 确保硬件接线正确：

  - 火焰传感器的信号引脚接 EC800X Duino 开发板ADC1；

  实际部署时可根据需求调整检测间隔（`time.sleep()` 参数）。