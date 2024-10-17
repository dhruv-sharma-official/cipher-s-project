import os
import tkinter as tk
from tkinter import scrolledtext, simpledialog, messagebox, filedialog
import time
import threading

STATUS_FILE = "status.txt"
COMMAND_FILE = "command.txt"
PREMIUM_FOLDERS_FILE = "premiumfolder.txt"

class MonitorGUI(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Ransomware Monitor Control Panel")
        self.geometry("600x400")

        # Output Panel (Scrolled Textbox)
        self.output_panel = scrolledtext.ScrolledText(self, wrap=tk.WORD, width=70, height=20)
        self.output_panel.pack(pady=10)

        # Buttons
        self.start_button = tk.Button(self, text="Start Monitoring", command=self.start_monitoring)
        self.start_button.pack(side=tk.LEFT, padx=10, pady=5)

        self.stop_button = tk.Button(self, text="Stop Monitoring", command=self.stop_monitoring)
        self.stop_button.pack(side=tk.LEFT, padx=10, pady=5)

        self.clear_output_button = tk.Button(self, text="Clear Output", command=self.clear_output)
        self.clear_output_button.pack(side=tk.LEFT, padx=10, pady=5)

        self.premium_bridge = tk.Button(self, text="Force Premium Bridge", command=self.backup)
        self.premium_bridge.pack(side=tk.LEFT, padx=10, pady=5)

        self.premium_folders_button = tk.Button(self, text="Premium Folders", command=self.add_premium_folders)
        self.premium_folders_button.pack(side=tk.LEFT, padx=10, pady=5)

        # Start a thread to keep updating the status output
        self.update_thread = threading.Thread(target=self.update_output)
        self.update_thread.daemon = True
        self.update_thread.start()

    def backup(self):
        self.write_command("backup")
        self.output_panel.insert(tk.END, "Command Sent: Backup\n")

    def add_premium_folders(self):
        """Allows user to select folder paths and saves them to premiumfolder.txt."""
        folder_paths = filedialog.askdirectory(mustexist=True)  # Allows selection of a single directory
        if folder_paths:
            with open(PREMIUM_FOLDERS_FILE, 'a') as f:
                f.write(folder_paths + '\n')
            self.output_panel.insert(tk.END, f"Added folder: {folder_paths}\n")
        else:
            self.output_panel.insert(tk.END, "No folder selected.\n")

    def read_status_file(self):
        """Reads the status from status.txt and returns its content."""
        try:
            with open(STATUS_FILE, 'r') as file:
                return file.read()
        except FileNotFoundError:
            return "No status file found."

    def update_output(self):
        """Continuously updates the output panel with new status updates."""
        while True:
            status_content = self.read_status_file()
            self.output_panel.delete(1.0, tk.END)  # Clear previous output
            self.output_panel.insert(tk.END, status_content)  # Insert new content
            time.sleep(2)  # Refresh every 2 seconds

    def write_command(self, command):
        """Writes a command to the command.txt file."""
        with open(COMMAND_FILE, 'w') as command_file:
            command_file.write(f"{command}\n")

    def start_monitoring(self):
        """Command to start monitoring."""
        self.write_command("START_MONITORING")
        self.output_panel.insert(tk.END, "Command Sent: Start Monitoring\n")

    def stop_monitoring(self):
        """Command to stop monitoring."""
        self.write_command("STOP_MONITORING")
        self.output_panel.insert(tk.END, "Command Sent: Stop Monitoring\n")

    def clear_output(self):
        """Clears the output panel."""
        self.output_panel.delete(1.0, tk.END)

if __name__ == "__main__":
    gui = MonitorGUI()
    gui.mainloop()
