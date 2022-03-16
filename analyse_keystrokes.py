import pickle
from pynput import keyboard
import pandas as pd
import itertools

# Define list of keys that analysed
key_set = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', keyboard.Key.enter, keyboard.Key.space, keyboard.Key.esc]

# Define a list of all combinations of keys (including same-key combination)
key_set_combos = list(itertools.permutations(key_set, 2))
for key in key_set:
    key_set_combos.append((key, key))


def calc_dwell(keystroke_array):
    """
    Calculates the dwell time attributes for the keystroke data
    """

    dwell_feats = []

    # Calculate dwell features for each key in the key set
    for key in key_set:
        keystrokes_press = list(keystroke_array[(keystroke_array['Key'] == key) & (keystroke_array['Action'] == "Pressed")]['Time'])
        keystrokes_release = list(keystroke_array[(keystroke_array['Key'] == key) & (keystroke_array['Action'] == "Released")]['Time'])

        dwell_times = []

        # Calculate dwell time for each press and release pair
        for i in range(len(keystrokes_press)):
            dwell_times.append(keystrokes_release[i] - keystrokes_press[i])

        # If a key has no keypresses, set it's values to 0 and go to next key
        if len(dwell_times) <= 0:
            dwell_feats.append([key, 0, 0, 0])
            continue
        
        # Calculate min, max and avg of dwell times
        min_dwell = min(dwell_times)
        max_dwell = max(dwell_times)
        avg_dwell = sum(dwell_times) / len(dwell_times)

        dwell_feats.append([key, min_dwell, max_dwell, avg_dwell])
    
    return dwell_feats


def calc_flight(keystroke_array):
    """
    Calculates the flight time attributes for the keystroke data
    """

    flight_times = []

    # Separate keystroke presses and releases
    keystrokes_press = keystroke_array[keystroke_array['Action'] == "Pressed"]
    keystrokes_release = keystroke_array[keystroke_array['Action'] == "Released"]

    # Calculate the flight time between keystrokes and append to list
    for i in range(len(keystrokes_press)):
        cur_key = keystrokes_press['Key'].iloc[i]
        prev_key = keystrokes_release['Key'].iloc[i]

        # Calculate flight time
        flight_time = keystrokes_press['Time'].iloc[i] - keystrokes_release['Time'].iloc[i]

        flight_times.append([cur_key, prev_key, flight_time])

    # Convert list to dataframe
    flight_times = pd.DataFrame(flight_times)
    flight_times.columns = ["Key", "PrevKey", "FlightTime"]

    avg_flight_times = []

    # Calculate average flight time for each key combination and append to list
    for key_combo in key_set_combos:

        key_combo_flights = flight_times[(flight_times['Key'] == key_combo[0]) & (flight_times['PrevKey'] == key_combo[1])]
        
        # If there is no flight attribute for a key set average time to 0
        if len(key_combo_flights['Key']) == 0:
            avg_flight_times.append([key_combo[0], key_combo[1], 0])
            continue

        # Calculate average flight time and append to list
        avg_flight_time = sum(key_combo_flights['FlightTime']) / len(key_combo_flights['FlightTime'])
        avg_flight_times.append([key_combo[0], key_combo[1], avg_flight_time])

    return avg_flight_times
        
        
def calc_features(keystroke_array):
    """
    Calculates features from raw keystroke data
    """

    # Calculate dwell and flight features
    dwell_features = calc_dwell(keystroke_array)
    flight_features = calc_flight(keystroke_array)

    # Define list of column names for dwell time features
    dwell_col_names = []
    for dwell in dwell_features:
        dwell_col_names.append(str(dwell[0]) + "_min_dwell")
        dwell_col_names.append(str(dwell[0]) + "_max_dwell")
        dwell_col_names.append(str(dwell[0]) + "_avg_dwell")

    # Define list of values for dwell time features
    dwell_values = []
    for dwell in dwell_features:
        dwell_values.append(dwell[1])
        dwell_values.append(dwell[2])
        dwell_values.append(dwell[3])

    # Define list of column names for flight time features
    flight_col_names = []
    for flight in flight_features:
        flight_col_names.append(str(flight[0]) + "_" + str(flight[1]))

    # Define line of values for flight time features
    flight_values = []
    for flight in flight_features:
        flight_values.append(flight[2])

    # Append flight column names and values to dwell column names and value
    dwell_col_names.extend(flight_col_names)
    dwell_values.extend(flight_values)

    col_names = dwell_col_names
    values = dwell_values

    # Create dataframe using values list and column names list
    features = pd.DataFrame([values], columns=col_names)

    return features

def get_empty_df(keystroke_array):
    """
    Generates empy dataframe with keystroke feature headings
    """

    # Calculate dwell and flight features
    dwell_features = calc_dwell(keystroke_array)
    flight_features = calc_flight(keystroke_array)

    # Define list of column names for dwell time features
    dwell_col_names = []
    for dwell in dwell_features:
        dwell_col_names.append(str(dwell[0]) + "_min_dwell")
        dwell_col_names.append(str(dwell[0]) + "_max_dwell")
        dwell_col_names.append(str(dwell[0]) + "_avg_dwell")

    # Define list of column names for flight time features
    flight_col_names = []
    for flight in flight_features:
        flight_col_names.append(str(flight[0]) + "_" + str(flight[1]))

    # Append flight column names and values to dwell column names and value
    dwell_col_names.extend(flight_col_names)

    temp_df = pd.DataFrame(columns=dwell_col_names)

    with open("user_data\\keystroke_features_store", 'wb') as file:
        pickle.dump(temp_df, file)
    file.close()