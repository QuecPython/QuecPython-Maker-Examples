# gnss_simple_print.py
import utime
import quecgnss
from machine import Timer

# 尝试导入 math 模块，若不可用则使用 cmath 替代（适配部分 QuecPython 版本）
try:
    from math import sin, asin, cos, radians, fabs
except ImportError:
    from cmath import sin as csin, cos as ccos, pi

    def radians(x):
        return x * pi / 180.0

    def fabs(x):
        return x if x > 0 else -x

    def sin(x):
        return csin(x).real

    def cos(x):
        return ccos(x).real

    def asin(x):
        low, high = -1, 1
        while abs(high - low) > 1e-10:
            mid = (low + high) / 2.0
            if sin(mid) < x:
                low = mid
            else:
                high = mid
        return (low + high) / 2.0



def parse_nmea(raw_data):
    """解析原始 NMEA 数据，提取有效的 $GNRMC 或 $GNGGA 行"""
    lines = raw_data.split('\r\n')
    for line in lines:
        if line.startswith('$GNRMC'):
            parts = line.split(',')
            if len(parts) > 2 and parts[2] == 'A':  # A = valid
                return line, parts
        elif line.startswith('$GNGGA'):
            parts = line.split(',')
            if len(parts) > 6 and parts[6] != '0':  # satellites > 0
                return line, parts
    return None, None

def parse_nmeaGGA(raw_data):
    """解析原始 NMEA 数据，提取有效的 $GNRMC 或 $GNGGA 行"""
    lines = raw_data.split('\r\n')
    for line in lines:
        if line.startswith('$GNGGA'):
            parts = line.split(',')
            if len(parts) > 6 and parts[6] != '0':  # satellites > 0
                return line, parts
    return None, None

def convert_to_decimal(coord_str, direction, is_longitude=False):
    """将 ddmm.mmmm 或 dddmm.mmmm 转换为十进制"""
    if not coord_str or coord_str == '':
        return None
    value = float(coord_str)
    if is_longitude:
        degrees = int(value / 100)
    else:
        degrees = int(value / 100)
    minutes = value - degrees * 100
    decimal = degrees + minutes / 60.0
    if direction in ['S', 'W']:
        decimal = -decimal
    return decimal

lat, lng = 0, 0
nmea_line = None
altitude, speed, direction, time = 0, 0, 0, 0

def parse_gnss_data(args):
    global lat, lng, nmea_line, altitude, speed, direction, time
    if lat and lng:
        print("返回定位数据")
        return lat, lng , altitude, speed, direction, time


def gnss_data():
    global lat, lng , altitude, speed, direction, time
    print("Initializing GNSS...")
    if quecgnss.init() != 0:
        print("GNSS init failed!")
        return

    # if quecgnss.gnssEnable(True) != 0:
    #     print("Failed to enable GNSS!")
    #     return

    print("GNSS enabled. Waiting for fix...")

    while True:
        raw = quecgnss.read(4096)
        if raw == -1:
            utime.sleep(2)
            continue

        size, data = raw
        if not data.strip():
            utime.sleep(2)
            continue

        nmea_line, parts = parse_nmea(data)
        GGA_line, GGA_parts = parse_nmeaGGA(data)
        if nmea_line is None:
            print("No valid RMC/GGA sentence found.")
            utime.sleep(2)
            continue
        # else:
        #     print(data)


        # 提取经纬度
        # lat, lng = None, None
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

if __name__ == '__main__':
    gnss_data()