import tkinter as tk
from tkinter import scrolledtext
from tkinter import ttk
import psutil
import argparse
import subprocess
import os
import stat
import threading
import platform
import ctypes
import time
import logging
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime, timedelta


class SystemMonitorApp:
    def __init__(self, root, args):
        self.root = root
        self.args = args

        # Initialize previous network counters
        self.prev_net_sent = psutil.net_io_counters().bytes_sent
        self.prev_net_recv = psutil.net_io_counters().bytes_recv

        # Initialize email and logging settings
        self.init_email_settings()
        self.init_logging()

        # Initialize Tkinter UI
        self.init_ui()

        # Start monitoring in separate threads
        self.start_monitoring()

    def init_email_settings(self):
        self.email_from = "your_email@example.com"
        self.email_to = "admin@example.com"
        self.email_subject = "Network Monitor Warning"
        self.smtp_server = "smtp.example.com"
        self.smtp_port = 587
        self.smtp_username = "your_email@example.com"
        self.smtp_password = "your_password"
        self.email_cooldown = timedelta(minutes=5)
        self.last_email_time = datetime.min

    def init_logging(self):
        self.warning_logger = self.setup_logger(
            'warning_logger', 'network_monitor_warnings.log', logging.WARNING
        )
        self.network_logger = self.setup_logger(
            'network_logger', 'network_monitor.log', logging.INFO
        )

    @staticmethod
    def setup_logger(name, log_file, level):
        handler = logging.FileHandler(log_file)
        handler.setLevel(level)
        handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
        logger = logging.getLogger(name)
        logger.setLevel(level)
        logger.addHandler(handler)
        return logger

    def send_email(self, subject, body):
        current_time = datetime.now()
        if current_time - self.last_email_time < self.email_cooldown:
            print("Email not sent due to cooldown period.")
            return

        msg = MIMEMultipart()
        msg['From'] = self.email_from
        msg['To'] = self.email_to
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))

        try:
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.smtp_username, self.smtp_password)
                server.sendmail(self.email_from, self.email_to, msg.as_string())
                self.last_email_time = current_time
                print("Warning email sent successfully.")
        except Exception as e:
            print(f"Failed to send email: {e}")

    def get_open_ports(self):
        command = ["netstat", "-an"] if platform.system() == "Windows" else ["ss", "-tuln"]
        try:
            result = subprocess.check_output(command, text=True)
            return result.strip()
        except Exception as e:
            return f"Error retrieving open ports: {e}"

    @staticmethod
    def is_world_readable(filepath):
        mode = os.stat(filepath).st_mode
        return mode & stat.S_IROTH

    @staticmethod
    def check_windows_permissions(filepath):
        try:
            sd = ctypes.windll.advapi32.GetFileSecurityW(
                ctypes.c_wchar_p(filepath),
                7,
                None,
                0,
                ctypes.byref(ctypes.c_ulong(0)),
            )
            return sd == 0
        except Exception:
            return False

    def check_insecure_files(self, directories):
        insecure_files = []
        is_windows = platform.system() == "Windows"

        for directory in directories:
            for root, _, files in os.walk(directory):
                for name in files:
                    full_path = os.path.join(root, name)
                    try:
                        if is_windows and self.check_windows_permissions(full_path):
                            insecure_files.append(full_path)
                        elif not is_windows and self.is_world_readable(full_path):
                            insecure_files.append(full_path)
                    except (OSError, PermissionError) as e:
                        print(f"Error checking permissions for {full_path}: {e}")
        return insecure_files

    def update_health_indicators(self):
        start_time = time.time()

        self.update_cpu_usage()
        self.update_memory_usage()
        self.update_disk_usage()
        self.update_network_usage()

        execution_time = time.time() - start_time
        if execution_time > 2:  # 2 seconds
            warning_message = f"Script execution is too slow! Execution time: {execution_time:.2f} seconds"
            self.warning_logger.warning(warning_message)
            self.send_email(self.email_subject, warning_message)

        self.root.after(1000, self.update_health_indicators)

    def update_cpu_usage(self):
        cpu_usage = psutil.cpu_percent(interval=1)
        self.cpu_label.config(text=f"CPU Usage: {cpu_usage:.2f}%")
        self.cpu_label.config(fg="red" if cpu_usage > self.args.cpu else "green")

    def update_memory_usage(self):
        memory_usage = psutil.virtual_memory().percent
        self.memory_label.config(text=f"Memory Usage: {memory_usage:.2f}%")
        self.memory_label.config(fg="red" if memory_usage > self.args.memory else "green")

    def update_disk_usage(self):
        disk_usage = psutil.disk_usage("/").percent
        self.disk_label.config(text=f"Disk Usage: {disk_usage:.2f}%")
        self.disk_label.config(fg="red" if disk_usage > self.args.disk else "green")

    def update_network_usage(self):
        net_info = psutil.net_io_counters()
        sent_per_sec = (net_info.bytes_sent - self.prev_net_sent) / (1024 * 1024)
        recv_per_sec = (net_info.bytes_recv - self.prev_net_recv) / (1024 * 1024)

        self.network_label.config(
            text=f"Network Usage: Sent: {sent_per_sec:.2f} MB/s, Recv: {recv_per_sec:.2f} MB/s"
        )
        if sent_per_sec > self.args.network or recv_per_sec > self.args.network:
            warning_message = f"High network usage detected! Sent: {sent_per_sec:.2f} MB/s, Recv: {recv_per_sec:.2f} MB/s"
            self.warning_logger.warning(warning_message)
            self.send_email(self.email_subject, warning_message)
            self.network_label.config(fg="red")
        else:
            self.network_label.config(fg="green")

        self.network_logger.info(f"Sent: {sent_per_sec:.2f} MB/s, Recv: {recv_per_sec:.2f} MB/s")

        self.prev_net_sent = net_info.bytes_sent
        self.prev_net_recv = net_info.bytes_recv

    def update_ssh_info(self):
        open_ports = self.get_open_ports()
        self.ssh_ports_text.delete(1.0, tk.END)
        self.ssh_ports_text.insert(tk.END, open_ports)

        insecure_files = self.check_insecure_files(self.args.insecure_dirs)
        self.insecure_files_text.delete(1.0, tk.END)
        if insecure_files:
            for file in insecure_files:
                self.insecure_files_text.insert(tk.END, f"{file}\n")
        else:
            self.insecure_files_text.insert(tk.END, "No insecure files found.")

        self.root.after(60000, self.update_ssh_info)

    @staticmethod
    def update_log_content(log_text_widget, log_file):
        try:
            with open(log_file, 'r') as file:
                log_text_widget.delete(1.0, tk.END)
                log_text_widget.insert(tk.END, file.read())
        except FileNotFoundError:
            log_text_widget.delete(1.0, tk.END)
            log_text_widget.insert(tk.END, f"Log file {log_file} not found.")

    def init_ui(self):
        self.root.title("System Health and SSH Monitoring")
        self.root.geometry("800x600")

        notebook = ttk.Notebook(self.root)
        notebook.pack(expand=True, fill='both')

        self.init_monitoring_tab(notebook)
        self.init_logs_tab(notebook)

    def init_monitoring_tab(self, notebook):
        main_frame = tk.Frame(notebook)
        notebook.add(main_frame, text="Monitoring")

        system_frame = tk.LabelFrame(main_frame, text="System Health Indicators", padx=10, pady=10)
        system_frame.pack(fill="both", expand="yes", padx=10, pady=5)

        ssh_frame = tk.LabelFrame(main_frame, text="SSH Monitoring", padx=10, pady=10)
        ssh_frame.pack(fill="both", expand="yes", padx=10, pady=5)

        self.cpu_label = tk.Label(system_frame, text="CPU Usage: Calculating...", font=("Helvetica", 12))
        self.cpu_label.pack(anchor="w")

        self.memory_label = tk.Label(system_frame, text="Memory Usage: Calculating...", font=("Helvetica", 12))
        self.memory_label.pack(anchor="w")

        self.disk_label = tk.Label(system_frame, text="Disk Usage: Calculating...", font=("Helvetica", 12))
        self.disk_label.pack(anchor="w")

        self.network_label = tk.Label(system_frame, text="Network Usage: Calculating...", font=("Helvetica", 12))
        self.network_label.pack(anchor="w")

        ssh_ports_label = tk.Label(ssh_frame, text="Open Ports:", font=("Helvetica", 12))
        ssh_ports_label.pack(anchor="w")

        self.ssh_ports_text = scrolledtext.ScrolledText(ssh_frame, height=10)
        self.ssh_ports_text.pack(fill="both", expand=True, pady=5)

        insecure_files_label = tk.Label(ssh_frame, text="Insecure Files:", font=("Helvetica", 12))
        insecure_files_label.pack(anchor="w")

        self.insecure_files_text = scrolledtext.ScrolledText(ssh_frame, height=10)
        self.insecure_files_text.pack(fill="both", expand=True, pady=5)

    def init_logs_tab(self, notebook):
        log_frame = tk.Frame(notebook)
        notebook.add(log_frame, text="Logs")

        warning_log_frame = tk.LabelFrame(log_frame, text="Warnings Log", padx=10, pady=10)
        warning_log_frame.pack(fill="both", expand="yes", padx=10, pady=5)

        info_log_frame = tk.LabelFrame(log_frame, text="Network Log", padx=10, pady=10)
        info_log_frame.pack(fill="both", expand="yes", padx=10, pady=5)

        self.warning_log_text = scrolledtext.ScrolledText(warning_log_frame, height=10)
        self.warning_log_text.pack(fill="both", expand=True, pady=5)

        self.info_log_text = scrolledtext.ScrolledText(info_log_frame, height=10)
        self.info_log_text.pack(fill="both", expand=True, pady=5)

    def start_monitoring(self):
        threading.Thread(target=self.update_health_indicators).start()
        threading.Thread(target=self.update_ssh_info).start()
        threading.Thread(target=self.update_log_content, args=(self.warning_log_text, 'network_monitor_warnings.log')).start()
        threading.Thread(target=self.update_log_content, args=(self.info_log_text, 'network_monitor.log')).start()


def parse_arguments():
    default_dir = "C:\\ProgramData" if platform.system() == "Windows" else "/etc"
    parser = argparse.ArgumentParser(description="System Health and SSH Monitoring Tool")
    parser.add_argument("--cpu", type=int, default=80, help="CPU usage warning threshold (%)")
    parser.add_argument("--memory", type=int, default=80, help="Memory usage warning threshold (%)")
    parser.add_argument("--disk", type=int, default=90, help="Disk usage warning threshold (%)")
    parser.add_argument("--network", type=float, default=100.0, help="Network usage warning threshold (MB/s)")
    parser.add_argument("--insecure_dirs", nargs="*", default=[default_dir], help="Directories to scan for insecure files")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_arguments()
    root = tk.Tk()
    app = SystemMonitorApp(root, args)
    root.mainloop()
