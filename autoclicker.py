import keyboard
import mouse
import time

clicking = False

def toggle_clicking():
    global clicking
    clicking = not clicking
    if clicking:
        print("\nStarted clicking")
        start_clicking()
    else:
        print("Stopped clicking")

def start_clicking():
    while clicking:
        time.sleep(0.02)
        mouse.click('left')

keyboard.add_hotkey('ctrl+1', toggle_clicking)

# Keep the script running
keyboard.wait('esc')  # Use 'esc' to stop the script
