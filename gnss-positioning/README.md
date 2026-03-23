# 初学者视角体验：【C1-P02开发板】轻松玩转GNSS定位！

## 项目介绍：

本文围绕 搭载**EG912UGL AA**模组的**C1-P02**开发板展开实战讲解，聚焦板载 GNSS 定位模块的硬件接线、参数配置与数据解析，手把手带你实现定位信息获取、经纬度解析等核心功能，帮助初学者快速上手基于 QuecPython 的 GNSS 定位开发，轻松玩转卫星定位应用。



## 硬件连接：

包括硬件连接：

1.天线连接开发板GNSS底座

2.USB连接主机与开发板



### 开发环境搭建

复用 QuecPython 基础开发环境，步骤如下：

1. 驱动准备：参考[QuecPython 驱动准备教程](https://developer.quectel.com/doc/quecpython/Getting_started/zh/4G/driver_prepare.html)配置基础驱动；
2. 工具获取：下载[QuecPython 开发工具](https://developer.quectel.com/doc/quecpython/Getting_started/zh/4G/tools_prepare.html)（如 QPYcom），用于代码下载与调试；
3. 固件烧录：确保开发板烧录支持GNSS功能的 QuecPython 固件，参考[固件烧录教程](https://developer.quectel.com/doc/quecpython/Getting_started/zh/4G/flash_firmware.html)。



### 经纬度提取逻辑设计

以下为基于GNSS原始数据中提取经纬度的功能：

```python
        if parts[0].startswith('$GNRMC'):
            # RMC: $GNRMC,hhmmss.ss,A,llll.ll,a,yyyyy.yy,a,x.x,x.x,ddmmyy,x.x,E,A*hh
            lat = convert_to_decimal(parts[3], parts[4], is_longitude=False)
            lng = convert_to_decimal(parts[5], parts[6], is_longitude=True)
            speed = float(parts[7]) if parts[7] else 0   # 速度，单位：节
            direction = float(parts[8]) if parts[8] else 0 # 方向，单位：度
        	time = parts[9]
            if GGA_line is not None:
                # print("GGAaaa:", GGA_line)
                altitude = GGA_parts[9] if GGA_parts[9] else 0  # 海拔，单位：米
        elif parts[0].startswith('$GNGGA'):
            # GGA: $GNGGA,hhmmss.ss,llll.ll,a,yyyyy.yy,a,x,xx,x.x,x.x,M,x.x,M,x.x,xxxx*hh
            lat = convert_to_decimal(parts[2], parts[3], is_longitude=False)
            lng = convert_to_decimal(parts[4], parts[5], is_longitude=True)

        if lat is not None and lng is not None:
            # pass
            print("[GNSS FIX] Latitude: {}, Longitude: {}".format(lat, lng))
            # print("Raw NMEA: Speed: {}, Direction: {}, Altitude: {}, Time: {}".format(speed, direction, altitude, time))
        else:
            print("Failed to parse coordinates.")
        utime.sleep(3)
```

### 代码使用说明：

1. 保存代码文件为 `GNSS.py`；
2. 参考[教程](https://developer.quectel.com/doc/quecpython/Getting_started/zh/index.html)，通过QPYcom把该脚本下载至模组中；
3. 点击运行脚本

## 工程测试：

1. 硬件连接完成后，通过 QPYcom 工具将`GNSS.py`下载到开发板；
2. 运行脚本，观察终端是否打印经纬度信息；
3. 调试要点：

   - 若长时间无信息，查看开发板上的GNSS底座是否安装了天线；

## 运行效果：

- 开发板终端打印：开始运行时出现`No valid RMC/GGA sentence found.`是正常的，gnss冷启动需要1-5分钟获取定位信息，程序刚运行时可能会上传空定位信息至服务器，有真实数据后会定时自动上传
- 有真实数据后会正常在终端打印

## 总结：

整体而言，C1-P02 开发板的 GNSS 功能具备易上手、易调试、稳定性强的特点，结合 QuecPython 的轻量化开发优势，非常适合物联网初学者入门卫星定位技术，也为小型物联网项目的快速落地提供了高效的实现路径。