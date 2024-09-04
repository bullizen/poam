import tkinter as tk
import psutil
import time

# Funktion för att uppdatera hälsoindikatorer
def update_health_indicators():
    # CPU-användning
    cpu_usage = psutil.cpu_percent(interval=1)
    cpu_label.config(text=f"CPU Usage: {cpu_usage}%")
    
    # Minnesanvändning
    memory_info = psutil.virtual_memory()
    memory_usage = memory_info.percent
    memory_label.config(text=f"Memory Usage: {memory_usage}%")
    
    # Diskanvändning
    disk_info = psutil.disk_usage('/')
    disk_usage = disk_info.percent
    disk_label.config(text=f"Disk Usage: {disk_usage}%")
    
    # Nätverksanvändning
    net_info = psutil.net_io_counters()
    net_sent = net_info.bytes_sent / (1024 * 1024)  # Omvandla till MB
    net_recv = net_info.bytes_recv / (1024 * 1024)  # Omvandla till MB
    network_label.config(text=f"Network: Sent: {net_sent:.2f} MB, Recv: {net_recv:.2f} MB")
    
    # Uppdatera igen efter 1000 ms (1 sekund)
    root.after(1000, update_health_indicators)

# Skapa Tkinter-fönstret
root = tk.Tk()
root.title("Health Indicators")

# Skapa och placera etiketter för varje hälsoindikator
cpu_label = tk.Label(root, text="CPU Usage: Calculating...", font=('Helvetica', 12))
cpu_label.pack(pady=10)

memory_label = tk.Label(root, text="Memory Usage: Calculating...", font=('Helvetica', 12))
memory_label.pack(pady=10)

disk_label = tk.Label(root, text="Disk Usage: Calculating...", font=('Helvetica', 12))
disk_label.pack(pady=10)

network_label = tk.Label(root, text="Network: Calculating...", font=('Helvetica', 12))
network_label.pack(pady=10)

# Börja uppdatera hälsoindikatorer
update_health_indicators()

# Starta huvudloopen i Tkinter
root.mainloop()
