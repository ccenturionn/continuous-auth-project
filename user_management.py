import capture_keystrokes
import pickle
import pandas as pd
import analyse_keystrokes
import os

def add_user(username, reps):
    """
    Adds a user to the system
    """

    # Load user_num dict from file
    with open("user_data\\user_num_store", 'rb') as file:
        user_num = pickle.load(file)
    file.close()

    # Set the user number
    user_num[username] = len(user_num)

    frames = []

    # Record the user typing a phrase multiple times
    for i in range(reps):
        keystroke_array = capture_keystrokes.record_keystrokes()

        frames.append(analyse_keystrokes.calc_features(keystroke_array))

    keystroke_features = pd.concat(frames)

    keystroke_features['user'] = int(user_num[username])

    with open("user_data\\keystroke_features_store", 'rb') as file:
        master_keystroke_features = pickle.load(file)
    file.close()

    master_keystroke_features = pd.concat([master_keystroke_features, keystroke_features])

    # Store the features dataframe to file
    with open("user_data\\keystroke_features_store", 'wb') as file:
        pickle.dump(master_keystroke_features, file)
    file.close()

    # Store user_num dict to file
    with open("user_data\\user_num_store", 'wb') as file:
        pickle.dump(user_num, file)
    file.close()

    print(f"Successfully added {username} (user no. {user_num[username]}) to the keystroke feature datastore.")


def remove_user(username):
    """
    Removes a user from the system
    """

    with open("user_data\\user_num_store", 'rb') as file:
        user_num = pickle.load(file)
    file.close()

    with open("user_data\\keystroke_features_store", 'rb') as file:
        master_keystroke_features = pickle.load(file)
    file.close()

    master_keystroke_features = master_keystroke_features[master_keystroke_features['user'] != user_num[username]]

    # Store the features dataframe to file
    with open("user_data\\keystroke_features_store", 'wb') as file:
        pickle.dump(master_keystroke_features, file)
    file.close()

    user_num.pop(username, None)

    with open("user_data\\user_num_store", 'wb') as file:
        pickle.dump(user_num, file)
    file.close()

    print(f"Successfully removed {username} (user no. {user_num[username]}) from the keystroke feature datastore.")


def list_users():
    """
    List all users in the system
    """

    with open("user_data\\user_num_store", 'rb') as file:
        user_num = pickle.load(file)
    file.close()

    for key, value in user_num.items():
        print(f"Username: {key}\t\tUser No.: {value}")

def print_keystroke_datastore():
    """
    Output contents of keystroke features datastore
    """

    with open("user_data\\keystroke_features_store", 'rb') as file:
        keystroke_features = pickle.load(file)
    file.close()

    print(keystroke_features)


