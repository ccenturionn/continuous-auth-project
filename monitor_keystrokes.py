import multiprocessing
import pickle
import time
from os.path import exists

import pandas as pd
import numpy as np
from pynput import keyboard
from win10toast import ToastNotifier

import analyse_keystrokes
import classify

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

start = 0
end = 0
keystroke_array = []
count = 0
prev_key = None
toaster = ToastNotifier()
num_keystrokes = 40

class Confidence:
    def __init__(self, user_num):
        self.current_user = -1
        self.user_confidence = {}

        for i in range(len(user_num)):
            self.user_confidence[i] = [0.5, 0.5, 0.5, 0.5, 0.5]


def update_confidence(pred_proba):
    with open("user_data\\confidence_data", 'rb') as file:
        cd = pickle.load(file)
    file.close()

    pred_proba_len = len(pred_proba[0])

    for conf in cd.user_confidence:
        cd.user_confidence[conf].pop(0)

    for i in range(pred_proba_len):
        cd.user_confidence[i].append(pred_proba[0][i])

    confidence_avg = []

    print(cd.user_confidence)
    for i in range(pred_proba_len):
        confidence_avg.append(np.mean(cd.user_confidence[i]))
        print(np.mean(cd.user_confidence[i]))

    current_user = np.argmax(confidence_avg)

    if current_user != cd.current_user:
        cd.current_user = current_user

        # Windows notification with detected user
        toaster.show_toast("User Detected", f"{user_num[current_user]}")

    with open("user_data\\confidence_data", 'wb') as file:
        pickle.dump(cd, file)
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

    update_confidence(pred_proba)

    # Output the predicted class
    print(f"Prediction: {pred}\t\tProbability: {pred_proba}")



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

    confidence_data = Confidence(user_num)

    with open("user_data\\confidence_data", 'wb') as file:
        pickle.dump(confidence_data, file)
    file.close()

    listener = keyboard.Listener(on_press=monitor_on_press, on_release=monitor_on_release)
    listener.start()

    input()
   