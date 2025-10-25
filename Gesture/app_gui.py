# app_gui.py
import tkinter as tk
from tkinter import filedialog
from GestureDetector import GestureDetector

class DetectorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("AI Vision Detector")
        self.root.minsize(350, 250)
        self.root.resizable(True, True)
        self.detector = GestureDetector()

        tk.Label(root, text="Select Detection Mode", font=("Arial", 14, "bold")).pack(pady=10)

        tk.Button(root, text="🖼 Detect from Image", command=self.from_image, width=25).pack(pady=5)
        tk.Button(root, text="🎥 Detect from Video", command=self.from_video, width=25).pack(pady=5)
        tk.Button(root, text="📷 Detect from Webcam", command=self.from_webcam, width=25).pack(pady=5)

        tk.Button(root, text="❌ Exit", command=root.quit, width=25, bg="red", fg="white").pack(pady=10)

    def from_image(self):
        file_path = filedialog.askopenfilename(title="Select Image", filetypes=[("Image Files", "*.jpg *.png *.jpeg")])
        if file_path:
            self.detector.detect_image(file_path)

    def from_video(self):
        file_path = filedialog.askopenfilename(title="Select Video", filetypes=[("Video Files", "*.mp4 *.avi *.mov")])
        if file_path:
            self.detector.detect_video(file_path)

    def from_webcam(self):
        self.detector.detect_webcam()

if __name__ == "__main__":
    root = tk.Tk()
    app = DetectorApp(root)
    root.mainloop()
