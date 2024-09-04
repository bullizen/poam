import argparse
import platform

def parse_arguments():
    """
    Parse command-line arguments for the System Health and SSH Monitoring Tool.

    This function sets up an argument parser to handle various command-line options
    related to system health monitoring and email notifications. It includes thresholds
    for CPU, memory, disk, and network usage, as well as email settings for sending alerts.

    Returns:
        argparse.Namespace: Parsed command-line arguments.

    Command-line Arguments:
        --cpu (int): CPU usage warning threshold (%). Default is 80.
        --memory (int): Memory usage warning threshold (%). Default is 80.
        --disk (int): Disk usage warning threshold (%). Default is 90.
        --network (float): Network usage warning threshold (MB/s). Default is 100.0.
        --insecure_dirs (list of str): Directories to scan for insecure files. Default is 
            "C:\\ProgramData" on Windows and "/etc" on other platforms.
        --email_from (str): Sender email address. Default is "your_email@example.com".
        --email_to (str): Recipient email address. Default is "admin@example.com".
        --smtp_server (str): SMTP server address. Default is "smtp.example.com".
        --smtp_port (int): SMTP server port. Default is 587.
        --smtp_username (str): SMTP username. Default is "your_email@example.com".
        --smtp_password (str): SMTP password. Default is "your_password".
    """
    if platform.system() == "Windows":
        default_dir = "C:\\ProgramData"
    else:
        default_dir = "/etc"

    parser = argparse.ArgumentParser(description="System Health and SSH Monitoring Tool")
    parser.add_argument("--cpu", type=int, default=80, help="CPU usage warning threshold (%%)")
    parser.add_argument("--memory", type=int, default=80, help="Memory usage warning threshold (%%)")
    parser.add_argument("--disk", type=int, default=90, help="Disk usage warning threshold (%%)")
    parser.add_argument("--network", type=float, default=100.0, help="Network usage warning threshold (MB/s)")
    parser.add_argument("--insecure_dirs", nargs="*", default=[default_dir], help="Directories to scan for insecure files")
    
    # Email settings
    parser.add_argument("--email_from", type=str, default="your_email@example.com", help="Sender email address")
    parser.add_argument("--email_to", type=str, default="admin@example.com", help="Recipient email address")
    parser.add_argument("--smtp_server", type=str, default="smtp.example.com", help="SMTP server address")
    parser.add_argument("--smtp_port", type=int, default=587, help="SMTP server port")
    parser.add_argument("--smtp_username", type=str, default="your_email@example.com", help="SMTP username")
    parser.add_argument("--smtp_password", type=str, default="your_password", help="SMTP password")
    
    return parser.parse_args()

args = parse_arguments()
