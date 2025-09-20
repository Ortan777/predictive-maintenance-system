# AI-Powered Predictive System Monitoring

An end-to-end monitoring platform that collects system metrics (CPU, RAM, etc.) from multiple devices, analyzes the data using machine learning to predict potential failures, and provides a real-time web dashboard for visualization and control.

[Dashboard Screenshot]<img width="1823" height="897" alt="Screenshot 2025-09-20 121825 - Copy" src="https://github.com/user-attachments/assets/b0512a39-c85a-4654-bc26-b217077c7e20" />

---

##  Key Features

* **Multi-Device Monitoring:** Agents can be deployed on any number of client machines (laptops, servers, etc.) to send metrics to a central host.
* **Predictive Failure Analysis:** A machine learning model analyzes incoming metrics to calculate a real-time failure probability score for each device.
* **Real-Time Dashboard:** A clean, interactive web interface built with pure JavaScript and Chart.js to visualize device status, metrics, and historical data.
* **Interactive Controls:** Click on device status groups to instantly view a list of corresponding devices.
* **Remote File Sharing:** Send files from the host dashboard to a specific client device or broadcast to all connected devices at once.

---

##  Tech Stack

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)
![JavaScript](https://img.shields.io/badge/javascript-%23323330.svg?style=for-the-badge&logo=javascript&logoColor=%23F7DF1E)
![HTML5](https://img.shields.io/badge/html5-%23E34F26.svg?style=for-the-badge&logo=html5&logoColor=white)
![CSS3](https://img.shields.io/badge/css3-%231572B6.svg?style=for-the-badge&logo=css3&logoColor=white)
![Scikit-learn](https://img.shields.io/badge/scikit--learn-%23F7931E.svg?style=for-the-badge&logo=scikit-learn&logoColor=white)
![Chart\.js](https://img.shields.io/badge/chart.js-F5788D.svg?style=for-the-badge&logo=chart.js&logoColor=white)

---

##  Getting Started

Follow these instructions to set up and run the project on your local network.

### Prerequisites

* Python 3.8+
* Git

### 1. Set Up the Host Server

This is the main "command center" that runs the backend and serves the frontend.

```bash
# 1. Clone the repository
git clone [https://github.com/Ortan777/predictive-maintenance-system.git]
cd Your-Repo-Name

# 2. Create and activate a virtual environment
python -m venv .venv
# On Windows
.\.venv\Scripts\Activate
# On macOS/Linux
source .venv/bin/activate

# 3. Install all required Python packages
pip install -r backend/requirements.txt

# 4. Train the machine learning model
# This creates the .pkl file needed by the server.
python backend/train_failure_model.py

# 5. Find your Host IP Address
# On Windows
ipconfig
# On macOS/Linux
ip addr
# Note your IPv4 address (e.g., 192.168.1.15)

# 6. Configure the frontend
# Open 'frontend-pure-js/script.js' and set the API_BASE_URL to your Host's IP address.
# const API_BASE_URL = '[http://192.168.1.15:8000](http://192.168.1.15:8000)';

# 7. Run the backend server
cd backend
python main.py
