# GreenMetrics

Welcome to GreenMetrics, a web-based application designed to monitor and optimize system energy consumption for a greener future. This project provides valuable insights into your system's performance metrics and helps in making eco-friendly decisions.

## Features

- Monitor Average CPU Percent, Average Disk IO (GB), and Average Memory Percent.
- Estimate Energy Usage based on collected metrics.
- User-friendly interface with real-time data visualization.
- Future plans for a personalized dashboard and advanced Docker integration.

## Installation

Follow these steps to set up and run GreenMetrics on your local machine.

### Prerequisites

- Python 3.6+
- Django 3.1+
- `pip` package manager

### Steps to Install

1. **Clone the Repository:**

   ```bash
   https://github.com/npriya2612/intel-unnati-project
   cd final_telemetry_project
   ```

2. **Create a Virtual Environment:**

   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. **Install Dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Run Migrations:**

   ```bash
   python manage.py migrate
   ```

5. **Create a Superuser (optional but recommended):**

   ```bash
   python manage.py createsuperuser
   ```

6. **Start the Development Server:**

   ```bash
   python manage.py runserver
   ```

   Open your web browser and go to `http://127.0.0.1:8000` to access GreenMetrics.

   Here are some screenshots of how the dashboard looks:

![image](https://github.com/user-attachments/assets/1d956357-4e6f-4f75-a301-174ecc07b59d)
![image](https://github.com/user-attachments/assets/64de5718-03ca-4deb-a5d3-04eb945e997e)
![image](https://github.com/user-attachments/assets/71f2e733-a356-4603-8277-60cd660efc67)


## Usage

1. **Power Utilization:**
   - Click on the "Power Utilization" button on the homepage to fetch the latest metrics.
   - Metrics such as Average CPU Percent, Average Disk IO (GB), and Average Memory Percent will be displayed.

2. **Data Storage:**
   - All fetched data is stored in a JSON file (`all_data.json`) for future reference and analysis.

## Optimization Tips

GreenMetrics provides optimization tips based on the following standards and guidelines:

1. **Energy Star Recommendations:**
   - Following the guidelines provided by the Energy Star program to optimize energy consumption for computing devices.

2. **Bureau of Energy Efficiency (BEE) Standards:**
   - Adopting best practices as outlined by the BEE in India, focusing on reducing energy consumption and improving system efficiency.

3. **ASHRAE Standards:**
   - Implementing cooling and heating standards recommended by ASHRAE to ensure efficient thermal management of computing devices.

4. **ISO 50001 Energy Management:**
   - Aligning with the ISO 50001 standards for energy management to continuously improve energy performance.

## Future Enhancements

- **Docker Integration:**
  - We are currently working on Docker integration to simulate different workloads and collect relevant metrics. This will enhance the robustness and scalability of GreenMetrics.
  
- **Personalized Dashboard:**
  - In future updates, we plan to develop a more personalized dashboard that will provide detailed insights and optimization tips based on individual user telemetry data.

