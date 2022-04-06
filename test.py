import multiprocessing
import pickle
import time
from os.path import exists

import pandas as pd
from pynput import keyboard
from win10toast import ToastNotifier

import analyse_keystrokes
import classify

# Load the trained classifier from file
with open("user_data\\trained_classifier", 'rb') as file:
    ml_classifier = pickle.load(file)
file.close()

toaster = ToastNotifier()

# Load the user_num dict from file
with open("user_data\\user_num_store", 'rb') as file:
    user_num = pickle.load(file)
file.close()

def start_ml(keystroke_array):
    ml_process = multiprocessing.Process(target=run_ml, args=[keystroke_array])
    ml_process.start()

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

    # update_confidence(pred_proba)

    # Output the predicted class
    print(f"Prediction: {pred}\t\tProbability: {pred_proba}")

    # Windows notification with detected user
    toaster.show_toast("User Detected", f"{user_num[pred[0]]}")