"""
Harmless RAT Simulator - Educational Demo
------------------------------------------
This program is intentionally confined to its own GUI.

It DOES NOT:
- connect to or control another computer
- capture real keyboard input outside this window
- capture the real screen/camera/microphone
- access real files
- execute arbitrary system commands
- install persistence
- steal credentials

Run with:
    python rat_simulator.py
"""

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import platform
import random
import socket


class RATSimulator:
    def __init__(self, root):
        self.root = root
        self.root.title("RAT Simulator — EDUCATIONAL / SIMULATION ONLY")
        self.root.geometry("1100x700")
        self.root.minsize(900, 600)

        self.connected = False
        self.simulated_keys = []
        self.fake_files = [
            "Desktop/",
            "Desktop/demo_notes.txt",
            "Documents/",
            "Documents/project_report.pdf",
            "Documents/passwords_demo.txt",
            "Downloads/",
            "Downloads/example.zip",
            "Pictures/",
            "Pictures/demo_photo.jpg",
        ]

        self.setup_style()
        self.build_ui()
        self.log("Simulator started.")
        self.log("No real remote connection is used.")

    def setup_style(self):
        style = ttk.Style()
        try:
            style.theme_use("clam")
        except tk.TclError:
            pass

        style.configure("Title.TLabel", font=("Segoe UI", 20, "bold"))
        style.configure("Heading.TLabel", font=("Segoe UI", 12, "bold"))
        style.configure("Status.TLabel", font=("Segoe UI", 11, "bold"))

    def build_ui(self):
        header = ttk.Frame(self.root, padding=12)
        header.pack(fill="x")

        ttk.Label(
            header,
            text="RAT Simulator",
            style="Title.TLabel"
        ).pack(side="left")

        self.status_var = tk.StringVar(value="● DISCONNECTED")
        self.status_label = ttk.Label(
            header,
            textvariable=self.status_var,
            style="Status.TLabel"
        )
        self.status_label.pack(side="right")

        warning = tk.Label(
            self.root,
            text="⚠ SIMULATION ONLY — No real remote access, surveillance, or system control",
            font=("Segoe UI", 10, "bold"),
            fg="white",
            bg="#8a1c1c",
            pady=7
        )
        warning.pack(fill="x")

        main = ttk.Frame(self.root, padding=12)
        main.pack(fill="both", expand=True)

        left = ttk.LabelFrame(main, text="Controller / Attacker Console", padding=10)
        left.pack(side="left", fill="both", expand=True, padx=(0, 6))

        right = ttk.LabelFrame(main, text="Simulated Victim", padding=10)
        right.pack(side="right", fill="both", expand=True, padx=(6, 0))

        # Controller
        controls = ttk.Frame(left)
        controls.pack(fill="x", pady=(0, 10))

        ttk.Button(
            controls, text="Connect", command=self.connect
        ).pack(side="left", padx=3)

        ttk.Button(
            controls, text="Disconnect", command=self.disconnect
        ).pack(side="left", padx=3)

        ttk.Button(
            controls, text="System Info", command=self.system_info
        ).pack(side="left", padx=3)

        ttk.Button(
            controls, text="Fake Screenshot", command=self.fake_screenshot
        ).pack(side="left", padx=3)

        command_frame = ttk.LabelFrame(left, text="Safe Command Simulator", padding=8)
        command_frame.pack(fill="x", pady=5)

        self.command_var = tk.StringVar()
        command_entry = ttk.Entry(command_frame, textvariable=self.command_var)
        command_entry.pack(side="left", fill="x", expand=True, padx=(0, 5))
        command_entry.bind("<Return>", lambda _e: self.run_command())

        ttk.Button(
            command_frame, text="Run", command=self.run_command
        ).pack(side="right")

        ttk.Label(
            command_frame,
            text="Try: whoami, hostname, ipconfig, dir, help"
        ).pack(anchor="w", pady=(6, 0))

        file_frame = ttk.LabelFrame(left, text="Fake File Browser", padding=8)
        file_frame.pack(fill="both", expand=True, pady=5)

        self.file_list = tk.Listbox(file_frame, height=10)
        self.file_list.pack(fill="both", expand=True)

        for item in self.fake_files:
            self.file_list.insert("end", item)

        ttk.Button(
            file_frame,
            text="Simulate Download",
            command=self.simulate_download
        ).pack(anchor="e", pady=(7, 0))

        # Victim
        info_frame = ttk.LabelFrame(right, text="Fake System Information", padding=8)
        info_frame.pack(fill="x")

        self.info_text = tk.Text(info_frame, height=9, wrap="word")
        self.info_text.pack(fill="both", expand=True)
        self.info_text.insert("end", self.get_fake_system_info())
        self.info_text.config(state="disabled")

        key_frame = ttk.LabelFrame(
            right,
            text="Safe Keylogger Demonstration",
            padding=8
        )
        key_frame.pack(fill="both", expand=True, pady=8)

        ttk.Label(
            key_frame,
            text="Only characters typed into THIS demo box are recorded:"
        ).pack(anchor="w")

        self.demo_input = tk.Text(key_frame, height=6, wrap="word")
        self.demo_input.pack(fill="x", pady=5)
        self.demo_input.bind("<KeyPress>", self.capture_demo_key)

        self.key_log = tk.Text(key_frame, height=5, state="disabled")
        self.key_log.pack(fill="both", expand=True)

        ttk.Button(
            key_frame,
            text="Clear Demo Keystrokes",
            command=self.clear_keys
        ).pack(anchor="e", pady=(5, 0))

        log_frame = ttk.LabelFrame(right, text="Activity Log", padding=8)
        log_frame.pack(fill="both", expand=True)

        self.log_text = tk.Text(log_frame, height=8, state="disabled")
        self.log_text.pack(fill="both", expand=True)

    def timestamp(self):
        return datetime.now().strftime("%H:%M:%S")

    def log(self, message):
        self.log_text.config(state="normal")
        self.log_text.insert("end", f"[{self.timestamp()}] {message}\n")
        self.log_text.see("end")
        self.log_text.config(state="disabled")

    def connect(self):
        if self.connected:
            self.log("Already connected to simulated victim.")
            return

        self.connected = True
        self.status_var.set("● SIMULATED CONNECTION")
        self.log("Connected to simulated victim.")
        self.log("IMPORTANT: This is an in-process simulation only.")

    def disconnect(self):
        self.connected = False
        self.status_var.set("● DISCONNECTED")
        self.log("Disconnected from simulated victim.")

    def require_connection(self):
        if not self.connected:
            messagebox.showinfo(
                "Not Connected",
                "Click Connect first.\n\nThis simulator never creates a real network connection."
            )
            return False
        return True

    def get_fake_system_info(self):
        fake_host = "DEMO-PC"
        fake_ip = "192.0.2.100"  # Documentation/test address
        fake_user = "demo_user"

        return (
            "SYSTEM INFORMATION (FAKE)\n"
            "────────────────────────────\n"
            f"Hostname : {fake_host}\n"
            f"Username : {fake_user}\n"
            f"OS       : {platform.system()} (simulated)\n"
            f"Version  : {platform.release()} (simulated)\n"
            f"CPU      : Educational Demo CPU\n"
            f"RAM      : 8 GB (simulated)\n"
            f"IP       : {fake_ip}\n"
        )

    def system_info(self):
        if not self.require_connection():
            return

        self.log("Requested simulated system information.")

        self.info_text.config(state="normal")
        self.info_text.delete("1.0", "end")
        self.info_text.insert("end", self.get_fake_system_info())
        self.info_text.config(state="disabled")

    def fake_screenshot(self):
        if not self.require_connection():
            return

        self.log("Generated a simulated screenshot placeholder.")

        win = tk.Toplevel(self.root)
        win.title("Simulated Screenshot")
        win.geometry("700x400")

        canvas = tk.Canvas(win, bg="#20242b", highlightthickness=0)
        canvas.pack(fill="both", expand=True)

        canvas.create_text(
            350, 130,
            text="SIMULATED SCREENSHOT",
            fill="white",
            font=("Segoe UI", 26, "bold")
        )
        canvas.create_text(
            350, 190,
            text="No real screen was captured.",
            fill="#cccccc",
            font=("Segoe UI", 14)
        )
        canvas.create_text(
            350, 235,
            text="This image is generated entirely inside the demo.",
            fill="#aaaaaa",
            font=("Segoe UI", 11)
        )

    def run_command(self):
        if not self.require_connection():
            return

        command = self.command_var.get().strip().lower()
        if not command:
            return

        self.command_var.set("")
        self.log(f"Simulated command: {command}")

        responses = {
            "help": (
                "SAFE DEMO COMMANDS:\n"
                "whoami     → returns fake username\n"
                "hostname   → returns fake hostname\n"
                "ipconfig   → returns fake network information\n"
                "dir        → shows fake directory listing\n"
                "clear      → clears the command log"
            ),
            "whoami": "demo_user",
            "hostname": "DEMO-PC",
            "ipconfig": (
                "Ethernet adapter Demo:\n"
                "   IPv4 Address : 192.0.2.100\n"
                "   Subnet Mask  : 255.255.255.0\n"
                "   Gateway      : 192.0.2.1\n"
                "(All values are simulated.)"
            ),
            "dir": "\n".join(self.fake_files),
            "clear": ""
        }

        if command in responses:
            response = responses[command]
        else:
            response = (
                "Command blocked by safety design.\n"
                "Only predefined educational commands are available."
            )

        if command == "clear":
            self.log_text.config(state="normal")
            self.log_text.delete("1.0", "end")
            self.log_text.config(state="disabled")
            self.log("Command log cleared.")
            return

        self.log(f"Result: {response.replace(chr(10), ' | ')}")

        messagebox.showinfo(
            f"Simulated: {command}",
            response
        )

    def simulate_download(self):
        if not self.require_connection():
            return

        selection = self.file_list.curselection()
        if not selection:
            messagebox.showinfo(
                "Fake File Browser",
                "Select a fake file first."
            )
            return

        filename = self.file_list.get(selection[0])

        if filename.endswith("/"):
            messagebox.showinfo(
                "Fake File Browser",
                "That item is a simulated directory."
            )
            return

        self.log(f"Simulated download requested: {filename}")

        messagebox.showinfo(
            "Simulation",
            f"Simulated download of:\n\n{filename}\n\n"
            "No real file was accessed or transferred."
        )

    def capture_demo_key(self, event):
        # This handler receives key events ONLY from self.demo_input.
        key = event.keysym

        if key == "BackSpace":
            entry = "[BACKSPACE]"
        elif key == "Return":
            entry = "[ENTER]"
        elif key == "space":
            entry = " "
        elif len(event.char) == 1:
            entry = event.char
        else:
            entry = f"[{key}]"

        self.simulated_keys.append(entry)

        self.key_log.config(state="normal")
        self.key_log.delete("1.0", "end")
        self.key_log.insert(
            "end",
            "".join(self.simulated_keys)
        )
        self.key_log.config(state="disabled")

    def clear_keys(self):
        self.simulated_keys.clear()
        self.key_log.config(state="normal")
        self.key_log.delete("1.0", "end")
        self.key_log.config(state="disabled")
        self.log("Demo keystroke buffer cleared.")


def main():
    root = tk.Tk()
    app = RATSimulator(root)
    root.mainloop()


if __name__ == "__main__":
    main()
