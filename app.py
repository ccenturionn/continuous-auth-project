import capture_keystrokes
import pickle
import pandas as pd

capture_keystrokes.record_keystrokes()

with open("keystroke_data", 'rb') as file:
    keystroke_array = pickle.load(file)

print(keystroke_array)