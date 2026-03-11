# 蜂窝通信体验之电话功能

该模块提供电话功能相关接口。

> - 支持voiceCall功能的模组：
>   EC600N系列：EC600NCN_LC/EC600NCN_LD/EC600NCN_LF
>   EG912N系列：EG912NEN_AA
>   EG915N系列：EG915NEU_AG/EG915NEA_AC
>   EC200A系列：EC200AAU_HA/EC200ACN_DA/EC200ACN_HA/EC200ACN_LA/EC200AEU_HA
>   EC200U系列：EC200UAU_AA/EC200UAU_AB/EC200UCN_AA/EC200UEU_AA/EC200UEU_AB
>   EC600U系列：EC600UEU_AB/EC600UEC_AC/EC600ULA_AC
>   EG912U系列：EG912UGL_AA/EG912UGL_AC
>   EG915U系列：EG915UEU_AB/EG915ULA_AB
> - BC25/BC32/EC600G/EC800G/BG95系列模组不支持voiceCall功能。
> - EC600M/EC800M/EG810M系列模组需要支持VOLTE功能固件才支持voiceCall功能。
> - 其他系列模组需要定制版本才能支持voiceCall功能。

**项目介绍**

准备工作：硬件连接、软件设计；

工程测试：根据QuecPython官方手册实现 EG915 模组的voiceCall功能；

**准备工作**

包括硬件连接、开发环境搭建、驱动设计等。

### **硬件连接**

- 将sim卡插入模组sim卡槽中
- 天线接入LTE接口
- typeC连接模组接口供电

### **开发环境搭建**

- [驱动准备 - QuecPython](https://developer.quectel.com/doc/quecpython/Getting_started/zh/4G/driver_prepare.html)
- [获取工具 - QuecPython](https://developer.quectel.com/doc/quecpython/Getting_started/zh/4G/tools_prepare.html)
- [固件烧录 - QuecPython](https://developer.quectel.com/doc/quecpython/Getting_started/zh/4G/flash_firmware.html)

### 软件设计

#### **设置自动应答时间**

```python
voiceCall.setAutoAnswer(seconds)
```

**参数描述：**

- `seconds `- 自动应答时间，整型值，单位/s，范围：0-255。

**返回值描述：**

成功返回整型 `0 `，失败返回整型 `-1 `。

> EC200U/EC600U/EG912U/EG915U系列的模组，设置的 `seconds `代表的是来电自动应答前的振铃次数。单位是“振铃次数”而不是秒。
>
> 如果是基于voLTE的IMS电话， `seconds `代表的是是否使能自动应答， `0 `:关闭自动应答； `非0 `：开启自动应答，无应答时间的设置



#### **拨打电话**

```python
voiceCall.callStart(phonenum)
```

**参数描述：**

- `phonenum `- 接收方电话号码，字符串类型。

**返回值描述：**

成功返回整型 `0 `，失败返回整型 `-1 `。



#### 接听电话 

```none
voiceCall.callAnswer()
```

该方法用于接听电话。

**返回值描述：**

成功返回整型 `0 `，失败返回整型 `-1 `。



#### 挂断电话

```none
voiceCall.callEnd()
```

**返回值描述：**

成功返回整型 `0 `，失败返回整型 `-1 `。



#### 来电自动挂断功能

```none
>>> import voiceCall
#手机呼叫模块，默认不会自动挂断
>>> voiceCall.getAutoCancelStatus()
0

#设置自动挂断功能，手机呼叫模块，默认自动挂断
>>> voiceCall.setAutoCancel(1)
0
>>> voiceCall.getAutoCancelStatus()
1
```

**参数描述：**

- `enable `- 开启或者关闭来电自动挂断功能， `1 `：开启， `0 `：关闭 (默认不开启)。

**返回值描述：**

成功返回整型 `0 `，失败返回整型 `-1 `。



```none
>>> import voiceCall
#手机呼叫模块，默认不会自动挂断
>>> voiceCall.getAutoCancelStatus()
0

#设置自动挂断功能，手机呼叫模块，默认自动挂断
>>> voiceCall.setAutoCancel(1)
0
>>> voiceCall.getAutoCancelStatus()
1
```

该方法用于获取来电自动挂断使能状态。

**返回值描述：**

`0 `：来电自动挂断使能关闭，来电不会被模组自动挂断。

`1 `：来电自动挂断使能开启，来电会被模组自动挂断。



#### DTMF识别功能

```none
voiceCall.startDtmf(dtmf, duration)
```

**参数描述：**

- `dtmf `- DTMF字符串，字符串类型，最大字符数：6个，有效字符数有： `0-9、A、B、C、D、*、# `。
- `duration `- 持续时间，整型值，范围：100-1000，单位：毫秒。

**返回值描述：**

设置成功返回整型 `0 `，设置失败返回整型 `-1 `。



```none
voiceCall.dtmfDetEnable(enable)
```

该方法用于使能DTMF识别功能，默认不开启DTMF识别。

**参数描述：**

- `enable `- 使能开关，整型值，取值 `0/1 `， `0 `：不开启DTMF识别， `1 `：开启DTMF识别。

**返回值描述：**

设置成功返回整型 `0 `，设置失败返回整型 `-1 `。



```none
voiceCall.dtmfSetCb(dtmfFun)
```

该方法用于注册DTMF识别功能的回调接口。

**参数描述：**

- `dtmfFun `- 回调函数名，回调函数格式以及回调函数的参数说明如下：



#### 设置呼叫转移

```none
voiceCall.setFw(reason, fwmode, phonenum)
```

该方法用于控制呼叫转移补充业务。

**参数描述：**

- `reason `- 呼叫转移的条件，整型值，具体如下说明：

| 值   | 参数说明   |
| ---- | ---------- |
| 0    | 无条件的   |
| 1    | 用户忙     |
| 2    | 用户无响应 |
| 3    | 用户不可达 |

- `fwMode `- 对呼叫转移的控制，整型值，具体如下说明：

| 值   | 参数说明 |
| ---- | -------- |
| 0    | 禁用     |
| 1    | 启用     |
| 2    | 查询状态 |
| 3    | 注册     |
| 4    | 擦除     |

- `phonenum `- 呼叫转移的目标电话，字符串类型

**返回值描述：**

设置成功返回整型 `0 `，设置失败返回整型 `-1 `。



#### 切换语音通道

```none
voiceCall.setChannel(device)
```

**参数描述：**

- `device `- 输出通道，整型值，具体如下说明：
- 0：听筒，1：耳机，2：喇叭

**返回值描述：**

设置成功返回整型 `0 `，设置失败返回整型 `-1 `。



#### 音量大小配置

```none
voiceCall.getVolume()
```

该方法用于获取电话当前音量大小。

**返回值描述：**

返回整型音量值。



```none
voiceCall.setVolume(volume)
```

该方法用于设置电话音量大小。

**参数描述:**

- `volume `- 音量等级，整型值，范围 `（0 ~ 11） `，数值越大，音量越大。

**返回值描述：**

设置成功返回整型 `0 `，失败返回整型 `-1 `。



#### 自动录音功能

```none
voiceCall.setAutoRecord(enable, recordType, recordMode, filename)
```

该接口用于使能自动录音功能。默认关闭自动录音，自动录音使能需要在通话前设置完毕。

**参数描述：**

- `enable `- 使能开关，整型值，取值0或1， `0 `：关闭自动录音功能 ， `1 `：开启自动录音功能。
- `recordType `- 录音文件类型，整型值，0：AMR，    1：WAV

| 值   | 说明                                                 |
| ---- | ---------------------------------------------------- |
| 0    | 表示录制的是下行链路通道的音频数据，即对端的声音。   |
| 1    | 表示录制的是上行链路通道的音频数据，即本端的声音。   |
| 2    | 表示录制的是上行链路通道和下行链路通道的混合音频流。 |

- `filename `- 期望存储的文件名，字符串类型，需包含完整路径。

**返回值描述：**

设置成功返回整型 `0 `，设置失败返回整型 `-1 `， 不支持该接口返回字符串 `"NOT SUPPORT" `。



保存代码文件为 `test.py` ；

通过[教程](https://developer.quectel.com/doc/quecpython/Getting_started/zh/4G/first_python.html)将脚本下载到开发板中：

![](C:\Users\Aaron.chen\AppData\Roaming\Typora\typora-user-images\image-20260304153631181.png)

**运行效果：**









