"""
Harmless RAT Simulator
Educational cybersecurity demonstration.

SAFE BY DESIGN:
- Local GUI only
- No network connections
- No persistence
- No keylogging
- No credential collection
- No shell command execution
- File actions are restricted to a local demo folder
- Screenshot action creates a text placeholder only
"""

import platform
from datetime import datetime
from pathlib import Path
import tkinter as tk
from tkinter import messagebox

APP_DIR = Path(__file__).resolve().parent / "RAT_Simulator_Demo"
LOG_FILE = APP_DIR / "activity.log"
DEMO_FILE = APP_DIR / "demo_note.txt"


def now():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


class Simulator:
    def __init__(self, root):
        self.root = root
        self.root.title("Harmless RAT Simulator")
        self.root.geometry("900x620")
        self.root.minsize(760, 520)

        APP_DIR.mkdir(exist_ok=True)
        if not DEMO_FILE.exists():
            DEMO_FILE.write_text(
                "This is a harmless demonstration file.\n",
                encoding="utf-8",
            )

        self.build_ui()
        self.log("Simulator started")

    def log(self, message):
        line = f"[{now()}] {message}"
        with LOG_FILE.open("a", encoding="utf-8") as f:
            f.write(line + "\n")

        if hasattr(self, "log_box"):
            self.log_box.insert("end", line + "\n")
            self.log_box.see("end")

    def output(self, text):
        self.output_box.config(state="normal")
        self.output_box.delete("1.0", "end")
        self.output_box.insert("1.0", text)
        self.output_box.config(state="disabled")

    def build_ui(self):
        tk.Label(
            self.root,
            text="HARMLESS RAT SIMULATOR",
            font=("Segoe UI", 20, "bold"),
        ).pack(anchor="w", padx=18, pady=(15, 2))

        tk.Label(
            self.root,
            text="Educational simulation — LOCAL ONLY — no real remote control",
            font=("Segoe UI", 10),
        ).pack(anchor="w", padx=18)

        tk.Label(
            self.root,
            text="SAFE MODE: all file activity is confined to RAT_Simulator_Demo",
            font=("Segoe UI", 10, "bold"),
            padx=10,
            pady=8,
        ).pack(fill="x", padx=18, pady=12)

        main = tk.Frame(self.root)
        main.pack(fill="both", expand=True, padx=18, pady=(0, 10))

        left = tk.LabelFrame(main, text="Simulated RAT Features", padx=10, pady=10)
        left.pack(side="left", fill="y")

        actions = [
            ("System Information", self.system_info),
            ("List Demo Files", self.list_files),
            ("Create Demo File", self.create_file),
            ("Read Demo File", self.read_file),
            ("Delete Demo File", self.delete_file),
            ("Simulate Command", self.command),
            ("Simulate Screenshot", self.screenshot),
            ("Clear Log", self.clear_log),
        ]

        for label, command in actions:
            tk.Button(
                left,
                text=label,
                width=23,
                pady=6,
                command=command,
            ).pack(pady=4)

        right = tk.Frame(main)
        right.pack(side="left", fill="both", expand=True, padx=(15, 0))

        out_frame = tk.LabelFrame(right, text="Output", padx=8, pady=8)
        out_frame.pack(fill="both", expand=True)

        self.output_box = tk.Text(
            out_frame,
            wrap="word",
            font=("Consolas", 10),
            state="disabled",
        )
        self.output_box.pack(fill="both", expand=True)

        log_frame = tk.LabelFrame(right, text="Activity Log", padx=8, pady=8)
        log_frame.pack(fill="both", expand=True, pady=(10, 0))

        self.log_box = tk.Text(
            log_frame,
            height=8,
            wrap="word",
            font=("Consolas", 9),
        )
        self.log_box.pack(fill="both", expand=True)

        if LOG_FILE.exists():
            self.log_box.insert("1.0", LOG_FILE.read_text(encoding="utf-8"))
            self.log_box.see("end")

        self.status = tk.StringVar(value="Ready — SAFE LOCAL SIMULATION")
        tk.Label(
            self.root,
            textvariable=self.status,
            anchor="w",
            relief="sunken",
            padx=10,
            pady=5,
        ).pack(fill="x", side="bottom")

    def system_info(self):
        info = {
            "Mode": "SAFE LOCAL SIMULATION",
            "Computer": platform.node() or "Demo-PC",
            "OS": platform.platform(),
            "Python": platform.python_version(),
            "Architecture": platform.machine(),
            "Processor": platform.processor() or "Unavailable",
            "Demo folder": str(APP_DIR),
        }

        self.output("\n".join(f"{k}: {v}" for k, v in info.items()))
        self.status.set("System information simulated")
        self.log("Simulated system-information collection")

    def list_files(self):
        files = [p.name for p in sorted(APP_DIR.iterdir()) if p.is_file()]

        text = (
            "Files in RAT_Simulator_Demo:\n\n"
            + ("\n".join("• " + f for f in files) if files else "No files.")
        )

        self.output(text)
        self.status.set("Demo files listed")
        self.log("Listed demo-directory files")

    def create_file(self):
        path = APP_DIR / "simulated_remote_file.txt"
        path.write_text(
            f"Created by simulator at {now()}\n",
            encoding="utf-8",
        )

        self.output(
            "SIMULATED FILE CREATION\n\n"
            f"Created: {path.name}\n"
            f"Location: {APP_DIR}\n\n"
            "No files outside the demo folder are touched."
        )
        self.status.set("Demo file created")
        self.log(f"Created {path.name}")

    def read_file(self):
        content = DEMO_FILE.read_text(encoding="utf-8")
        self.output(
            "SIMULATED FILE READ\n\n"
            f"File: {DEMO_FILE.name}\n\n"
            f"Contents:\n{content}"
        )
        self.status.set("Demo file read")
        self.log(f"Read {DEMO_FILE.name}")

    def delete_file(self):
        path = APP_DIR / "simulated_remote_file.txt"

        if path.exists():
            path.unlink()
            result = f"Deleted {path.name}"
        else:
            result = "No simulated_remote_file.txt exists."

        self.output(
            "SIMULATED FILE DELETE\n\n"
            + result
            + "\n\nOnly the simulator's demo folder is affected."
        )
        self.status.set("File deletion simulated")
        self.log(result)

    def command(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("Safe Command Simulator")
        dialog.geometry("470x210")
        dialog.transient(self.root)
        dialog.grab_set()

        tk.Label(
            dialog,
            text="Enter a simulated command:",
            font=("Segoe UI", 10, "bold"),
        ).pack(pady=(18, 5))

        entry = tk.Entry(dialog, width=48)
        entry.pack(pady=5)
        entry.focus()

        allowed = {
            "whoami": "demo-user",
            "hostname": platform.node() or "DEMO-PC",
            "ver": platform.platform(),
            "date": now(),
            "help": "Allowed: whoami, hostname, ver, date, help",
        }

        def run():
            command = entry.get().strip().lower()

            if command in allowed:
                result = allowed[command]
                self.output(
                    "SIMULATED COMMAND\n\n"
                    f"> {command}\n\n"
                    f"{result}\n\n"
                    "The operating system command was NOT executed."
                )
                self.log(f"Simulated command: {command}")
                self.status.set("Safe command simulated")
            else:
                self.output(
                    "COMMAND BLOCKED\n\n"
                    "Only fixed demonstration commands are allowed.\n"
                    "No shell commands are executed by this program."
                )
                self.log(f"Blocked command: {command!r}")
                self.status.set("Unsupported command blocked")

            dialog.destroy()

        tk.Button(dialog, text="Simulate", command=run, width=15).pack(pady=12)

    def screenshot(self):
        placeholder = APP_DIR / "simulated_screenshot.txt"
        placeholder.write_text(
            "This is NOT an image.\n"
            "It represents a simulated screenshot-collection event.\n",
            encoding="utf-8",
        )

        self.output(
            "SIMULATED SCREENSHOT\n\n"
            "No screenshot was captured.\n"
            f"Created placeholder: {placeholder.name}"
        )
        self.status.set("Screenshot event simulated")
        self.log("Simulated screenshot event; no image captured")

    def clear_log(self):
        if not messagebox.askyesno("Clear Log", "Clear the simulator log?"):
            return

        LOG_FILE.write_text("", encoding="utf-8")
        self.log_box.delete("1.0", "end")
        self.output("Activity log cleared.")
        self.status.set("Log cleared")


def main():
    root = tk.Tk()
    Simulator(root)
    root.mainloop()


if __name__ == "__main__":
    main()
