from asyncio.windows_events import NULL
from pynput import keyboard
import numpy as np
import pandas as pd
import time
import pickle

start = 0
end = 0
keystroke_array = []
count = 0
prev_key = None

def on_press(key):
    global start, keystroke_array, count, prev_key 
    start = time.perf_counter_ns()
    start /= 1000000
    # try:
    #     print(f'alphanumeric key {key.char} pressed')
    # except AttributeError:
    #     print(f'special key {key} pressed')

    # Stop recording keystrokes if user presses Esc
    if key == keyboard.Key.esc:
        # Stop listener
        return False

    try:
        keystroke_array.append([key, start, "Pressed", prev_key])
    except AttributeError:
        keystroke_array.append([key, start, "Pressed", prev_key])

def on_release(key):
    global end, start, keystroke_array, count, prev_key
    end = time.perf_counter_ns()
    end /= 1000000
    # print(f'{key} released after {end - start} milliseconds')

    try:
        keystroke_array.append([key, end, "Released", prev_key])
    except AttributeError:
        keystroke_array.append([key, end, "Released", prev_key])

    prev_key = key

def record_keystrokes():
    global keystroke_array
    input("Please type the following passage of text and press 'Esc' once finished. Press 'Enter' to continue...")

    print("one day, a zebra found a xylophone on the sidewalk. he quickly ran over, picked it up, and gave it to his pet mule. just then, he found another xylophone. he kept that one for himself")

    # Collect events until released
    # with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    #     listener.join()

    # Collect events until released
    listener = keyboard.Listener(on_press=on_press, on_release=on_release)
    listener.start()

    input()

    keystroke_array = pd.DataFrame(keystroke_array)
    keystroke_array.columns = ["Key", "Time", "Action", "PrevKey"]
    print(keystroke_array)

    with open("keystroke_data", 'wb') as file:
        pickle.dump(keystroke_array, file)

# record_keystrokes()

# # ...or, in a non-blocking fashion:
# listener = keyboard.Listener(on_press=on_press, on_release=on_release)
# listener.start()