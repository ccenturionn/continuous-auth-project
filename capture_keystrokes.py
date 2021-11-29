from pynput import keyboard
import numpy as np
import pandas as pd
import time

start = 0
end = 0
keystroke_array = []
count = 0

def on_press(key):
    global start 
    start = time.perf_counter_ns()
    start /= 1000000
    try:
        print(f'alphanumeric key {key.char} pressed')
    except AttributeError:
        print(f'special key {key} pressed')

def on_release(key):
    global end, start, keystroke_array, count
    end = time.perf_counter_ns()
    end /= 1000000
    print(f'{key} released after {end - start} milliseconds')

    try:
        keystroke_array.append([key.char, start, end])
    except AttributeError:
        keystroke_array.append([key, start, end])

    print(keystroke_array)
    if key == keyboard.Key.esc:
        # Stop listener
        return False

# Collect events until released
with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()

keystroke_array2 = pd.DataFrame(keystroke_array)
keystroke_array2.columns = ["Key", "Pressed", "Released"]
print(keystroke_array2)

# ...or, in a non-blocking fashion:
# listener = keyboard.Listener(on_press=on_press, on_release=on_release)
# listener.start()