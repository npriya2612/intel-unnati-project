import json

# Function to save telemetry data to JSON file
def save_telemetry_data(cpu, memory, disk):
    data = {
        'cpu': cpu,
        'memory': memory,
        'disk': disk
    }

    try:
        with open('previous_telemetry.json', 'a+') as file:
            file.seek(0)
            contents = file.read()
            if contents:
                file.write(',')
            json.dump(data, file)
            file.write('\n')
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
