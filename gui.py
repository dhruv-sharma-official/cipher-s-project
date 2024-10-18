
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk
import psutil  # To get real system info like CPU and memory usage
import os
import time
import threading

# Define necessary file paths
STATUS_FILE = 'status.txt'
COMMAND_FILE = 'command.txt'
PREMIUM_FOLDERS_FILE = 'premiumfolder.txt'
MONITORING_FOLDERS_FILE = 'monitoring_locations.txt'

# Initialize the root window
root = tk.Tk()
root.title("⚠ Cipher's Ransomware Solution ⚠")
root.geometry("900x700")
root.configure(bg="#0d0d0d")

# Set app icon if available
icon_path = "icon.ico"
if os.path.exists(icon_path):
    root.iconbitmap(icon_path)
else:
    print(f"Icon file not found at {icon_path}, skipping icon setting.")

# Custom styles for the advanced theme
style = ttk.Style()
style.theme_use('clam')
style.configure("TButton", font=("Consolas", 12), padding=6, background="#ff3333", foreground="white", borderwidth=0)
style.map("TButton", background=[('active', '#e60000')])
style.configure("TProgressbar", thickness=25, troughcolor='#262626', background='#ff3333')

# Adding a tabbed interface for different sections
notebook = ttk.Notebook(root)
notebook.pack(pady=20, expand=True)

# Create tabs
tab1 = ttk.Frame(notebook)
tab2 = ttk.Frame(notebook)
tab3 = ttk.Frame(notebook)
tab4 = ttk.Frame(notebook)
notebook.add(tab1, text='🛡 Scan System')
notebook.add(tab2, text='⚙ Settings')
notebook.add(tab3, text='📊 Logs')
notebook.add(tab4, text='📈 System Stats')

# --- Tab 1: Scan System (Start/Stop Monitoring and Force Premium Bridge) ---
title_label = tk.Label(tab1, text="🔒 Cipher's Ransomware Solution", font=("Consolas", 24, "bold"), bg="#0d0d0d", fg="#ff3333")
title_label.pack(pady=10)

# Add buttons for Start/Stop Monitoring and Force Premium Bridge
start_button = ttk.Button(tab1, text="Start Monitoring", command=lambda: write_command("START_MONITORING"))
start_button.pack(pady=5)

stop_button = ttk.Button(tab1, text="Stop Monitoring", command=lambda: write_command("STOP_MONITORING"))
stop_button.pack(pady=5)

force_bridge_button = ttk.Button(tab1, text="Force Premium Bridge", command=lambda: write_command("backup"))
force_bridge_button.pack(pady=5)

# --- Tab 2: Settings (Add Premium/Monitoring Folders) ---
add_premium_button = ttk.Button(tab2, text="Add Premium Folders", command=lambda: add_premium_folders())
add_premium_button.pack(pady=5)

add_monitoring_button = ttk.Button(tab2, text="Add Monitoring Folders", command=lambda: add_monitoring_folders())
add_monitoring_button.pack(pady=5)

# --- Tab 3: Logs (Realtime log updates) ---
log_panel = tk.Text(tab3, height=20, width=80, bg="#0d0d0d", fg="white", font=("Consolas", 12))
log_panel.pack(pady=10)

clearlogs = ttk.Button(tab3, text="clear logs", command=lambda: clear_output())
clearlogs.pack(pady=10)
# Function to update logs in real-time
def update_logs():
    while True:
        try:
            with open(STATUS_FILE, 'r') as file:
                content = file.read()
            log_panel.delete(1.0, tk.END)
            log_panel.insert(tk.END, content)
        except FileNotFoundError:
            log_panel.insert(tk.END, "No logs available yet.")
        time.sleep(2)

# Start the log update thread
log_thread = threading.Thread(target=update_logs, daemon=True)
log_thread.start()

# --- Tab 4: System Stats ---
def update_system_stats():
    cpu_label = tk.Label(tab4, text="CPU Usage: ", font=("Consolas", 14), bg="#0d0d0d", fg="white")
    cpu_label.pack(pady=5)
    memory_label = tk.Label(tab4, text="Memory Usage: ", font=("Consolas", 14), bg="#0d0d0d", fg="white")
    memory_label.pack(pady=5)

    while True:
        cpu_usage = psutil.cpu_percent(interval=1)
        memory_info = psutil.virtual_memory().percent

        cpu_label.config(text=f"CPU Usage: {cpu_usage}%")
        memory_label.config(text=f"Memory Usage: {memory_info}%")
        time.sleep(2)

system_stats_thread = threading.Thread(target=update_system_stats, daemon=True)
system_stats_thread.start()

# Helper functions for adding folders and sending commands
def add_premium_folders():
    folder_paths = filedialog.askdirectory(mustexist=True)
    if folder_paths:
        with open(PREMIUM_FOLDERS_FILE, 'a') as f:
            f.write(folder_paths + '\n')
        log_panel.insert(tk.END, f"Added premium folder: {folder_paths}\n")
    else:
        log_panel.insert(tk.END, "No premium folder selected.\n")

def add_monitoring_folders():
    folder_paths = filedialog.askdirectory(mustexist=True)
    if folder_paths:
        with open(MONITORING_FOLDERS_FILE, 'a') as f:
            f.write(folder_paths + '\n')
        log_panel.insert(tk.END, f"Added monitoring folder: {folder_paths}\n")
    else:
        log_panel.insert(tk.END, "No monitoring folder selected.\n")

def write_command(command):
    with open(COMMAND_FILE, 'w') as command_file:
        command_file.write(f"{command}\n")
    log_panel.insert(tk.END, f"Command Sent: {command}\n")

def clear_output():
    log_panel.delete(1.0, tk.END)
    with open(STATUS_FILE, 'w') as command_file:
        command_file.write("")

root.mainloop()
