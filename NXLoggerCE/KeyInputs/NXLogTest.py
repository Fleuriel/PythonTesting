from pynput import keyboard
from pathlib import Path
import datetime

# Set up log file in the same directory as script
SCRIPT_DIR = Path(__file__).resolve().parent
LOG_FILE = SCRIPT_DIR / "keystrokes.log"

ALLOWED_KEYS = {'w', 'a', 's', 'd'}
STOP_KEY = 'q'

# Listener object will be accessible to stop it
listener = None

def on_press(key):
    global listener
    try:
        k = key.char.lower()
        if k == STOP_KEY:
            print("Exit key detected. Stopping listener.")
            listener.stop()  # Stop the listener
        elif k in ALLOWED_KEYS:
            with open(LOG_FILE, "a") as f:
                f.write(f"{datetime.datetime.now()} - Pressed: {k}\n")
    except AttributeError:
        pass  # Special keys (e.g., shift)

print("W A S D keys are programmed to log into keystrokes.log.")
print("Keylogger running. Press 'q' to stop.")
listener = keyboard.Listener(on_press=on_press)
listener.start()
listener.join()
