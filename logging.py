import csv
import time
import psutil
import subprocess
import os

def get_cpu_temperature():
    try:
        with open('/sys/class/thermal/thermal_zone0/temp', 'r') as f:
            temp = float(f.read().strip()) / 1000
        return temp
    except:
        return None

def get_cpu_frequency():
    return psutil.cpu_freq().current

def get_fan_speed():
    try:
        with open('/sys/devices/platform/cooling_fan/hwmon/hwmon2/fan1_input', 'r') as f:
            fan_speed = int(f.read().strip())
        return fan_speed
    except Exception as e:
        print(f"ファンスピードの取得に失敗しました: {e}")
        return None

def log_system_info():
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    cpu_temp = get_cpu_temperature()
    cpu_freq = get_cpu_frequency()
    cpu_usage = psutil.cpu_percent()
    memory_usage = psutil.virtual_memory().percent
    fan_speed = get_fan_speed()

    if cpu_temp is not None:
        cpu_temp_str = f"{cpu_temp:.1f}"
    else:
        cpu_temp_str = "N/A"

    log_entry = [
        timestamp,
        cpu_temp_str,
        f"{cpu_freq:.0f}",
        f"{cpu_usage:.1f}",
        f"{memory_usage:.1f}",
        f"{fan_speed}"
    ]

    with open("system_log.csv", "a", newline='') as log_file:
        csv_writer = csv.writer(log_file)
        csv_writer.writerow(log_entry)

# CSVヘッダーの書き込み（初回のみ）
if not os.path.exists("system_log.csv"):
    with open("system_log.csv", "w", newline='') as log_file:
        csv_writer = csv.writer(log_file)
        csv_writer.writerow(["Timestamp", "Temperature[degC]", "CPU_Frequency[MHz]", "CPU_Usage[%]", "Memory_Usage[%]", "Fan_Speed[RPM]"])

while True:
    log_system_info()
    time.sleep(10)
