import subprocess
import time
import os

log_file = "/path/to/your/logfile.txt"
temp_log_interval = 5  # seconds
load_duration = 300  # seconds per load step
load_steps = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]  # Load levels
cool_down = 120  # seconds


def log_temperature():
    """Logs the CPU temperature."""
    try:
        temp_output = (
            subprocess.check_output("sensors | grep 'Core 0'", shell=True)
            .decode()
            .strip()
        )

        with open(log_file, "a") as file:
            file.write(f"{time.ctime()}: {temp_output}\n")
    except subprocess.CalledProcessError as e:
        print(f"Error logging temperature: {e}")


def apply_load(load):
    """Applies CPU load using stress-ng."""
    print(f"Applying {load}% CPU load for {load_duration} seconds...")
    subprocess.run(
        f"stress-ng --cpu 1 --cpu-load {load} --timeout {load_duration}", shell=True
    )


def main():
    os.makedirs(os.path.dirname(log_file), exist_ok=True)
    next_log_time = time.time()

    try:
        for load in load_steps:
            while time.time() < next_log_time + load_duration:
                log_temperature()
                time.sleep(temp_log_interval)

            apply_load(load)

            print(f"Cooling down for {cool_down} seconds...")
            next_log_time = time.time() + cool_down

            while time.time() < next_log_time:
                log_temperature()
                time.sleep(temp_log_interval)
    except KeyboardInterrupt:
        print("Script interrupted.")


if __name__ == "__main__":
    main()
