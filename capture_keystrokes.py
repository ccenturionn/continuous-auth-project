import time

import pandas as pd
from pynput import keyboard
import random

keystroke_array = []
prev_key = None

typing_prompts = ["Six javelins thrown by the quick savages whizzed forty paces beyond the mark.",
                "While making deep excavations we found some quaint bronze jewelry.",
                "We quickly seized the black axle and just saved it from going past him.",
                "Jaded zombies acted quietly but kept driving their oxen forward.",
                "The wizard quickly jinxed the gnomes before they vaporized.",
                "A quick movement of the enemy will jeopardize six gunboats.",
                "The July sun caused a fragment of black pine wax to ooze on the velvet quilt.",
                "A mad boxer shot a quick, gloved jab to the jaw of his dizzy opponent."]

def on_press(key):
    """
    Called when a key is pressed. Get the time that the key is pressed and append to keystroke array.
    """

    global keystroke_array, prev_key

    # Get time that key is pressed
    start = time.perf_counter_ns()
    start /= 1000000

    # Add keystroke data to keystroke_array
    try:
        keystroke_array.append([key.char, start, "Pressed", prev_key])
    except AttributeError:
        keystroke_array.append([key, start, "Pressed", prev_key])

def on_release(key):
    """
    Called when a key is released. Get the time that the key is released and append to keystroke array.
    """

    global keystroke_array, prev_key

    # Get time that key is released
    end = time.perf_counter_ns()
    end /= 1000000

    # Add keystroke data to keystroke_array
    try:
        keystroke_array.append([key.char, end, "Released", prev_key])
    except AttributeError:
        keystroke_array.append([key, end, "Released", prev_key])

    prev_key = key

def record_keystrokes():
    """
    Record keystroke data for a user
    """

    global keystroke_array
    keystroke_array = []

    # Prompt user for input
    input("Please type the following passage of text and press 'Enter' once finished. Press 'Enter' to continue...")
    print(typing_prompts[random.randrange(0, len(typing_prompts)-1)])


    # Start keyboard listener
    listener = keyboard.Listener(on_press=on_press, on_release=on_release)
    listener.start()

    input()

    # Convert keystroke_array to dataframe
    keystroke_array = pd.DataFrame(keystroke_array)
    keystroke_array.columns = ["Key", "Time", "Action", "PrevKey"]

    listener.stop()
    return keystroke_array

