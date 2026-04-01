# 初学者视角的试用：【QEM820MA-CN】轻松查询天气情况！

**【QEM820MA-CN】轻松查询天气情况**

本文基于移远 QEM820MA-CN 开发板 + QuecPython 实现**网络天气查询**功能，通过 HTTP 请求获取公开天气数据，帮助物联网初学者快速掌握网络请求、数据解析与日志打印，零基础也能快速跑通物联网联网开发。

## 项目介绍：

本项目基于 **QEM820MA-CN 开发板** 实现 HTTP 网络请求功能，通过调用公共天气 API 获取城市实时天气信息，完成**网络初始化 → HTTP GET 请求 → 数据接收 → 结果打印**全流程，是物联网设备联网、数据上报、远程查询类项目的入门基础案例，适用于环境监测、智慧屏、便携气象站等场景快速开发。

### 硬件连接

1. SIM 卡插入设备卡槽（确保已开通流量、正常注网）
2. Type-C USB 连接设备与主机

### 开发环境搭建

复用 QuecPython 基础开发环境，步骤如下：

1. 驱动准备：参考[QuecPython 驱动准备教程](https://developer.quectel.com/doc/quecpython/Getting_started/zh/4G/driver_prepare.html)配置基础驱动；
2. 工具获取：下载[QuecPython 开发工具](https://developer.quectel.com/doc/quecpython/Getting_started/zh/4G/tools_prepare.html)（如 QPYcom），用于代码下载与调试；
3. 固件烧录：确保开发板烧录支持 **HTTP / 网络功能** 的官方固件，参考[固件烧录教程](https://developer.quectel.com/doc/quecpython/Getting_started/zh/4G/flash_firmware.html)。

### 播放逻辑设计

本项目基于移远官方 **HTTP 协议开发指南**实现：

```python
import request
import utime
import json
import _thread

# 天气API接口（免费公共接口）
WEATHER_API_URL = "https://api.vvhan.com/api/weather?city=beijing"

def get_weather():
    print("=== 开始获取天气信息 ===")
    try:
        # 发送HTTP GET请求
        resp = request.get(WEATHER_API_URL)
        # 获取返回文本数据
        data = resp.text
        print("获取成功，原始数据：\n", data)
        
        # 可选：JSON解析（如果API返回json格式）
        # json_data = json.loads(data)
        # print("城市：", json_data["city"])
        # print("天气：", json_data["weather"])
        # print("温度：", json_data["temperature"])
        
    except Exception as e:
        print("天气查询失败：", e)
    
    print("=== 查询结束 ===")

# 启动独立线程运行网络请求
_thread.start_new_thread(get_weather, ())

# 主循环保持程序运行
while True:
    utime.sleep(1)
```

### 代码使用说明：

1. 保存代码文件为 `WeatherQuery.py`
1. 通过QPYcom把该脚本下载至模组中；
1. 点击运行脚本

## 工程测试：

1. 确认 SIM 卡插入正常，设备成功**注网**

2. 通过 QPYcom 下载并运行 `WeatherQuery.py`

3. 查看终端日志，观察是否成功获取天气信息

4. 常见问题排查：
   - 请求失败：检查信号、SIM 流量、网络是否可用
   - 无返回：确认 API 地址可正常访问
   - 报错重启：增加异常捕获处理



## 运行效果：

- 终端打印：`=== 开始获取天气信息 ===`

- 自动打印获取到的**城市、天气、温度、风向**等信息

- 最终打印：`=== 查询结束 ===`

  

## 总结：

本文基于 **QEM820MA-CN 开发板** 完成 HTTP 天气查询实战，完整演示了 QuecPython 网络请求开发流程，是物联网联网开发的必备基础案例。