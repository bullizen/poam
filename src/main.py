import os
import threading
from gui import create_gui, start_gui, update_log_content, update_labels, update_ssh_texts
from monitor import update_health_indicators, update_ssh_info

def start_monitoring(root, cpu_label, memory_label, disk_label, network_label, ssh_ports_text, insecure_files_text, warning_log_text, info_log_text):
    """
    Start monitoring system health indicators and SSH information, and update the GUI accordingly.

    Args:
        root (tk.Tk): The root Tkinter window.
        cpu_label (tk.Label): Label widget to display CPU usage.
        memory_label (tk.Label): Label widget to display memory usage.
        disk_label (tk.Label): Label widget to display disk usage.
        network_label (tk.Label): Label widget to display network usage.
        ssh_ports_text (tk.Text): Text widget to display SSH port information.
        insecure_files_text (tk.Text): Text widget to display insecure file information.
        warning_log_text (tk.Text): Text widget to display warning log content.
        info_log_text (tk.Text): Text widget to display info log content.

    This function sets up the paths for the log files, schedules periodic updates for the log content,
    and starts background threads to monitor system health and SSH information.
    """
    # Define the log file paths within the src directory
    log_dir = os.path.dirname(__file__)
    warning_log_file = os.path.join(log_dir, 'network_monitor_warnings.log')
    info_log_file = os.path.join(log_dir, 'network_monitor.log')

    print(f"Reading from warning log file: {warning_log_file}")  # Debug print statement
    print(f"Reading from info log file: {info_log_file}")  # Debug print statement

    # Update logs more frequently (e.g., every 2 seconds)
    root.after(2000, update_log_content, warning_log_text, warning_log_file)
    root.after(2000, update_log_content, info_log_text, info_log_file)

    # Start the health monitoring and SSH info update in background threads
    threading.Thread(target=update_health_indicators, args=(root, cpu_label, memory_label, disk_label, network_label)).start()
    threading.Thread(target=update_ssh_info, args=(root, ssh_ports_text, insecure_files_text)).start()

if __name__ == "__main__":
    root, cpu_label, memory_label, disk_label, network_label, ssh_ports_text, insecure_files_text, warning_log_text, info_log_text = create_gui()
    root.after(3000, start_monitoring, root, cpu_label, memory_label, disk_label, network_label, ssh_ports_text, insecure_files_text, warning_log_text, info_log_text)  # Pass the widgets to start_monitoring
    start_gui(root)
