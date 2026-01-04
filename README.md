# HandGestureMouseControl

**HandGestureMouseControl** is a Python-based application that allows you to control your computer’s mouse cursor using hand gestures. By utilizing the **MediaPipe** hand tracking library, this program recognizes specific hand gestures and translates them into mouse actions.

## Features:
- **Index Finger**: Move the cursor on the screen based on the finger’s position.
- **Fist Gesture**: Perform left-click and drag actions by making a fist.
- **Peace Sign**: Trigger right-click actions by forming a peace sign.
- **Smooth Cursor Movement**: The program uses smoothing to provide a more natural and fluid cursor movement.

This tool is ideal for anyone interested in exploring gesture-based control systems or looking for an accessible way to control a computer without using a traditional mouse or touchpad.

## Requirements:
- **Python 3.x**
- **Libraries**: `cv2`, `mediapipe`, `pyautogui`
  
  Install them using:
  ```bash
  pip install opencv-python mediapipe pyautogui
