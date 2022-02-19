import capture_keystrokes
import pickle
import pandas as pd
import analyse_keystrokes

reps = 3

def add_user(username):
    for i in range(reps):
        keystroke_array = capture_keystrokes.record_keystrokes()

        print(keystroke_array)

        with open(username + "_keystroke_data_" + str(i+1), 'wb') as file:
            pickle.dump(keystroke_array, file)

        file.close()

    frames = []
    for i in range(reps):

        with open(username + "_keystroke_data_" + str(i+1), 'rb') as file:
            keystroke_array = pickle.load(file)

        file.close()

        frames.append(analyse_keystrokes.calc_features(keystroke_array))
    
    keystroke_features = pd.concat(frames)

    with open(username + "_keystroke_features", 'wb') as file:
            pickle.dump(keystroke_features, file)

    file.close()

add_user("lauren")

# with open("oliver_keystroke_features", 'rb') as file:
#             print(pickle.load(file))

# file.close()