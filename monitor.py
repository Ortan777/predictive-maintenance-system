# monitor.py (agent)

import os
import socket
import statistics
import time
from collections import deque
from uuid import getnode as get_mac

import psutil
import requests

# --- Configuration ---
# Set this to the IP address or domain of your backend server
HOST_IP = "10.206.212.90"
BASE_URL = f"http://{HOST_IP}:8000"
METRICS_API_URL = f"{BASE_URL}/send_metrics"
INTERVAL = 5  # Seconds between each cycle

# Rolling history buffers (last 5 points)
cpu_history = deque(maxlen=5)
mem_history = deque(maxlen=5)


# ### ADDED: Configuration for file downloads ###
DOWNLOADS_FOLDER = "received_files"
# ### END ADDED ###


def collect_metrics(device_id=None):
    """Collects system metrics and computes rolling statistics."""
    # Instant readings
    cpu_usage = psutil.cpu_percent(interval=1)
    memory_usage = psutil.virtual_memory().percent
    disk_usage = psutil.disk_usage('/').percent
    net_counters = psutil.net_io_counters()
    net_io = float(net_counters.bytes_sent + net_counters.bytes_recv) # Convert to float
    net_rate = net_io / (1024*1024) # MB

    # Update rolling buffers
    cpu_history.append(cpu_usage)
    mem_history.append(memory_usage)

    # Compute rolling statistics (if enough samples, else use current)
    cpu_mean_5 = statistics.mean(cpu_history) if len(cpu_history) > 0 else 0.0
    cpu_std_5 = statistics.pstdev(cpu_history) if len(cpu_history) > 1 else 0.0
    mem_mean_5 = statistics.mean(mem_history) if len(mem_history) > 0 else 0.0

    return {
        "device_id": device_id,
        "cpu_usage": round(cpu_usage, 2),
        "memory_usage": round(memory_usage, 2),
        "disk_usage": round(disk_usage, 2),
        "net_io": net_io,
        "cpu_mean_5": round(cpu_mean_5, 2),
        "cpu_std_5": round(cpu_std_5, 4),
        "mem_mean_5": round(mem_mean_5, 2),
        "net_rate": round(net_rate, 3)
    }

def get_device_id():
    """Generates a unique device ID from hostname and MAC address."""
    try:
        name = socket.gethostname()
        mac = get_mac()
        # Use last 4 hex digits of MAC for uniqueness
        return f"{name}-{mac & 0xffff:04x}"
    except:
        return socket.gethostname()

def send_metrics(metrics):
    """Sends metrics to the backend API."""
    try:
        r = requests.post(METRICS_API_URL, json=metrics, timeout=5)
        if r.status_code == 200:
            print(f"Metrics sent for '{metrics['device_id']}'. Risk: {r.json().get('failure_risk'):.2%}")
        else:
            print(f"Server error sending metrics: {r.status_code} - {r.text}")
    except Exception as e:
        print(f"Failed to send metrics: {e}")


# ### ADDED: Function to check for and download files ###
def check_and_download_files(device_id):
    """Checks for pending files on the server and downloads them."""
    try:
        # 1. Ask the server if there are any files for this device
        check_url = f"{BASE_URL}/files/check/{device_id}"
        response = requests.get(check_url, timeout=5)
        response.raise_for_status() # Raise an exception for bad status codes

        data = response.json()
        files_to_download = data.get("files_to_download", [])

        if not files_to_download:
            return # No files to download, just exit the function

        print(f"⬇️ Found {len(files_to_download)} file(s) to download: {', '.join(files_to_download)}")

        # 2. Download each file
        for filename in files_to_download:
            print(f"Downloading '{filename}'...")
            download_url = f"{BASE_URL}/files/download/{device_id}/{filename}"

            with requests.get(download_url, stream=True) as r:
                r.raise_for_status()
                local_filepath = os.path.join(DOWNLOADS_FOLDER, filename)
                with open(local_filepath, 'wb') as f:
                    for chunk in r.iter_content(chunk_size=8192):
                        f.write(chunk)
            print(f"✅ Successfully saved to '{local_filepath}'")

    except requests.exceptions.RequestException as e:
        print(f"Could not check for files: {e}")
    except Exception as e:
        print(f"An unexpected error occurred during file download: {e}")
# ### END ADDED ###


if __name__ == "__main__":
    device_id = get_device_id()
    print(f"🚀 Agent started. Device ID: '{device_id}'")
    
    # ### ADDED: Ensure downloads folder exists ###
    os.makedirs(DOWNLOADS_FOLDER, exist_ok=True)
    
    while True:
        # --- Task 1: Collect and Send Metrics ---
        metrics_data = collect_metrics(device_id=device_id)
        send_metrics(metrics_data)

        # --- Task 2: Check for and Download Files ---
        check_and_download_files(device_id=device_id)

        # --- Wait for the next cycle ---
        time.sleep(INTERVAL)