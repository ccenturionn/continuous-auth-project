import matplotlib.pyplot as plt
import numpy as np
import pickle

import capture_keystrokes
import analyse_keystrokes
import classify

with open("user_data\\trained_classifier", 'rb') as file:
    ml_classifier = pickle.load(file)
file.close()

def demo_project():
    keystroke_array = capture_keystrokes.record_keystrokes()

    print(keystroke_array)

    pred_proba_list = []

    for i in range(len(keystroke_array)):
        keystroke_array_section = keystroke_array.iloc[0:i+3]
        keystroke_features = analyse_keystrokes.calc_features(keystroke_array_section)

        pred, pred_proba = classify.predict_class(ml_classifier, keystroke_features)

        pred_proba_list.append(pred_proba[0][0])

    print(pred_proba_list)


    plt.plot(pred_proba_list)
    plt.title("ML Classifier Probability")
    plt.xlabel("Number of Keystrokes")
    plt.ylabel("Prediction Probability")
    plt.show()
    """
    Record keystrokes
    For a range of single keystroke to all keystrokes
        Calculate features
        Predict against classifier
        store prediction confidence
    output to a plot
    """

demo_project()