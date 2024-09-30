# Working print to screen loop

import tkinter as tk
import keyboard as kb
import mouse as ms

# List to keep track of all created windows
root = tk.Tk()
root.withdraw()
translation_enabled = False
windows = []

def close_translation_boxes():
    global windows
    for window in windows:
        window.destroy()
    windows = []

def create_borderless_window(x, y, text):
    # Create a Toplevel window
    root = tk.Toplevel()
    windows.append(root)  # Add the window to the list of created windows
    root.overrideredirect(True)  # Remove window border and title bar

    # Set window dimensions and position
    root.geometry(f"{200}x{200}+{x}+{y}")

    # Create a label with the specified text
    label = tk.Label(root, text=text, font=("Helvetica", 16))
    label.pack(pady=20)

# Toggle whether the translation program overlay should be activated or not
def toggle_translation_program():
    global translation_enabled
    translation_enabled = not translation_enabled
    if not translation_enabled:
        close_translation_boxes()

# Function to be executed once after no input for >=1 second
def translate_after_input():
    global timer_active
    timer_active = False
    if translation_enabled:
        # Example usage
        create_borderless_window(400, 200, "Window 1")
        create_borderless_window(300, 150, "Window 2")
        create_borderless_window(500, 300, "Window 3")

# Reset timer function
def reset_timer(event):
    global root, timer_active
    if not timer_active:
        close_translation_boxes()
        root.after(1000, translate_after_input)
        timer_active = True

# Closes the entire program
def close_program():
    root.quit()

timer_active = False

# Bind Escape keypress to close all windows and reset timer on keyboard and mouse callbacks
kb.hook(reset_timer)
ms.hook(reset_timer)

# Turn on the translation program and exit the program
kb.add_hotkey('ctrl+shift+1', close_program)
kb.add_hotkey('ctrl+shift+2', toggle_translation_program)

# Run the Tkinter event loop
tk.mainloop()

# Cleanup
kb.unhook_all()
ms.unhook_all()