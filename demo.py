import pickle

import matplotlib.pyplot as plt

import analyse_keystrokes
import capture_keystrokes
import classify


def demo_project():
    with open("user_data\\trained_classifier", 'rb') as file:
        ml_classifier = pickle.load(file)
    file.close()

    with open("user_data\\user_num_store", 'rb') as file:
        user_num = pickle.load(file)
    file.close()

    keystroke_array = capture_keystrokes.record_keystrokes()

    keystroke_array = keystroke_array.iloc[1:-1]

    keystrokes_pressed = keystroke_array[keystroke_array['Action'] == "Pressed"]
    keystrokes_pressed = keystrokes_pressed['Key'].values.tolist()

    x = range(0, len(keystrokes_pressed), 1)

    pred_proba_list = [ [] for _ in range(len(user_num))]

    for i in range(0, len(keystroke_array), 2):

        keystroke_array_section = keystroke_array.iloc[0:i+2]

        keystroke_features = analyse_keystrokes.calc_features(keystroke_array_section)

        pred, pred_proba = classify.predict_class(ml_classifier, keystroke_features)

        for i in range(len(pred_proba[0])):
            pred_proba_list[i].append(pred_proba[0][i])

    for i in pred_proba_list:
        plt.plot(i)
    plt.title("ML Classifier Probability")
    plt.xlabel("Keystrokes")
    plt.ylabel("Prediction Probability")
    plt.xticks(x, keystrokes_pressed, rotation=90)
    plt.legend(list(user_num.values()))
    plt.show()

    input("Press enter to continue...")
