import Opus
import audio
import utime
import log
from machine import Pin

# 配置参数
GPIO_PIN = Pin.GPIO29
PCM_SAMPLE_RATE = 16000
OPUS_BITRATE = 10000
VOLUME_LEVEL = 8
RECORDING_DURATION = 320
READ_CHUNK_SIZE = 320

logger = log.getLogger("[TEST]")

if __name__ == "__main__":
    while True:
        try:
            logger.info("测试开始")
            
            # 初始化 PA 使能引脚
            pa_enable_pin = Pin(GPIO_PIN, Pin.OUT, Pin.PULL_DISABLE, 1)
            pa_enable_pin.write(1)
            
            # 初始化 PCM 音频设备
            pcm = audio.Audio.PCM(0, 1, PCM_SAMPLE_RATE, 2, 1, 15)
            opus = Opus(pcm, 0, 16000) 
            pcm.setVolume(VOLUME_LEVEL)
            logger.info("当前音量: %d", pcm.getVolume())
            
            # 初始化 Opus 编解码器
            # opus = Opus(pcm, 5, OPUS_BITRATE)  # 比特率范围：6000 ~ 128000
            
            buffer = []
            logger.info("开始录音")
            for i in range(40):
                data = opus.read(60)
                if not data:  # 检查读取的数据是否有效
                    logger.warning("读取数据为空，跳过当前帧")
                    continue
                buffer.append(data)
            
            logger.info("录音结束，共录制 %d 帧", len(buffer))
            
            # 回放录音数据
            logger.info("开始回放录音")
            for data in buffer:
                print("回放数据:",len(data))
                opus.write(data)
            logger.info("回放完成")
        
            utime.sleep(3)
        except Exception as e:
            logger.error("发生异常: %s", str(e))
            raise  # 可根据需求决定是否重新抛出异常
        
        finally:
            # 确保资源释放
            try:
                if 'pcm' in locals():
                    pcm.close()
                    logger.info("PCM 设备已关闭")
            except Exception as close_err:
                logger.error("关闭 PCM 设备时发生错误: %s", str(close_err))