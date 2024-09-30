from pytesseract import pytesseract, Output
from googletrans import Translator
from PIL import ImageGrab as image
# from sklearn.cluster import OPTICS
from sklearn.cluster import AgglomerativeClustering
from autocorrect import Speller
import pyautogui as gui
import tkinter as tk
import keyboard as kb
import mouse as ms
import numpy as np
import os

"""
END OF IMPORTED LIBRARIES
BEGINNING OF USER CUSTOMIZATION
"""

# Path to tesseract executable (Change this if needed)
tesseract_file_path = "C:\\Users\\N1bbL3R\\AppData\\Local\\Programs\\Tesseract-OCR\\tesseract.exe"
os.environ['TESSDATA_PREFIX'] = "C:\\Users\\N1bbL3R\\AppData\\Local\\Programs\\Tesseract-OCR\\tessdata"

# Source language to be translated to English, auto by default but can be hard set for increased accuracy
# https://tesseract-ocr.github.io/tessdoc/Data-Files-in-different-versions.html
source_language = 'Portuguese'
clustering_distance_threshold = 400

"""
END OF USER CUSTOMIZATION
BEGINNING OF TRANSLATION CODE
"""

# Currently supported languages
# 0 = pytesseract, 1 = googletrans & autocorrect
source_language_dictionary = {
    'Auto': ['auto', 'auto'],
    'Portuguese': ['por', 'pt'],
    'Italian': ['ita', 'it'],
    'Japanese': ['jpn', 'ja'],
    'Korean': ['kor', 'ko'],
    'French': ['fra', 'fr'],
    'Spanish': ['spa', 'es'],
    'Russian': ['rus', 'ru']
}

# Customized region for the program to read, currently set to the inner borders of a website
screen_width, screen_height = gui.size()
left = 0
top = int(screen_height * 0.06)
right = int(screen_width)
bottom = int(screen_height * 0.96)
text_region = (left, top, right, bottom)

# Initialize translation variables
source_language = source_language_dictionary[source_language]
pytesseract.tesseract_cmd = tesseract_file_path

def create_borderless_window(x, y, w, h, text):
    # Create a windowed borderless Toplevel window (subwindow of Tk)
    root = tk.Toplevel()
    windows.append(root)
    root.overrideredirect(True)

    # Set window dimensions and position
    root.geometry(f"{w}x{h}+{x}+{y}")

    # Create a label with the specified text
    label = tk.Label(root, text=text, font=("Ariel", 12), wraplength=w)
    label.pack(pady=20)

def check_for_misspells(text, lang=source_language[1]):
    # Check for any misspells due to inaccuracy in the pytesseract OCR
    spell_checker = Speller(lang=lang)
    words = text.split()
    return " ".join(spell_checker(word) if not spell_checker(word) else word for word in words)

def translate_text(text, source_lang=source_language[1], target_lang='en'):
    # Translate text to English
    translator = Translator()
    translated_text = translator.translate(check_for_misspells(text), src=source_lang, dest=target_lang)
    return translated_text.text

def print_translated_cluster(word_cluster, cluster_bbox):
    if word_cluster != "":
        # Set up rectangle values from bounding box
        x = left + cluster_bbox[0][0]
        y = top + cluster_bbox[0][1]
        w = cluster_bbox[1][0] - cluster_bbox[0][0]
        h = cluster_bbox[1][1] - cluster_bbox[0][1]

        # Draw a background rectangle and the translated text for the word cluster
        create_borderless_window(x, y, w, h, translate_text(word_cluster))

def detect_text_on_screen(lang = source_language[0]):
    global text_region, clustering_distance_threshold
    print("Detecting text on screen...")

    # Capture the screen
    if text_region:
        screen = image.grab(bbox=text_region)
    else:
        # xdisplay = 0 if display needs to be hard set to 0, otherwise uses default display
        screen = image.grab()

    # Take a picture of the current screen and create variables to be used to determine word clusters
    image_data = pytesseract.image_to_data(screen, output_type=Output.DICT, lang=lang)
    wrapped_word = ""

    # Initialize word cluster data variables
    words = []
    graphics_data = []
    clustering_data = []

    for i, word in enumerate(image_data['text']):
        if str(word).strip() != "":
            # Screen coordinates of each word
            x, y, w, h = image_data['left'][i], image_data['top'][i], image_data['width'][i], image_data['height'][i]

            # Pass information to help translation, information to help detect clusters, and information to help graphics  
            if word[-1] == '-':
                # Text is wrapped around a line
                graphics_data.append([x, y, w, h])
                clustering_data.append([x, y])
                wrapped_word = word
            elif wrapped_word != "":
                # Second half of word from wrapped text around a line
                words.append(wrapped_word + word)
                wrapped_word = ""
            else:
                # Default case where text is not wrapped
                words.append(word)
                graphics_data.append([x, y, w, h])
                clustering_data.append([x, y])

    # Detect word clusters and assign the results to word_cluster_identities
    agglomerative = AgglomerativeClustering(n_clusters=None, distance_threshold=clustering_distance_threshold)
    word_cluster_identities = agglomerative.fit_predict(np.array(clustering_data))

    print("Printing translated clusters...")

    # Initialize graphics data variables
    word_cluster = ""
    cluster_bbox = [[0, 0], [0, 0]]

    for i, data in enumerate(graphics_data):
        x, y, w, h = data
        
        if word_cluster_identities[i] != word_cluster_identities[i - 1]:
            # Upon detection of a new cluster, translate the old cluster
            if i != 0:
                print_translated_cluster(word_cluster, cluster_bbox)
            
            word_cluster = ""
            cluster_bbox = [[x, y], [x + w, y + h]]
        else:
            # While still in the current cluster, concatenate the words and update the bounding box
            word_cluster = word_cluster + words[i] + " "
            if x < cluster_bbox[0][0]:
                cluster_bbox[0][0] = x
            if y < cluster_bbox[0][1]:
                cluster_bbox[0][1] = y
            if x + w > cluster_bbox[1][0]:
                cluster_bbox[1][0] = x + w
            if y + h > cluster_bbox[1][1]:
                cluster_bbox[1][1] = y + h

    # Print the last cluster
    print_translated_cluster(word_cluster, cluster_bbox)

""" 
END OF TRANSLATION CODE
BEGINNING OF PROGRAM CONTROL FUNCTIONS
"""

def close_translation_boxes():
    global windows
    for window in windows:
        window.destroy()
    windows = []

# Toggle whether the translation program overlay should be activated or not
def toggle_translation_program():
    global translation_enabled
    print("Translation Program Toggled.")
    translation_enabled = not translation_enabled
    if not translation_enabled:
        close_translation_boxes()

# Function to be executed once after no input for >=1 second
def translate_after_input():
    global timer_active
    timer_active = False
    if translation_enabled:
        print("Detecting Screen Input...")
        detect_text_on_screen()

# Reset timer function, calls the control for translation code after no input for >=1 second 
def reset_timer(event):
    global root, timer_active
    if not timer_active:
        close_translation_boxes()
        root.after(1000, translate_after_input)
        timer_active = True

# Closes the entire program
def close_program():
    print("Program Ended.")
    root.quit()

""" 
END OF PROGRAM CONTROL FUNCTIONS
BEGINNING OF MAIN PROGRAM
"""

# Initialize main program variables
root = tk.Tk()
root.withdraw()
windows = []
# translation_enabled = False
# timer_active = False

# Bind Escape keypress to close all windows and reset timer on keyboard and mouse callbacks
# kb.hook(reset_timer)
# ms.hook(reset_timer)

# Turn on the translation program and exit the program
kb.add_hotkey('ctrl+shift+1', close_program)
kb.add_hotkey('ctrl+shift+2', detect_text_on_screen)

# Run the Tkinter event loop
tk.mainloop()

# Cleanup
kb.unhook_all()
ms.unhook_all()
