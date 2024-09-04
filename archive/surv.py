import tkinter as tk
from tkinter import scrolledtext
import psutil
import argparse
import subprocess
import os
import stat
import threading
import platform
import ctypes


def parse_arguments():
    # Determine the default directory based on the OS
    if platform.system() == "Windows":
        default_dir = "C:\\ProgramData"  # Example directory on Windows
    else:
        default_dir = "/etc"  # Example directory on Linux/Unix

    parser = argparse.ArgumentParser(
        description="System Health and SSH Monitoring Tool"
    )
    parser.add_argument(
        "--cpu", type=int, default=80, help="CPU usage warning threshold (%)"
    )
    parser.add_argument(
        "--memory", type=int, default=80, help="Memory usage warning threshold (%)"
    )
    parser.add_argument(
        "--disk", type=int, default=90, help="Disk usage warning threshold (%)"
    )
    parser.add_argument(
        "--network",
        type=float,
        default=100.0,
        help="Network usage warning threshold (MB/s)",
    )
    parser.add_argument(
        "--insecure_dirs",
        nargs="*",
        default=[default_dir],  # Use the OS-specific default directory
        help="Directories to scan for insecure files",
    )
    args = parser.parse_args()
    return args


args = parse_arguments()

# Initialize previous network counters
prev_net_sent = psutil.net_io_counters().bytes_sent
prev_net_recv = psutil.net_io_counters().bytes_recv


def get_open_ports():
    try:
        if platform.system() == "Windows":
            # Use netstat on Windows
            result = subprocess.check_output(["netstat", "-an"], text=True)
        else:
            # Use ss on Linux/Unix
            result = subprocess.check_output(["ss", "-tuln"], text=True)
        return result.strip()
    except Exception as e:
        return f"Error retrieving open ports: {e}"


def is_world_readable(filepath):
    """Check if a file is world-readable on Unix-like systems."""
    mode = os.stat(filepath).st_mode
    return mode & stat.S_IROTH


def check_windows_permissions(filepath):
    """Check if a file is readable by everyone on Windows using ctypes."""
    try:
        sd = ctypes.windll.advapi32.GetFileSecurityW(
            ctypes.c_wchar_p(filepath),
            7,  # DACL_SECURITY_INFORMATION
            None,
            0,
            ctypes.byref(ctypes.c_ulong(0)),
        )
        return sd == 0  # If GetFileSecurityW returns 0, the file might be insecure
    except Exception:
        return False


def check_insecure_files(directories):
    insecure_files = []
    is_windows = platform.system() == "Windows"

    for directory in directories:
        for root, dirs, files in os.walk(directory):
            for name in files:
                full_path = os.path.join(root, name)
                try:
                    if is_windows:
                        # Check using Windows-specific permissions
                        if check_windows_permissions(full_path):
                            insecure_files.append(full_path)
                    else:
                        # Check using Unix-style permissions
                        if is_world_readable(full_path):
                            insecure_files.append(full_path)
                except (OSError, PermissionError) as e:
                    print(f"Error checking permissions for {full_path}: {e}")
    return insecure_files


def update_health_indicators():
    # CPU Usage
    cpu_usage = psutil.cpu_percent(interval=1)
    cpu_label.config(text=f"CPU Usage: {cpu_usage:.2f}%")
    cpu_label.config(fg="red" if cpu_usage > args.cpu else "green")

    # Memory Usage
    memory_info = psutil.virtual_memory()
    memory_usage = memory_info.percent
    memory_label.config(text=f"Memory Usage: {memory_usage:.2f}%")
    memory_label.config(fg="red" if memory_usage > args.memory else "green")

    # Disk Usage
    disk_info = psutil.disk_usage("/")
    disk_usage = disk_info.percent
    disk_label.config(text=f"Disk Usage: {disk_usage:.2f}%")
    disk_label.config(fg="red" if disk_usage > args.disk else "green")

    # Network Usage
    global prev_net_sent, prev_net_recv
    net_info = psutil.net_io_counters()
    net_sent = net_info.bytes_sent
    net_recv = net_info.bytes_recv

    sent_per_sec = (net_sent - prev_net_sent) / (1024 * 1024)  # Convert to MB
    recv_per_sec = (net_recv - prev_net_recv) / (1024 * 1024)  # Convert to MB

    network_label.config(
        text=f"Network Usage: Sent: {sent_per_sec:.2f} MB/s, Recv: {recv_per_sec:.2f} MB/s"
    )
    if sent_per_sec > args.network or recv_per_sec > args.network:
        network_label.config(fg="red")
    else:
        network_label.config(fg="green")

    prev_net_sent = net_sent
    prev_net_recv = net_recv

    # Schedule next update
    root.after(1000, update_health_indicators)


def update_ssh_info():
    # Open Ports
    open_ports = get_open_ports()
    ssh_ports_text.delete(1.0, tk.END)
    ssh_ports_text.insert(tk.END, open_ports)

    # Insecure Files
    insecure_files = check_insecure_files(args.insecure_dirs)
    insecure_files_text.delete(1.0, tk.END)
    if insecure_files:
        for file in insecure_files:
            insecure_files_text.insert(tk.END, f"{file}\n")
    else:
        insecure_files_text.insert(tk.END, "No insecure files found.")

    # Schedule next update every 60 seconds
    root.after(60000, update_ssh_info)


# Initialize Tkinter window
root = tk.Tk()
root.title("System Health and SSH Monitoring")
root.geometry("800x600")

# Create frames for organization
system_frame = tk.LabelFrame(root, text="System Health Indicators", padx=10, pady=10)
system_frame.pack(fill="both", expand="yes", padx=10, pady=5)

ssh_frame = tk.LabelFrame(root, text="SSH Monitoring", padx=10, pady=10)
ssh_frame.pack(fill="both", expand="yes", padx=10, pady=5)

# System Health Labels
cpu_label = tk.Label(
    system_frame, text="CPU Usage: Calculating...", font=("Helvetica", 12)
)
cpu_label.pack(anchor="w")

memory_label = tk.Label(
    system_frame, text="Memory Usage: Calculating...", font=("Helvetica", 12)
)
memory_label.pack(anchor="w")

disk_label = tk.Label(
    system_frame, text="Disk Usage: Calculating...", font=("Helvetica", 12)
)
disk_label.pack(anchor="w")

network_label = tk.Label(
    system_frame, text="Network Usage: Calculating...", font=("Helvetica", 12)
)
network_label.pack(anchor="w")

# SSH Monitoring Labels and Text Areas
ssh_ports_label = tk.Label(ssh_frame, text="Open Ports:", font=("Helvetica", 12))
ssh_ports_label.pack(anchor="w")

ssh_ports_text = scrolledtext.ScrolledText(ssh_frame, height=10)
ssh_ports_text.pack(fill="both", expand=True, pady=5)

insecure_files_label = tk.Label(
    ssh_frame, text="Insecure Files:", font=("Helvetica", 12)
)
insecure_files_label.pack(anchor="w")

insecure_files_text = scrolledtext.ScrolledText(ssh_frame, height=10)
insecure_files_text.pack(fill="both", expand=True, pady=5)


# Start monitoring in separate threads to keep UI responsive
def start_monitoring():
    threading.Thread(target=update_health_indicators).start()
    threading.Thread(target=update_ssh_info).start()


start_monitoring()

# Start Tkinter main loop
root.mainloop()