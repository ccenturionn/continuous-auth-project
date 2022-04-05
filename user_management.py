import pickle
from os import system
from os.path import exists

import pandas as pd

import analyse_keystrokes
import capture_keystrokes
import classify

# Check if user_num_store file exists if not create empty dict
if exists("user_data\\user_num_store") == False:
    user_num = {}
    with open("user_data\\user_num_store", 'wb') as file:
        pickle.dump(user_num, file)
    file.close()

# Check if keystroke_features_store file exists if not create empty datafram
if exists("user_data\\keystroke_features_store") == False:
    print("Please type random letters to initialise keystroke dataframe.")
    analyse_keystrokes.create_empty_df(capture_keystrokes.record_keystrokes())

def clear_console():
    system('cls')

def add_user(username="none_provided", reps=0):
    """
    Adds a user to the system
    """

    # Check if username is provided if not, prompt user to enter
    if username == "none_provided":
        username = input("Enter a username to add: ")

    # Prompt for number of training repetitions
    if reps == 0:
        reps = int(input("Enter the number of training repetitions the user should complete: "))

    # Load user_num dict from file
    with open("user_data\\user_num_store", 'rb') as file:
        user_num = pickle.load(file)
    file.close()

    # Get value for user number
    for i in range(50):
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

    # Load master_keystroke_features from file
    with open("user_data\\keystroke_features_store", 'rb') as file:
        master_keystroke_features = pickle.load(file)
    file.close()

    # Concat the new keystroke features to master_keystroke_features
    master_keystroke_features = pd.concat([master_keystroke_features, keystroke_features])

    # Store the features dataframe to file
    with open("user_data\\keystroke_features_store", 'wb') as file:
        pickle.dump(master_keystroke_features, file)
    file.close()

    # Store user_num dict to file
    with open("user_data\\user_num_store", 'wb') as file:
        pickle.dump(user_num, file)
    file.close()

    # Check if there is more that one user before training classifier
    if len(user_num) > 1:
        classify.train_classifier()

    print(f"Successfully added {user_num[num]} (user no. {num}) to the keystroke feature datastore.")

    input("Press enter to continue...")


def remove_user(username="none_provided"):
    """
    Removes a user from the system
    """

    # Check if username is provided, if not prompt user to enter username
    if username == "none_provided":
        username = input("Enter a username to remove: ")

    # Load user_num_store from file
    with open("user_data\\user_num_store", 'rb') as file:
        user_num = pickle.load(file)
    file.close()

    # Get user number for the username provided
    num = list(user_num.keys())[list(user_num.values()).index(username)]

    with open("user_data\\keystroke_features_store", 'rb') as file:
        master_keystroke_features = pickle.load(file)
    file.close()

    # Remove user from master_keystroke_features
    master_keystroke_features = master_keystroke_features[master_keystroke_features['user'] != num]

    # Store the features dataframe to file
    with open("user_data\\keystroke_features_store", 'wb') as file:
        pickle.dump(master_keystroke_features, file)
    file.close()

    print(f"Successfully removed {user_num[num]} (user no. {num}) from the keystroke feature datastore.")

    # Remove user from user_num dict
    user_num.pop(num, None)

    # Write user_num_store to file
    with open("user_data\\user_num_store", 'wb') as file:
        pickle.dump(user_num, file)
    file.close()

    input("Press enter to continue...")


def list_users():
    """
    List all users in the system
    """

    with open("user_data\\user_num_store", 'rb') as file:
        user_num = pickle.load(file)
    file.close()

    for key, value in user_num.items():
        print(f"Username: {value}\t\tUser No.: {key}")
        
    input("Press enter to continue...")

def print_keystroke_datastore():
    """
    Output contents of keystroke features datastore
    """

    with open("user_data\\keystroke_features_store", 'rb') as file:
        keystroke_features = pickle.load(file)
    file.close()

    print(keystroke_features)
    input("Press enter to continue...")

def manage_users():
    """
    Main menu for managing users
    """
    
    dispatcher = {'1': add_user, '2': remove_user, '3': list_users, '4': print_keystroke_datastore}
    
    while True:
        clear_console()
        print("Choose an option:\n1. Add a user\n2. Remove a user\n3. List users\n4. Output the keystroke datastore\n5. Return to main menu")
        response = input("Choice: ")

        if response == '5':
            break

        dispatcher[response]()


