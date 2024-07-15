import platform
import psutil
import json
import os
import datetime

# Function to collect CPU and memory data
def collect_cpu_memory_data():
    cpu_usage = psutil.cpu_percent(interval=1)
    cpu_frequency = psutil.cpu_freq()
    memory_info = psutil.virtual_memory()

    cpu_data = {
        "cpu_usage_percent": cpu_usage,
        "cpu_frequency": cpu_frequency.current,
        "cpu_frequency_max": cpu_frequency.max,
        "cpu_frequency_min": cpu_frequency.min
    }

    memory_data = {
        "memory_usage_percent": memory_info.percent,
        "memory_total": memory_info.total,
        "memory_used": memory_info.used,
        "memory_free": memory_info.available
    }

    return cpu_data, memory_data

# Function to collect network data
def collect_network_data():
    network_info = psutil.net_io_counters()

    network_data = {
        "bytes_sent": network_info.bytes_sent,
        "bytes_received": network_info.bytes_recv,
        "packets_sent": network_info.packets_sent,
        "packets_received": network_info.packets_recv
    }

    return network_data

# Function to query energy consumption using WMI (Windows Management Instrumentation)
def query_energy_consumption():
    try:
        import wmi
        c = wmi.WMI()
        for cpu in c.Win32_Processor():
            energy_consumed = cpu.CurrentVoltage * cpu.CurrentClockSpeed
            return energy_consumed  # Adjust calculation based on available properties
    except Exception as e:
        print(f"Error querying energy consumption: {e}")
        return None

# Function to collect all data
def collect_all_data():
    platform_info = platform.system()

    cpu_data, memory_data = collect_cpu_memory_data()
    network_data = collect_network_data()
    energy_consumed = query_energy_consumption()

    # Adding timestamp
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    telemetry_data = {
        "timestamp": timestamp,
        "platform": platform_info,
        "cpu": cpu_data,
        "memory": memory_data,
        "network": network_data,
        "energy_consumed": energy_consumed  # None if not available or not applicable
    }

    return telemetry_data

# Function to save telemetry data to JSON file
def save_telemetry_data(file_path, telemetry_data):
    try:
        # Check if file exists
        file_exists = os.path.isfile(file_path)

        with open(file_path, "a+") as file:
            if not file_exists:
                file.write("[\n")  # Start of JSON array if file is newly created
            else:
                file.seek(file.tell() - 1, os.SEEK_SET)
                file.truncate()  # Remove the last character (']') to append new data properly
                file.write(",\n")  # Write comma for JSON array continuation

            json.dump(telemetry_data, file, indent=4)
            file.write("\n]")  # End of JSON array

        print(f"Telemetry data appended to {file_path}")
    except Exception as e:
        print(f"Error saving telemetry data: {e}")

# Main execution
if __name__ == "__main__":
    try:
        telemetry_data = collect_all_data()

        # Print collected data for verification
        print("Telemetry Data:")
        print(json.dumps(telemetry_data, indent=4))

        # Specify the file path where telemetry data will be saved
        file_path = os.path.join(os.path.dirname(__file__), "telemetry_data.json")

        # Save telemetry data to JSON file
        save_telemetry_data(file_path, telemetry_data)

    except KeyboardInterrupt:
        print("\nTelemetry data collection interrupted.")
    except Exception as e:
        print(f"Error: {e}")
