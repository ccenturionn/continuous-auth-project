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

if not exists("user_data\\trained_classifier"):
    user_num = {}
    with open("user_data\\trained_classifier", 'wb') as file:
        pickle.dump(user_num, file)
    file.close()

with open("user_data\\trained_classifier", 'rb') as file:
    ml_classifier = pickle.load(file)
file.close()

with open("user_data\\user_num_store", 'rb') as file:
    user_num = pickle.load(file)
file.close()

def run_ml(keystroke_array):
    print("ML Process Started")
    keystroke_df = pd.DataFrame(keystroke_array)
    keystroke_df.columns = ["Key", "Time", "Action", "PrevKey"]

    pred, pred_proba = classify.predict_class(ml_classifier, analyse_keystrokes.calc_features(keystroke_df))

    print(f"Prediction: {pred}\t\tProbability: {pred_proba}")
    toaster.show_toast("User Detected", f"{user_num[pred[0]]}")


def monitor_on_press(key):
    global start, keystroke_array, count, prev_key 
    start = time.perf_counter_ns()
    start /= 1000000

    try:
        keystroke_array.append([key.char, start, "Pressed", prev_key])
    except AttributeError:
        keystroke_array.append([key, start, "Pressed", prev_key])

    count += 1

def monitor_on_release(key):
    global end, start, keystroke_array, count, prev_key
    end = time.perf_counter_ns()
    end /= 1000000
    # print(f'{key} released after {end - start} milliseconds')

    try:
        keystroke_array.append([key.char, end, "Released", prev_key])
    except AttributeError:
        keystroke_array.append([key, end, "Released", prev_key])

    prev_key = key

    print(key)

    if count > 40:
        count = 0
        ml_process = multiprocessing.Process(target=run_ml, args=[keystroke_array])
        ml_process.start()
        keystroke_array = []


def mon_keystrokes():

    listener = keyboard.Listener(on_press=monitor_on_press, on_release=monitor_on_release)
    listener.start()

    input()
   