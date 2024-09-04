# System Health and SSH Monitoring Tool Sequence Diagram

```mermaid
sequenceDiagram
    participant User
    participant main.py
    participant config.py
    participant monitor.py
    participant gui.py

    User->>main.py: Run the script
    main.py->>config.py: Import and parse arguments
    config.py-->>main.py: Return parsed arguments
    main.py->>gui.py: Call create_gui() to initialize the GUI
    gui.py-->>main.py: Returns the root window
    main.py->>monitor.py: Start threads for update_health_indicators and update_ssh_info

    par System Health Monitoring
        monitor.py->>psutil: Get CPU, Memory, Disk, and Network Usage
        monitor.py->>gui.py: Update labels with usage data
        gui.py-->>monitor.py: Labels updated
        monitor.py->>monitor.py: Schedule next update in 1 second
    end

    par SSH Monitoring
        monitor.py->>subprocess: Get open ports (netstat/ss)
        monitor.py->>monitor.py: Check insecure files in directories
        monitor.py->>gui.py: Update SSH text areas
        gui.py-->>monitor.py: Text areas updated
        monitor.py->>monitor.py: Schedule next update in 60 seconds
    end

    main.py->>gui.py: Call start_gui(root) to start the main loop
    gui.py-->>User: GUI interacts with the user, displaying real-time data
