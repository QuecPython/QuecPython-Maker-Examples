# 初学者视角体验：【C1-PO2开发板】驱动舵机超简单！



## 项目介绍：

本文介绍了 **C1-PO2开发板搭载 EG915UEU_AB** 模组结合PWM模块实现M**G90S舵机驱动**的项目设计，帮助初学者快速上手基于 QuecPython 的硬件外设功能开发。

## 硬件连接：

以下表格为硬件与开发板的对应连接关系

| 硬件       | 开发板  |
| ---------- | ------- |
| 舵机电源线 | 5.5V    |
| 舵机地线   | GND     |
| 舵机控制线 | PWM0    |
| USB        | USB接口 |



### 开发环境搭建

复用 QuecPython 基础开发环境，步骤如下：

1. 驱动准备：参考[QuecPython 驱动准备教程](https://developer.quectel.com/doc/quecpython/Getting_started/zh/4G/driver_prepare.html)配置基础驱动；
2. 工具获取：下载[QuecPython 开发工具](https://developer.quectel.com/doc/quecpython/Getting_started/zh/4G/tools_prepare.html)（如 QPYcom），用于代码下载与调试；
3. 固件烧录：确保开发板烧录支持音频 / SPI 功能的 QuecPython 固件，参考[固件烧录教程](https://developer.quectel.com/doc/quecpython/Getting_started/zh/4G/flash_firmware.html)。

### 播放逻辑设计

该函数实现平滑移动控制：

1. 在steps+1个步长内，从start0线性过渡到end；
2. 每步调用pwmx.open设置位置，并延时20毫秒。

```python
def smooth_move(pwmx,start0,end,steps=5):
    for i in range(steps+1):
        pwmx.open(100.0,start0+int((end-start0)/(steps)*i)) 
        utime.sleep_ms(20)
```

### 代码使用说明：

1. 保存代码文件为 `SG90.py`；
2. 参考[教程](https://developer.quectel.com/doc/quecpython/Getting_started/zh/index.html)，通过QPYcom把该脚本下载至模组中；
3. 点击运行脚本

## 工程测试：

1. 硬件连接完成后，通过 QPYcom 工具将`SG90.py`下载到开发板；

2. 运行脚本，观察舵机是否转动

3. 调试要点：

   - 若现象，检查电源、引脚连接是否正确；

     

## 运行效果：

- 开发板终端无打印

- 舵机向左旋转到极限再向右旋转到极限最后再回到中间位置。

  

## 总结：

对于初学者而言，本项目不仅能快速掌握 PWM 信号输出、硬件外设连接等基础硬件开发技能，还能熟悉 QuecPython 的代码编写、调试及脚本下载部署流程，为后续基于该开发板拓展更多物联网应用（如智能云台、机械臂控制、智能家居执行机构驱动等）奠定了坚实基础。