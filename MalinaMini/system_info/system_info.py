import os
import platform
import psutil
import subprocess

def get_model():
    try:
        with open('/proc/device-tree/model') as f:
            return f.read().strip()
    except Exception as e:
        return f"Error: {e}"

def get_python_version():
    return platform.python_version()

def get_ip_address():
    try:
        result = subprocess.check_output(['hostname', '-I']).decode().strip()
        return result.split()[0] if result else "No IP found"
    except Exception as e:
        return f"Error: {e}"

def get_temperature():
    try:
        result = subprocess.check_output(['vcgencmd', 'measure_temp']).decode()
        return result.replace("temp=", "").strip()
    except Exception as e:
        return f"Error: {e}"

def get_cpu_usage():
    return f"{psutil.cpu_percent()}%"

def get_memory_usage():
    mem = psutil.virtual_memory()
    return f"{mem.percent}%"

def get_disk_usage():
    disk = psutil.disk_usage('/')
    return f"{disk.percent}%"

def get_system_info():
    return {
        "model": get_model(),
        "python_version": get_python_version(),
        "ip_address": get_ip_address(),
        "temperature": get_temperature(),
        "cpu_usage": get_cpu_usage(),
        "memory_usage": get_memory_usage(),
        "disk_usage": get_disk_usage()
    }
