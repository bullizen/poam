import subprocess
import os
import stat
import platform
import ctypes
import time
import logging
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime, timedelta
from config import args
from gui import update_labels, update_ssh_texts
import psutil


# Initialize previous network counters
prev_net_sent = psutil.net_io_counters().bytes_sent
prev_net_recv = psutil.net_io_counters().bytes_recv

# Initialize logging and email settings
last_email_time = datetime.min
email_cooldown = timedelta(minutes=5)

# Setup logging
warning_logger = logging.getLogger('warning_logger')
network_logger = logging.getLogger('network_logger')

def setup_logger(name, log_file, level=logging.INFO):
    """
    Sets up a logger with the specified name, log file, and logging level.

    Args:
        name (str): The name of the logger.
        log_file (str): The file path where the log messages will be written.
        level (int, optional): The logging level (e.g., logging.INFO, logging.DEBUG). Defaults to logging.INFO.

    Returns:
        logging.Logger: The configured logger instance.
    """
    handler = logging.FileHandler(log_file)
    handler.setLevel(level)
    handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)
    print(f"Logger {name} is set up to write to {log_file}.")  # Debug print statement
    return logger

# Initialize loggers with paths within the src directory
log_dir = os.path.dirname(__file__)
warning_log_path = os.path.join(log_dir, 'network_monitor_warnings.log')
info_log_path = os.path.join(log_dir, 'network_monitor.log')

setup_logger('warning_logger', warning_log_path, logging.WARNING)
setup_logger('network_logger', info_log_path, logging.INFO)

def send_email(subject, body):
    """
    Sends an email with the specified subject and body, respecting a cooldown period between emails.

    Args:
        subject (str): The subject of the email.
        body (str): The body content of the email.

    Returns:
        None
    """
    global last_email_time
    current_time = datetime.now()
    if current_time - last_email_time < email_cooldown:
        print("Email not sent due to cooldown period.")
        return

    msg = MIMEMultipart()
    msg['From'] = args.email_from
    msg['To'] = args.email_to
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    try:
        with smtplib.SMTP(args.smtp_server, args.smtp_port) as server:
            server.starttls()
            server.login(args.smtp_username, args.smtp_password)
            server.sendmail(args.email_from, args.email_to, msg.as_string())
            last_email_time = current_time
            print("Warning email sent successfully.")
    except Exception as e:
        print(f"Failed to send email: {e}")

def get_open_ports():
    """
    Retrieves a list of open ports on the system.

    On Windows, it uses the `netstat` command to get the list of open ports.
    On Unix-like systems, it uses the `ss` command.

    Returns:
        str: A string containing the list of open ports or an error message if the command fails.
    """
    try:
        if platform.system() == "Windows":
            result = subprocess.check_output(["netstat", "-an"], text=True)
        else:
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
        return sd == 0
    except Exception:
        return False

def check_insecure_files(directories):
    """
    Checks for insecure files in the given directories.

    On Windows, it checks if the files have insecure permissions using `check_windows_permissions`.
    On Unix-like systems, it checks if the files are world-readable using `is_world_readable`.

    Args:
        directories (list): A list of directory paths to check for insecure files.

    Returns:
        list: A list of file paths that are considered insecure.
    """
    insecure_files = []
    is_windows = platform.system() == "Windows"

    for directory in directories:
        for root, dirs, files in os.walk(directory):
            for name in files:
                full_path = os.path.join(root, name)
                try:
                    if is_windows:
                        if check_windows_permissions(full_path):
                            insecure_files.append(full_path)
                    else:
                        if is_world_readable(full_path):
                            insecure_files.append(full_path)
                except (OSError, PermissionError) as e:
                    print(f"Error checking permissions for {full_path}: {e}")
    return insecure_files

def update_health_indicators(root, cpu_label, memory_label, disk_label, network_label):
    """
    Updates the health indicators for CPU, memory, disk, and network usage.

    Args:
        root (tk.Tk): The root Tkinter window.
        cpu_label (tk.Label): The label widget to display CPU usage.
        memory_label (tk.Label): The label widget to display memory usage.
        disk_label (tk.Label): The label widget to display disk usage.
        network_label (tk.Label): The label widget to display network usage.

    Returns:
        None
    """
    global prev_net_sent, prev_net_recv

    start_time = time.time()

    # CPU Usage
    cpu_usage = psutil.cpu_percent(interval=1)
    memory_info = psutil.virtual_memory()
    disk_info = psutil.disk_usage("/")
    net_info = psutil.net_io_counters()

    net_sent = net_info.bytes_sent
    net_recv = net_info.bytes_recv
    sent_per_sec = (net_sent - prev_net_sent) / (1024 * 1024)
    recv_per_sec = (net_recv - prev_net_recv) / (1024 * 1024)

    prev_net_sent = net_sent
    prev_net_recv = net_recv

    # Schedule UI updates on the main thread
    root.after(0, update_labels, cpu_label, memory_label, disk_label, network_label, cpu_usage, memory_info.percent, disk_info.percent, sent_per_sec, recv_per_sec)

    # Log network usage
    network_logger.info(f"Sent: {sent_per_sec:.2f} MB/s, Recv: {recv_per_sec:.2f} MB/s")

    if sent_per_sec > args.network or recv_per_sec > args.network:
        warning_message = f"High network usage detected! Sent: {sent_per_sec:.2f} MB/s, Recv: {recv_per_sec:.2f} MB/s"
        warning_logger.warning(warning_message)
        send_email("Network Monitor Warning", warning_message)

    # Check if execution time is too slow
    execution_time = time.time() - start_time
    if execution_time > 2:  # 2 seconds
        warning_message = f"Script execution is too slow! Execution time: {execution_time:.2f} seconds"
        warning_logger.warning(warning_message)
        send_email("Performance Warning", warning_message)

    # Schedule next update
    root.after(1000, update_health_indicators, root, cpu_label, memory_label, disk_label, network_label)

def update_ssh_info(root, ssh_ports_text, insecure_files_text):
    """
    Updates the SSH information displayed in the UI.

    This function retrieves the list of open SSH ports and insecure files, then updates the corresponding
    text widgets in the UI. It schedules itself to run every 60 seconds.

    Args:
        root (tk.Tk): The root Tkinter window.
        ssh_ports_text (tk.Text): The text widget to display open SSH ports.
        insecure_files_text (tk.Text): The text widget to display insecure files.

    Returns:
        None
    """
    open_ports = get_open_ports()
    insecure_files = check_insecure_files(args.insecure_dirs)

    # Schedule UI updates on the main thread
    root.after(0, update_ssh_texts, ssh_ports_text, insecure_files_text, open_ports, insecure_files)

    # Schedule next update every 60 seconds
    root.after(60000, update_ssh_info, root, ssh_ports_text, insecure_files_text)