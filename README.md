# System Health and Monitoring Tool

## Overview
This repository contains a Python application designed to monitor system health indicators. The tool provides a graphical user interface to display real time data, logs and can send email notifications when certain thresholds are exceeded.

## Features
- **System Health Monitoring:** Tracks CPU, memory, disk, network usage in real time and displays this information on the GUI.
- **Logging:** Logs warnings and information about network usage and system health.
- **Email Notifications:** Sends email alerts if the usage thresholds are breached or if other critical issues are detected.

## File Structure
- `main.py`: The main entry point for the application. It initializes the GUI and starts the monitoring process.
- `config.py`: Handles command-line arguments for configuring thresholds and email settings.
- `gui.py`: Defines the graphical user interface, including all the labels, text areas, and tabs used to display monitoring data.
- `monitor.py`: Contains the logic for monitoring system health and SSH information, logging activity, and sending email alerts.

## Usage

### Prerequisites
- Python 3.x
- Required Python packages: `tkinter`, `psutil`, `smtplib`

### Installation and Execution
- Clone the repository:
   ```bash
   git clone git@github.com:nackc8/itinf23-scrumprojekt-lemon-hawk.git
    ```
- Install the required packages:
   ```bash
   pip install -r requirements.txt
   alternatively:
   pip install psutil smtplib tkinter
   ```
- Run the application:
   ```bash
   cd src
   python main.py
   ```

### Configuration
- To configure the monitoring thresholds and email settings, use the command-line arguments in `config.py`.
#### Available options:
    ```	
    --cpu: CPU usage warning threshold (%). Default is 80.
    --memory: Memory usage warning threshold (%). Default is 80.
    --disk: Disk usage warning threshold (%). Default is 90.
    --network: Network usage warning threshold (MB/s). Default is 100.0.
    --insecure_dirs: Directories to scan for insecure files. Default is "C:\\ProgramData" on Windows and "/etc" on Unix-like systems.
    Email settings: --email_from, --email_to, --smtp_server, --smtp_port, --smtp_username, --smtp_password.
    ```

## GUI Overview

- Monitoring Tab: Displays real-time system health indicators such as CPU, memory, disk, and network usage.

- Logs: Provides access to warning logs and network logs for detailed monitoring information.

## Logging and Email Notifications

- Logs are stored in the application directory under network_monitor.log and network_monitor_warnings.log.

- Email notifications are sent when the usage thresholds are breached or when critical issues are detected.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.