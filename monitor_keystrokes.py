import multiprocessing
import pickle
import time
from os.path import exists

import pandas as pd
from pynput import keyboard
from win10toast import ToastNotifier

import analyse_keystrokes
import classify

start = 0
end = 0
keystroke_array = []
count = 0
prev_key = None
toaster = ToastNotifier()
num_keystrokes = 40

# If the trained_classifier file doesn't exist, create placeholder file
if not exists("user_data\\trained_classifier"):
    trained_classifier = 0
    with open("user_data\\trained_classifier", 'wb') as file:
        pickle.dump(trained_classifier, file)
    file.close()

# Load the trained classifier from file
with open("user_data\\trained_classifier", 'rb') as file:
    ml_classifier = pickle.load(file)
file.close()

# Load the user_num dict from file
with open("user_data\\user_num_store", 'rb') as file:
    user_num = pickle.load(file)
file.close()


def run_ml(keystroke_array):
    """
    Get keystroke features from keystroke array and predict class against ML classifier
    """
    print("ML Process Started")

    # Convert array to dataframe
    keystroke_df = pd.DataFrame(keystroke_array)
    keystroke_df.columns = ["Key", "Time", "Action", "PrevKey"]

    # Calculate features and predict against ML classifier
    pred, pred_proba = classify.predict_class(ml_classifier, analyse_keystrokes.calc_features(keystroke_df))

    # Output the predicted class
    print(f"Prediction: {pred}\t\tProbability: {pred_proba}")

    # Windows notification with detected user
    toaster.show_toast("User Detected", f"{user_num[pred[0]]}")


def monitor_on_press(key):
    """
    On key press, append keystroke information to keystroke array
    """
    global start, keystroke_array, count, prev_key

    # Get time that key is pressed and convert to ms
    start = time.perf_counter_ns()
    start /= 1000000

    # Append keystroke information to keystroke array
    try:
        keystroke_array.append([key.char, start, "Pressed", prev_key])
    except AttributeError:
        keystroke_array.append([key, start, "Pressed", prev_key])

    # Increment keypress count
    count += 1

def monitor_on_release(key):
    """
    On key release, append keystroke information to keystroke array
    """
    global end, start, keystroke_array, count, prev_key
    
    # Get time that key is released and convert to ms
    end = time.perf_counter_ns()
    end /= 1000000

    # Append keystroke information to keystroke array
    try:
        keystroke_array.append([key.char, end, "Released", prev_key])
    except AttributeError:
        keystroke_array.append([key, end, "Released", prev_key])

    prev_key = key

    # print(key)

    # When number of keystrokes reaches value of num_keystrokes start ML classification in another process
    if count > num_keystrokes:
        count = 0
        ml_process = multiprocessing.Process(target=run_ml, args=[keystroke_array])
        ml_process.start()
        keystroke_array = []


def mon_keystrokes():
    """
    Begin monitoring keystrokes
    """

    listener = keyboard.Listener(on_press=monitor_on_press, on_release=monitor_on_release)
    listener.start()

    input()
   