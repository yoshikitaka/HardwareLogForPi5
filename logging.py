import csv
import time
import psutil
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
    cpu_usage = psutil.cpu_percent(interval=1)  # 1秒間のCPU使用率を測定
    memory_usage = psutil.virtual_memory().percent
    fan_speed = get_fan_speed()

    cpu_temp_str = f"{cpu_temp:.1f}" if cpu_temp is not None else "N/A"

    log_entry = [
        timestamp,
        cpu_temp_str,
        f"{cpu_freq:.0f}",
        f"{cpu_usage:.1f}",
        f"{memory_usage:.1f}",
        f"{fan_speed}"
    ]

    log_file_path = os.path.join(os.path.dirname(__file__), "system_log.csv")
    file_exists = os.path.exists(log_file_path)

    with open(log_file_path, "a", newline='') as log_file:
        csv_writer = csv.writer(log_file)
        if not file_exists:
            csv_writer.writerow(["Timestamp", "Temperature[degC]", "CPU_Frequency[MHz]", "CPU_Usage[%]", "Memory_Usage[%]", "Fan_Speed[RPM]"])
        csv_writer.writerow(log_entry)

if __name__ == "__main__":
    log_system_info()
