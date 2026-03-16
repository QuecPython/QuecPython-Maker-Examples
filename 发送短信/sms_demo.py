import sms
import utime
import log

# 基础配置
log.basicConfig(level=log.INFO)
sms_log = log.getLogger("SMS")
TARGET_PHONE = "13532640348"  # 替换为接收号码
TEST_MSG = "QuecPython短信测试！"  # 短信内容（中文/英文都可）

# 初始化：注册接收短信回调
def sms_receive_callback(args):
    """收到新短信自动触发"""
    sim_id, sms_index, _ = args
    # 读取短信内容
    content = sms.searchTextMsg(sms_index)
    if content != -1:
        sender, msg, _ = content
        sms_log.info("收到短信：发件人[{}]，内容：{}".format(sender, msg))

# 注册接收回调
sms.setCallback(sms_receive_callback)
sms_log.info("短信功能初始化完成")

def send_sms(phone, msg):
    """发送短信（中文默认UCS2编码）"""
    sms_log.info("发送短信到 {}：{}".format(phone, msg))
    ret = sms.sendTextMsg(phone, msg, "UCS2")
    if ret == 0:
        sms_log.info("短信发送成功！")
    else:
        sms_log.info("发送失败，错误码：{}".format(ret))

# 主逻辑
if __name__ == "__main__":
    # 1. 发送一条测试短信
    send_sms(TARGET_PHONE, TEST_MSG)
    utime.sleep(2)
    
    # 2. 保持运行，监听新短信（收到会自动打印）
    sms_log.info("等待接收短信...（按Ctrl+C退出）")
    while True:
        utime.sleep(1)