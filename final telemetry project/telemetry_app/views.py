from django.shortcuts import render
import psutil
import json
import pythoncom
import wmi
from django.http import JsonResponse
import docker
import time
from datetime import datetime

# Function to query power consumption using WMI
def query_power_consumption():
    try:
        pythoncom.CoInitialize()
        c = wmi.WMI()
        total_power_consumption = 0.0

        for cpu in c.Win32_Processor():
            power_consumption = cpu.CurrentVoltage * cpu.CurrentClockSpeed * cpu.NumberOfCores
            total_power_consumption += power_consumption
        
        return total_power_consumption
    except Exception as e:
        print(f"Error querying power consumption: {e}")
        return None
    finally:
        pythoncom.CoUninitialize()

# Function to save telemetry data to JSON file
def save_telemetry_data(data):
    try:
        with open('previous_telemetry.json', 'a+') as file:
            file.seek(0)
            contents = file.read()
            if contents:
                file.write(',')
            json.dump(data, file)
            file.write('\n')
        print(f"Telemetry data saved: {data}")
    except Exception as e:
        print(f"Error saving telemetry data: {e}")

# Function to load telemetry data from JSON file
def load_telemetry_data():
    try:
        with open('previous_telemetry.json', 'r') as file:
            data = [json.loads(line) for line in file.readlines()]
        return data
    except FileNotFoundError:
        print("No previous telemetry data found.")
        return []
    except Exception as e:
        print(f"Error loading telemetry data: {e}")
        return []

# View to fetch and display the most recent telemetry data on index.html
def index(request):
    try:
        telemetry_data = load_telemetry_data()
        if telemetry_data:
            latest_data = telemetry_data[-1]
        else:
            latest_data = {
                'cpu': None,
                'memory': None,
                'disk': None,
                'energy_watts': None
            }
        
        return render(request, 'telemetry_app/index.html', {'telemetry_data': latest_data})
    except Exception as e:
        error_message = f"Error loading telemetry data: {e}"
        return render(request, 'telemetry_app/index.html', {'error': error_message})

# View to display previous telemetry data
def previous_data_view(request):
    try:
        telemetry_data = load_telemetry_data()
        data = {'telemetry_data': telemetry_data}
        return render(request, 'telemetry_app/previous_data.html', data)
    except Exception as e:
        error_message = f"Error loading previous telemetry data: {e}"
        return render(request, 'telemetry_app/previous_data.html', {'error': error_message})

# View to collect data and save to JSON file
def collect_data(request):
    try:
        cpu_usage = psutil.cpu_percent()
        memory_usage = psutil.virtual_memory().percent
        disk_usage = psutil.disk_usage('/').percent
        energy_usage = query_power_consumption()

        telemetry_data = {
            'cpu': cpu_usage,
            'memory': memory_usage,
            'disk': disk_usage,
            'energy_watts': energy_usage
        }

        save_telemetry_data(telemetry_data)

        return render(request, 'telemetry_app/index.html', {'telemetry_data': telemetry_data})
    except Exception as e:
        error_message = f"Error collecting or saving telemetry data: {e}"
        return render(request, 'telemetry_app/index.html', {'error_message': str(e)})

# View to fetch and return all telemetry data as JSON
def telemetry_results(request):
    try:
        telemetry_data = load_telemetry_data()
        return JsonResponse(telemetry_data, safe=False)
    except FileNotFoundError:
        return JsonResponse({'error': 'Telemetry data file not found'}, status=404)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Error decoding telemetry data JSON'}, status=500)

# Function to collect system metrics for power utilization
def collect_metrics(duration):
    import time
    start_time = time.time()
    end_time = start_time + duration
    metrics = {
        'cpu_percent': [],
        'disk_io': [],
        'memory_percent': []
    }

    while time.time() < end_time:
        cpu_percent = psutil.cpu_percent(interval=1)
        disk_io = psutil.disk_io_counters().write_bytes
        memory_percent = psutil.virtual_memory().percent

        metrics['cpu_percent'].append(cpu_percent)
        metrics['disk_io'].append(disk_io)
        metrics['memory_percent'].append(memory_percent)

    return metrics

def compute_averages(metrics):
    avg_cpu = sum(metrics['cpu_percent']) / len(metrics['cpu_percent'])
    avg_disk_io = sum(metrics['disk_io']) / len(metrics['disk_io'])
    avg_memory = sum(metrics['memory_percent']) / len(metrics['memory_percent'])
    return {
        'cpu_percent': avg_cpu,
        'disk_io_gb': avg_disk_io / (1024**3),
        'memory_percent': avg_memory
    }

def estimate_energy_usage(metrics):
    avg_cpu = metrics['cpu_percent']
    avg_disk_io = metrics['disk_io_gb']
    avg_memory = metrics['memory_percent']

    avg_power_cpu = avg_cpu * 0.3
    avg_power_disk = avg_disk_io * 2e-12
    avg_power_memory = avg_memory * 3 / 8
    avg_energy_usage = avg_power_cpu + avg_power_disk + avg_power_memory
    return avg_energy_usage

# Function to generate optimization tips based on telemetry data
def generate_optimization_tips(telemetry_data):
    tips = {
        'cpu_tips': [],
        'memory_tips': [],
        'disk_tips': [],
        'energy_tips': [],
        'general_tips': []
    }
    if telemetry_data['Average CPU Percent'] > 75:
        tips['cpu_tips'].append("Consider closing unnecessary applications to reduce CPU usage.")
    else:
        tips['cpu_tips'].append("Your CPU usage is optimal.")

    if telemetry_data['Average Memory Percent'] > 80:
        tips['memory_tips'].append("Upgrade your RAM or close memory-intensive applications to improve performance.")
    else:
        tips['memory_tips'].append("Your memory usage is optimal.")

    if telemetry_data['Average Disk IO (GB)'] > 100:
        tips['disk_tips'].append("Optimize your disk usage by deleting unused files or moving data to an external storage.")
    else:
        tips['disk_tips'].append("Your disk I/O usage is optimal.")

    if telemetry_data['Estimated Energy Usage'] > 50:
        tips['energy_tips'].append("Consider upgrading to more energy-efficient hardware to reduce power consumption.")
    else:
        tips['energy_tips'].append("Your energy usage is optimal.")

    tips['general_tips'].extend([
        "Regularly update your software and drivers to ensure optimal performance.",
        "Clean your computer hardware regularly to prevent dust buildup.",
        "Use power-saving settings on your computer to reduce energy consumption."
    ])

    return tips

# View to collect system metrics for power utilization and save to JSON file
def power_utilization(request):
    try:
        duration = 60
        metrics = collect_metrics(duration)
        average_metrics = compute_averages(metrics)
        estimated_energy_usage = estimate_energy_usage(average_metrics)

        telemetry_data = {
            'Average CPU Percent': average_metrics['cpu_percent'],
            'Average Disk IO (GB)': average_metrics['disk_io_gb'],
            'Average Memory Percent': average_metrics['memory_percent'],
            'Estimated Energy Usage': estimated_energy_usage
        }

        # Generate optimization tips based on telemetry data
        tips = generate_optimization_tips(telemetry_data)

        # Save the telemetry data
        save_telemetry_data(telemetry_data)

        return render(request, 'telemetry_app/power_utilization.html', {
            'avg_cpu': average_metrics['cpu_percent'],
            'avg_disk_io': average_metrics['disk_io_gb'],
            'avg_memory': average_metrics['memory_percent'],
            'avg_energy_usage': estimated_energy_usage,
            'tips': tips
        })
    except Exception as e:
        error_message = f"Error collecting power utilization data: {e}"
        return render(request, 'telemetry_app/power_utilization.html', {'error': error_message})
