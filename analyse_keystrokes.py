import pickle
from pynput import keyboard
import pandas as pd

with open("keystroke_data", 'rb') as file:
    keystroke_array = pickle.load(file)

def calc_avg_dwell():
    avg_dwell_times = []

    unique_keys = list(keystroke_array['Key'].unique())

    for i in range(len(unique_keys)):
        unique_keys[i] = unique_keys[i]

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

    avg_dwell_times = pd.DataFrame(avg_dwell_times)
    avg_dwell_times.columns = ["Key", "Time"]
    print(avg_dwell_times)

def calc_avg_flight():
    flight_times = []

    i = 0
    while i < len(keystroke_array['Key']):
        
        if keystroke_array['PrevKey'].iloc[i] == None:
            i += 1
            continue

        cur_key = keystroke_array['Key'].iloc[i]
        prev_key = keystroke_array['PrevKey'].iloc[i]

        flight_time = keystroke_array['Time'].iloc[i] - keystroke_array['Time'].iloc[i-1]

        flight_times.append([cur_key, prev_key, flight_time])

        i+=2

    flight_times = pd.DataFrame(flight_times)
    flight_times.columns = ["Key", "PrevKey", "FlightTime"]
    print(flight_times)

calc_avg_flight()