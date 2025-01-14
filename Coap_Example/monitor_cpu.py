import psutil
import time


# PID of the process to monitor
pid = 9164
process = psutil.Process(pid)

while True:
    cpu_usage = process.cpu_percent(interval=1)  # Get CPU usage as a percentage
    print(f"CPU Usage for process {pid}: {cpu_usage}%")
    time.sleep(0.05)  # Wait for 1 second before checking again