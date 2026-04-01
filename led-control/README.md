# 移远 BG95 开发板 LED 灯控制（Python）

## 项目介绍

基于移远**BG95 开发板**，通过 Python 控制 GPIO 引脚实现 LED 灯的亮灭操作，适用于物联网终端、智能设备等嵌入式开发场景。

## 硬件信息

- 主控平台：移远 BG95 模块
- 控制引脚：GPIO19
- 外设：LED 灯
- 模式：输出、浮空模式、默认高电平

## 代码实现

```python
# 导入I/O引脚控制模块
from machine import Pin

# 创建GPIO对象，配置引脚为输出、浮空模式，默认高电平
gpio1 = Pin(Pin.GPIO19, Pin.OUT, Pin.PULL_DISABLE, 1)

# 设置低电平，LED亮灯
gpio1.write(0)
```

## 代码说明

1. **导入库**：从 machine 模块导入 Pin，用于 GPIO 引脚控制

2. GPIO 初始化

   - 引脚：GPIO19
   - 模式：输出模式（OUT）
   - 上下拉：禁用上下拉（PULL_DISABLE，浮空模式）
   - 默认电平：高电平（1）

   

3. **LED 控制**：输出低电平（0）时 LED 点亮

## 注意事项

- 确保 BG95 开发板 GPIO19 引脚与 LED 硬件连接正确
- 确认开发环境支持 MicroPython/Python 固件运行
- 电平逻辑：高电平灭灯，低电平亮灯