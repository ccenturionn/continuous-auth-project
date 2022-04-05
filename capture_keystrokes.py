import time
from asyncio.windows_events import NULL

import pandas as pd
from pynput import keyboard

start = 0
end = 0
keystroke_array = []
count = 0
prev_key = None

def on_press(key):
    """
    Called when a key is pressed. Get the time that the key is pressed and append to keystroke array.
    """

    global start, keystroke_array, count, prev_key 
    start = time.perf_counter_ns()
    start /= 1000000

    try:
        keystroke_array.append([key.char, start, "Pressed", prev_key])
    except AttributeError:
        keystroke_array.append([key, start, "Pressed", prev_key])

def on_release(key):
    """
    Called when a key is released. Get the time that the key is released and append to keystroke array.
    """

    global end, start, keystroke_array, count, prev_key
    end = time.perf_counter_ns()
    end /= 1000000

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
    input("Please type the following passage of text and press 'Enter' once finished. Press 'Enter' to continue...")

    print("one day, a zebra found a xylophone on the sidewalk. he quickly ran over, picked it up, and gave it to his pet mule. just then, he found another xylophone. he kept that one for himself")


    # Collect events until released
    listener = keyboard.Listener(on_press=on_press, on_release=on_release)
    listener.start()

    input()

    keystroke_array = pd.DataFrame(keystroke_array)
    keystroke_array.columns = ["Key", "Time", "Action", "PrevKey"]

    listener.stop()
    return keystroke_array




