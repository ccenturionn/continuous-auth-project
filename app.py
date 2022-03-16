import capture_keystrokes
import pickle
import pandas as pd
import analyse_keystrokes
import os

reps = 3

def add_user(username):
    """
    Adds a user to the system
    """

    # Record the user typing a phrase multiple times
    for i in range(reps):
        keystroke_array = capture_keystrokes.record_keystrokes()

        # Store keystroke data to file
        with open("keystroke_datastore\\" + username + "_keystroke_data_" + str(i+1), 'wb') as file:
            pickle.dump(keystroke_array, file)
        file.close()

    frames = []

    # Take each keystroke data file and analyse the keystrokes
    for i in range(reps):

        file_name = "keystroke_datastore\\" + username + "_keystroke_data_" + str(i+1)

        # Load the keystroke array
        with open(file_name, 'rb') as file:
            keystroke_array = pickle.load(file)
        file.close()

        # Calculate the features and append to list
        frames.append(analyse_keystrokes.calc_features(keystroke_array))

        # Clean up unneeded files
        os.remove(file_name)
    
    # Concatenate all features into one dataframe
    keystroke_features = pd.concat(frames)

    # Store the features dataframe to file
    with open("keystroke_datastore\\" + username + "_keystroke_features", 'wb') as file:
            pickle.dump(keystroke_features, file)
    file.close()


add_user("test")