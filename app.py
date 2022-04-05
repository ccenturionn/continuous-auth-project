from os import system

import demo
import monitor_keystrokes
import user_management


def clear_console():
    system('cls')


if __name__ == "__main__":
    dispatcher = {'1': user_management.manage_users, '2': monitor_keystrokes.mon_keystrokes, '3': demo.demo_project}
    
    while True:
        clear_console()
        print("Choose an option:\n1. Manage users\n2. Monitor keystrokes\n3. Demo")
        response = input("Choice: ")

        dispatcher[response]()
