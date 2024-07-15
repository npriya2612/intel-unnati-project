import psutil
import json
import datetime
import os

DATA_FILE = 'all_data.json'

def collect_metrics():
    metrics = {
        'cpu_percent': psutil.cpu_percent(interval=1),
        'memory_percent': psutil.virtual_memory().percent,
        'disk_io_gb': psutil.disk_io_counters().read_bytes / (1024 ** 3),
        'timestamp': datetime.datetime.now().isoformat()
    }
    
    save_metrics(metrics)
    return metrics

def save_metrics(metrics):
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as file:
            data = json.load(file)
    else:
        data = []

    data.append(metrics)
    
    with open(DATA_FILE, 'w') as file:
        json.dump(data, file, indent=4)

def compute_averages(metrics_list):
    if not metrics_list:
        return {
            'cpu_percent': 0,
            'memory_percent': 0,
            'disk_io_gb': 0
        }
    
    total_cpu = sum(metric['cpu_percent'] for metric in metrics_list)
    total_memory = sum(metric['memory_percent'] for metric in metrics_list)
    total_disk_io = sum(metric['disk_io_gb'] for metric in metrics_list)

    count = len(metrics_list)
    
    return {
        'cpu_percent': total_cpu / count,
        'memory_percent': total_memory / count,
        'disk_io_gb': total_disk_io / count
    }

def estimate_energy_usage(metrics_list):
    average_metrics = compute_averages(metrics_list)
    
    # Simplified energy usage estimation
    cpu_power = 50  # Example power usage in watts
    memory_power = 20  # Example power usage in watts
    disk_power = 10  # Example power usage in watts

    estimated_energy_usage = (average_metrics['cpu_percent'] / 100 * cpu_power) + \
                             (average_metrics['memory_percent'] / 100 * memory_power) + \
                             (average_metrics['disk_io_gb'] / 100 * disk_power)

    return estimated_energy_usage

def load_metrics():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as file:
            return json.load(file)
    return []
