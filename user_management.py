import capture_keystrokes
import pickle
import pandas as pd
import analyse_keystrokes
import classify
import os

def add_user(username="none_provided", reps=0):
    """
    Adds a user to the system
    """

    if username == "none_provided":
        username = input("Enter a username to add: ")

    if reps == 0:
        reps = int(input("Enter the number of training repetitions the user should complete: "))

    # Load user_num dict from file
    with open("user_data\\user_num_store", 'rb') as file:
        user_num = pickle.load(file)
    file.close()

    # Get value for user number
    for i in range(50):
        print(i)
        if i not in user_num:
            num = i
            break

    # Set the user number
    user_num[num] = username

    frames = []

    # Record the user typing a phrase multiple times
    for i in range(reps):
        keystroke_array = capture_keystrokes.record_keystrokes()

        frames.append(analyse_keystrokes.calc_features(keystroke_array))

    keystroke_features = pd.concat(frames)

    keystroke_features['user'] = num

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

    if len(user_num) > 1:
        classify.train_classifier()

    print(f"Successfully added {user_num[num]} (user no. {num}) to the keystroke feature datastore.")


def remove_user(username="none_provided"):
    """
    Removes a user from the system
    """

    if username == "none_provided":
        username = input("Enter a username to remove: ")

    with open("user_data\\user_num_store", 'rb') as file:
        user_num = pickle.load(file)
    file.close()

    num = list(user_num.keys())[list(user_num.values()).index(username)]

    with open("user_data\\keystroke_features_store", 'rb') as file:
        master_keystroke_features = pickle.load(file)
    file.close()

    master_keystroke_features = master_keystroke_features[master_keystroke_features['user'] != num]

    # Store the features dataframe to file
    with open("user_data\\keystroke_features_store", 'wb') as file:
        pickle.dump(master_keystroke_features, file)
    file.close()

    print(f"Successfully removed {user_num[num]} (user no. {num}) from the keystroke feature datastore.")

    user_num.pop(num, None)

    with open("user_data\\user_num_store", 'wb') as file:
        pickle.dump(user_num, file)
    file.close()


def list_users():
    """
    List all users in the system
    """

    with open("user_data\\user_num_store", 'rb') as file:
        user_num = pickle.load(file)
    file.close()

    for key, value in user_num.items():
        print(f"Username: {value}\t\tUser No.: {key}")

def print_keystroke_datastore():
    """
    Output contents of keystroke features datastore
    """

    with open("user_data\\keystroke_features_store", 'rb') as file:
        keystroke_features = pickle.load(file)
    file.close()

    print(keystroke_features)

def manage_users():
    
    dispatcher = {'1': add_user, '2': remove_user, '3': list_users, '4': print_keystroke_datastore}
    
    while True:

        print("Choose an option:\n1. Add a user\n2. Remove a user\n3. List users\n4. Output the keystroke datastore")
        response = input("Choice: ")

        dispatcher[response]()


