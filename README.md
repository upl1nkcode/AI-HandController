# AI-HandController v0.1
- Cota Andrei & Cretu Beatrice
Lightweight Python prototype that maps simple hand gestures to keyboard input using MediaPipe, OpenCV and PyAutoGUI. Includes a small Tkinter GUI to choose image / video / webcam modes and basic settings.

## Features (V0.1)
- Detect gestures from:
  - Image file (`Detect from Image`)
  - Video file (`Detect from Video`)
  - Live webcam (`Detect from Webcam`)
- Heuristic gesture recognition for a single hand:
  - `open` (all fingers open)
  - `fist` (no fingers open)
  - `left` / `right` (based on hand horizontal position)
- Two control schemes:
  - `WASD` (default)
  - `Arrow`
- Simulates keyboard presses via `pyautogui` when using webcam mode.
- Basic Tkinter GUI in `Gesture/app_gui.py` for mode selection and settings (camera index, control scheme).

## Requirements
- Python 3.8+
- Packages:
  - `mediapipe`
  - `opencv-python`
  - `numpy`
  - `pyautogui`
- `tkinter` (usually included with standard Python installs on Windows)

Install dependencies:
```bash
pip install mediapipe opencv-python numpy pyautogui
