import tkinter as tk
from tkinter import messagebox
import cv2
from PIL import Image, ImageTk

class WebcamDemo:
    def __init__(self, root):
        self.root = root
        self.root.title("Safe Webcam Access Demo")
        self.root.geometry("900x700")
        self.root.resizable(False, False)

        self.cap = None
        self.running = False

        title = tk.Label(
            root,
            text="Safe Webcam Access Demo",
            font=("Segoe UI", 22, "bold")
        )
        title.pack(pady=(15, 5))

        self.status = tk.Label(
            root,
            text="● Camera OFF",
            font=("Segoe UI", 12, "bold")
        )
        self.status.pack(pady=5)

        self.video_label = tk.Label(
            root,
            text="Camera preview will appear here",
            font=("Segoe UI", 14),
            width=80,
            height=25,
            relief="solid",
            bd=1
        )
        self.video_label.pack(padx=20, pady=15)

        buttons = tk.Frame(root)
        buttons.pack(pady=10)

        self.start_button = tk.Button(
            buttons,
            text="Start Camera",
            command=self.start_camera,
            width=18,
            height=2
        )
        self.start_button.grid(row=0, column=0, padx=8)

        self.stop_button = tk.Button(
            buttons,
            text="Stop Camera",
            command=self.stop_camera,
            width=18,
            height=2,
            state=tk.DISABLED
        )
        self.stop_button.grid(row=0, column=1, padx=8)

        tk.Label(
            root,
            text="This demo only accesses the camera after you explicitly press Start Camera.",
            font=("Segoe UI", 10)
        ).pack(pady=5)

        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

    def start_camera(self):
        if self.running:
            return

        self.cap = cv2.VideoCapture(0)

        if not self.cap.isOpened():
            self.cap.release()
            self.cap = None
            messagebox.showerror(
                "Camera Error",
                "Could not open the camera. Check that it is connected and not being used by another application."
            )
            return

        self.running = True
        self.status.config(text="● Camera ON — preview active")
        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)
        self.update_frame()

    def update_frame(self):
        if not self.running or self.cap is None:
            return

        ok, frame = self.cap.read()

        if not ok:
            self.stop_camera()
            messagebox.showerror("Camera Error", "The camera stopped responding.")
            return

        # OpenCV uses BGR; Tkinter/PIL expects RGB.
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Keep the preview inside the application window.
        frame = cv2.resize(frame, (800, 480))

        image = Image.fromarray(frame)
        photo = ImageTk.PhotoImage(image=image)

        self.video_label.config(image=photo, text="")
        self.video_label.image = photo

        self.root.after(15, self.update_frame)

    def stop_camera(self):
        self.running = False

        if self.cap is not None:
            self.cap.release()
            self.cap = None

        self.video_label.config(
            image="",
            text="Camera preview stopped"
        )
        self.video_label.image = None

        self.status.config(text="● Camera OFF")
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)

    def on_close(self):
        self.stop_camera()
        self.root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = WebcamDemo(root)
    root.mainloop()
