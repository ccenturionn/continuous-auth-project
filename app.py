import capture_keystrokes
import pickle
import pandas as pd
import analyse_keystrokes
import os

reps = 3

def add_user(username):
    for i in range(reps):
        keystroke_array = capture_keystrokes.record_keystrokes()

        # print(keystroke_array)

        with open("keystroke_datastore\\" + username + "_keystroke_data_" + str(i+1), 'wb') as file:
            pickle.dump(keystroke_array, file)
        file.close()

    frames = []
    for i in range(reps):

        file_name = "keystroke_datastore\\" + username + "_keystroke_data_" + str(i+1)

        with open(file_name, 'rb') as file:
            keystroke_array = pickle.load(file)
        file.close()

        frames.append(analyse_keystrokes.calc_features(keystroke_array))

        os.remove(file_name)
    
    keystroke_features = pd.concat(frames)

    with open("keystroke_datastore\\" + username + "_keystroke_features", 'wb') as file:
            pickle.dump(keystroke_features, file)
    file.close()


add_user("test")