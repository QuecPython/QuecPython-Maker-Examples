# EC800X Duino 开发板 MQTT 远程控制 LED 灯

## 项目简介

本项目基于移远**EC800X Duino**开发板，采用 **QuecPython** 开发方式，通过 **MQTTS 加密通信协议**连接 ConnectLab 管理系统 MQTT 服务器，实现**云端下发指令远程控制 LED 灯亮灭**的物联网基础应用。

设备订阅指定主题后，可实时接收云端指令，当收到 `led` 指令时自动点亮 LED 灯，3 秒后自动熄灭，完整演示物联网 “云端指令下发 — 设备解析执行” 的核心流程。

## 功能特性

- ✅ MQTTS 加密通信，数据传输安全可靠
- ✅ 云端指令远程控制硬件 LED 灯
- ✅ 自动解析指令，`led` 指令触发亮灯 3 秒后自动熄灭
- ✅ 支持消息订阅、消息发布、实时监听
- ✅ 适配 EC800X Duino 开发板，即刷即用
- ✅ 代码简洁易懂，适合物联网初学者入门学习

## 硬件准备

|      硬件设备       |          说明          |
| :-----------------: | :--------------------: |
| EC800X Duino 开发板 |       主控制平台       |
|    Type‑C 数据线    |       供电与调试       |
| 物联网 Nano SIM 卡  | 蜂窝网络接入（已激活） |
|      外置天线       |      增强网络信号      |

## 软件环境

- QuecPython 开发环境
- QPYcom 调试工具
- ConnectLab 管理系统（MQTTS 服务器）

## 引脚定义

- LED 控制引脚：**GPIO31**
- 电平逻辑：**低电平点亮，高电平熄灭**（共阳极 LED）

## MQTT 服务器信息

|      参数       |        配置值         |
| :-------------: | :-------------------: |
|   服务器地址    |   `101.37.104.185`    |
|     端口号      |        `41094`        |
|     用户名      |       `quectel`       |
|      密码       |      `12345678`       |
| 订阅 / 发布主题 | `/public/TEST/python` |
|    加密方式     |   MQTTS（SSL 加密）   |

## 项目代码

```python
from umqtt import MQTTClient
import utime
import log
from machine import Pin

# 全局状态与 MQTT 登录信息
state = 0
usrname = "quectel"
password = "12345678"

# GPIO31 初始化：输出模式，初始高电平（LED 熄灭）
gpio1 = Pin(Pin.GPIO31, Pin.OUT, Pin.PULL_DISABLE, 1)

# MQTT 消息回调函数：处理云端下发指令
def sub_cb(topic, msg):
    data = msg.decode()
    print("收到消息：", data)
    
    # 判断是否为 LED 控制指令
    if data == "led":
        gpio1.write(0)       # 低电平 → 点亮 LED
        print("led open...")
        utime.sleep(3)       # 保持亮灯 3 秒
        gpio1.write(1)       # 高电平 → 熄灭 LED

if __name__ == '__main__':
    try:
        # 创建 MQTTS 客户端（SSL 加密连接）
        c = MQTTClient("umqtt_client", "101.37.104.185", 41094, usrname, password, ssl=True)
        c.set_callback(sub_cb)        # 设置消息回调
        c.connect()                   # 连接服务器
        c.subscribe("/public/TEST/python")  # 订阅主题
        c.publish("/public/TEST/python", "my name is Quecpython!")  # 上线消息
        print("MQTT 连接成功，开始监听指令...")

        # 循环等待云端消息
        while True:
            c.wait_msg()
            utime.sleep(1)
            
    except KeyboardInterrupt as e:
        c.disconnect()   # 断开 MQTT 连接
        print("MQTT 已断开")
```

## 运行步骤

1. 将 SIM 卡、天线正确安装到 EC800X Duino 开发板
2. 使用 Type‑C 线连接开发板与电脑
3. 打开 QPYcom 工具，将代码下载到开发板并运行
4. 查看日志，确认打印 `MQTT 连接成功，开始监听指令...`
5. 在 ConnectLab 管理系统向主题 `/public/TEST/python` 发布消息：`led`
6. 观察开发板 LED 灯：**收到指令 → 点亮 → 3 秒后自动熄灭**

## 工作原理

1. **网络通信**：EC800X Duino 模组注册蜂窝网络，接入互联网
2. **MQTTS 连接**：设备使用 SSL 加密方式连接 ConnectLab MQTT 服务器，完成身份验证
3. **主题订阅**：设备订阅 `/public/TEST/python` 主题，实时监听云端指令
4. **指令解析**：当云端发布 `led` 消息时，设备回调函数自动解析并识别指令
5. **硬件控制**：GPIO31 输出低电平点亮 LED，延时 3 秒后输出高电平熄灭 LED
6. **循环监听**：设备持续等待消息，支持多次远程重复控制

## 常见问题排查

- MQTT 连接失败：检查 SIM 卡信号、服务器地址、端口、用户名密码
- LED 不亮：确认 GPIO31 接线 / 硬件对应关系，检查电平逻辑是否正确
- 收不到消息：确认主题名称完全一致，网络已正常连接
- 程序异常退出：增加异常捕获，确保 MQTT 正常断开

## 适用人群

- 物联网入门初学者
- QuecPython 开发者
- 电子技术爱好者
- 教学实验与课程设计

## 总结

本项目是物联网入门级经典案例，通过 **MQTT + 云端指令 + GPIO 硬件控制** 的完整流程，帮助你快速掌握物联网设备与云端交互的核心原理，可扩展为远程开关、环境监测、智能家居等更多物联网应用。