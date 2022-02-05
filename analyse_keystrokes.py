import pickle
from pynput import keyboard
import pandas as pd

with open("keystroke_data", 'rb') as file:
    keystroke_array = pickle.load(file)

avg_dwell_times = []

unique_keys = list(keystroke_array['Key'].unique())

for i in range(len(unique_keys)):
    unique_keys[i] = unique_keys[i]

# for i in range(len(unique_keys)):
#     if unique_keys[i] == keyboard.Key.enter:
#         unique_keys = "Key.enter"
#     if unique_keys[i] == keyboard.Key.space:
#         unique_keys = "Key.space"


print(unique_keys)

for key in unique_keys:
    keystrokes_press = list(keystroke_array[(keystroke_array['Key'] == key) & (keystroke_array['Action'] == "Pressed")]['Time'])
    keystrokes_release = list(keystroke_array[(keystroke_array['Key'] == key) & (keystroke_array['Action'] == "Released")]['Time'])

    total_dwell = 0
    for i in range(len(keystrokes_press)):
        total_dwell += keystrokes_release[i] - keystrokes_press[i]

    try:
        avg_dwell = total_dwell / len(keystrokes_press)
    except:
        continue

    avg_dwell_times.append([key, avg_dwell])

print(pd.DataFrame(avg_dwell_times))