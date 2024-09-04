import tkinter as tk
from tkinter import scrolledtext, ttk
from config import args

# Declare labels and text areas as global variables
cpu_label = None
memory_label = None
disk_label = None
network_label = None
ssh_ports_text = None
insecure_files_text = None
warning_log_text = None
info_log_text = None


def create_gui():
    """
    Create and configure the graphical user interface for the System Health and SSH Monitoring Tool.

    This function initializes the main window and sets up a tabbed interface with two main tabs:
    "Monitoring" and "SSH Monitoring". Within the "Monitoring" tab, it creates labeled frames
    for displaying system health indicators and SSH monitoring information.

    The GUI components include:
    - A main window with a title and specified dimensions.
    - A notebook widget for tabbed navigation.
    - A "Monitoring" tab containing:
        - A labeled frame for system health indicators.
        - A labeled frame for SSH monitoring.
        - Labels for displaying CPU usage and other system health metrics.

    Returns:
        None
    """
    # Define local variables for the widgets
    root = tk.Tk()
    root.title("System Health and SSH Monitoring")
    root.geometry("800x600")

    # Create a notebook (tabbed interface)
    notebook = ttk.Notebook(root)
    notebook.pack(expand=True, fill='both')

    # Monitoring tab
    monitoring_tab = tk.Frame(notebook)
    notebook.add(monitoring_tab, text="Monitoring")

    system_frame = tk.LabelFrame(monitoring_tab, text="System Health Indicators", padx=10, pady=10)
    system_frame.pack(fill="both", expand="yes", padx=10, pady=5)

    ssh_frame = tk.LabelFrame(monitoring_tab, text="SSH Monitoring", padx=10, pady=10)
    ssh_frame.pack(fill="both", expand="yes", padx=10, pady=5)

    cpu_label = tk.Label(system_frame, text="CPU Usage: Calculating...", font=("Helvetica", 12))
    cpu_label.pack(anchor="w")

    memory_label = tk.Label(system_frame, text="Memory Usage: Calculating...", font=("Helvetica", 12))
    memory_label.pack(anchor="w")

    disk_label = tk.Label(system_frame, text="Disk Usage: Calculating...", font=("Helvetica", 12))
    disk_label.pack(anchor="w")

    network_label = tk.Label(system_frame, text="Network Usage: Calculating...", font=("Helvetica", 12))
    network_label.pack(anchor="w")

    ssh_ports_label = tk.Label(ssh_frame, text="Open Ports:", font=("Helvetica", 12))
    ssh_ports_label.pack(anchor="w")

    ssh_ports_text = scrolledtext.ScrolledText(ssh_frame, height=10)
    ssh_ports_text.pack(fill="both", expand=True, pady=5)

    insecure_files_label = tk.Label(ssh_frame, text="Insecure Files:", font=("Helvetica", 12))
    insecure_files_label.pack(anchor="w")

    insecure_files_text = scrolledtext.ScrolledText(ssh_frame, height=10)
    insecure_files_text.pack(fill="both", expand=True, pady=5)

    # Logs tab
    logs_tab = tk.Frame(notebook)
    notebook.add(logs_tab, text="Logs")

    warning_log_frame = tk.LabelFrame(logs_tab, text="Warnings Log", padx=10, pady=10)
    warning_log_frame.pack(fill="both", expand="yes", padx=10, pady=5)

    info_log_frame = tk.LabelFrame(logs_tab, text="Network Log", padx=10, pady=10)
    info_log_frame.pack(fill="both", expand="yes", padx=10, pady=5)

    # Initialize the log text widgets
    warning_log_text = scrolledtext.ScrolledText(warning_log_frame, height=10)
    warning_log_text.pack(fill="both", expand=True, pady=5)

    info_log_text = scrolledtext.ScrolledText(info_log_frame, height=10)
    info_log_text.pack(fill="both", expand=True, pady=5)

    # Return all necessary widgets
    return root, cpu_label, memory_label, disk_label, network_label, ssh_ports_text, insecure_files_text, warning_log_text, info_log_text

def start_gui(root):
    """
    Start the main loop of the graphical user interface.

    This function initiates the Tkinter main loop, which keeps the GUI running and responsive
    to user interactions. It should be called after all the GUI components have been created
    and configured.

    Args:
        root (tk.Tk): The root window of the Tkinter application.

    Returns:
        None
    """
    root.mainloop()

def update_labels(cpu_label, memory_label, disk_label, network_label, cpu_usage, memory_usage, disk_usage, sent_per_sec, recv_per_sec):
    """
    Update the text and color of the system health indicator labels.

    This function updates the text of the provided labels to display the current CPU, memory,
    disk, and network usage. It also changes the text color to red if the usage exceeds the
    specified thresholds, otherwise it sets the color to green.

    Args:
        cpu_label (tk.Label): Label widget for displaying CPU usage.
        memory_label (tk.Label): Label widget for displaying memory usage.
        disk_label (tk.Label): Label widget for displaying disk usage.
        network_label (tk.Label): Label widget for displaying network usage.
        cpu_usage (float): Current CPU usage percentage.
        memory_usage (float): Current memory usage percentage.
        disk_usage (float): Current disk usage percentage.
        sent_per_sec (float): Current network sent rate in MB/s.
        recv_per_sec (float): Current network received rate in MB/s.

    Returns:
        None
    """
    cpu_label.config(text=f"CPU Usage: {cpu_usage:.2f}%")
    cpu_label.config(fg="red" if cpu_usage > args.cpu else "green")

    memory_label.config(text=f"Memory Usage: {memory_usage:.2f}%")
    memory_label.config(fg="red" if memory_usage > args.memory else "green")

    disk_label.config(text=f"Disk Usage: {disk_usage:.2f}%")
    disk_label.config(fg="red" if disk_usage > args.disk else "green")

    network_label.config(text=f"Network Usage: Sent: {sent_per_sec:.2f} MB/s, Recv: {recv_per_sec:.2f} MB/s")
    if sent_per_sec > args.network or recv_per_sec > args.network:
        network_label.config(fg="red")
    else:
        network_label.config(fg="green")

def update_ssh_texts(ssh_ports_text, insecure_files_text, open_ports, insecure_files):
    """
    Update the text widgets for SSH ports and insecure files.

    This function updates the provided text widgets to display the current open SSH ports
    and insecure files. It clears the existing content and inserts the new information.

    Args:
        ssh_ports_text (tk.Text): Text widget for displaying open SSH ports.
        insecure_files_text (tk.Text): Text widget for displaying insecure files.
        open_ports (str): String containing the list of open SSH ports.
        insecure_files (list of str): List of insecure file paths.

    Returns:
        None
    """
    ssh_ports_text.delete(1.0, tk.END)
    ssh_ports_text.insert(tk.END, open_ports)

    insecure_files_text.delete(1.0, tk.END)
    if insecure_files:
        for file in insecure_files:
            insecure_files_text.insert(tk.END, f"{file}\n")
    else:
        insecure_files_text.insert(tk.END, "No insecure files found.")

def update_log_content(log_text_widget, log_file):
    """
    Update the content of a log text widget with the contents of a log file.

    This function reads the specified log file and updates the provided text widget
    with its contents. If the log file is not found, it displays an error message
    in the text widget. The function also scrolls to the end of the log content
    after updating.

    Args:
        log_text_widget (tk.Text): Text widget for displaying log content.
        log_file (str): Path to the log file to be read.

    Returns:
        None
    """
    if log_text_widget is None:
        print(f"Log text widget for {log_file} is None.")
        return

    print(f"Reading log file: {log_file}")

    try:
        with open(log_file, 'r') as file:
            log_text_widget.delete(1.0, tk.END)
            log_text_widget.insert(tk.END, file.read())
            log_text_widget.yview(tk.END)  # Scroll to the end of the log content
    except FileNotFoundError:
        log_text_widget.delete(1.0, tk.END)
        log_text_widget.insert(tk.END, f"Log file {log_file} not found.")
