from mimetypes import init
import pickle

import pandas as pd

import analyse_keystrokes
import user_management
import capture_keystrokes
import monitor_keystrokes
import demo

from os import system

def clear_console():
    system('cls')


if __name__ == "__main__":
    dispatcher = {'1': user_management.manage_users, '2': monitor_keystrokes.mon_keystrokes, '3': demo.demo_project}
    
    while True:
        clear_console()
        print("Choose an option:\n1. Manage users\n2. Monitor keystrokes\n3. Demo")
        response = input("Choice: ")

        dispatcher[response]()