# app_gui.py
import tkinter as tk
from tkinter import filedialog, simpledialog, messagebox
from GestureDetector import GestureDetector

class DetectorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("AI Gesture Control")
        self.root.minsize(350, 250)
        self.root.resizable(True, True)

        # Default camera index
        self.camera_index = 0

        # Initialize detector
        self.detector = GestureDetector()

        # --- UI Layout ---
        tk.Label(root, text="Select Detection Mode", font=("Arial", 14, "bold")).pack(pady=10)

        tk.Button(root, text="🖼 Detect from Image", command=self.from_image, width=25).pack(pady=5)
        tk.Button(root, text="🎥 Detect from Video", command=self.from_video, width=25).pack(pady=5)
        tk.Button(root, text="📷 Detect from Webcam", command=self.from_webcam, width=25).pack(pady=5)

        tk.Label(root, text=f"Current Camera Index: {self.camera_index}", fg="gray").pack(pady=5)
        tk.Button(root, text="⚙️ Settings", command=self.open_settings, width=25).pack(pady=5)

        tk.Button(root, text="❌ Exit", command=root.quit, width=25, bg="red", fg="white").pack(pady=10)

    # --- Detection Functions ---
    def from_image(self):
        file_path = filedialog.askopenfilename(
            title="Select Image",
            filetypes=[("Image Files", "*.jpg *.png *.jpeg")]
        )
        if file_path:
            self.detector.detect_image(file_path)

    def from_video(self):
        file_path = filedialog.askopenfilename(
            title="Select Video",
            filetypes=[("Video Files", "*.mp4 *.avi *.mov")]
        )
        if file_path:
            self.detector.detect_video(file_path)

    def from_webcam(self):
        self.detector.detect_webcam(cam_index=self.camera_index)

    # --- Settings Window ---
    def open_settings(self):
        settings_window = tk.Toplevel(self.root)
        settings_window.title("Settings")
        settings_window.geometry("300x250")
        settings_window.resizable(False, False)

        tk.Label(settings_window, text="Camera Input Settings", font=("Arial", 12, "bold")).pack(pady=10)
        tk.Label(settings_window, text="Enter camera index (0, 1, 2, ...):").pack(pady=5)

        cam_entry = tk.Entry(settings_window, width=10)
        cam_entry.insert(0, str(self.camera_index))
        cam_entry.pack(pady=5)

        # --- Control Mode Dropdown ---
        tk.Label(settings_window, text="Control Scheme:").pack(pady=8)
        control_var = tk.StringVar(value=self.detector.control_mode)
        control_menu = tk.OptionMenu(settings_window, control_var, "WASD", "Arrow", "Mouse")
        control_menu.pack(pady=5)

        def save_settings():
            try:
                new_index = int(cam_entry.get())
                self.camera_index = new_index
                # Save control mode to detector
                self.detector.control_mode = control_var.get()
                messagebox.showinfo("Settings Saved",
                                    f"✅ Camera index set to {new_index}\n🎮 Control mode: {self.detector.control_mode}")
                settings_window.destroy()
                self.refresh_label()
            except ValueError:
                messagebox.showerror("Invalid Input", "❌ Please enter a valid number.")

        tk.Button(settings_window, text="💾 Save", command=save_settings,
                  width=15, bg="#4CAF50", fg="white").pack(pady=15)

    def refresh_label(self):
        for widget in self.root.pack_slaves():
            if isinstance(widget, tk.Label) and "Camera Index" in widget.cget("text"):
                widget.config(text=f"Current Camera Index: {self.camera_index}")

if __name__ == "__main__":
    root = tk.Tk()
    app = DetectorApp(root)
    root.mainloop()
