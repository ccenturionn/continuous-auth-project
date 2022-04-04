from mimetypes import init
import pickle

import pandas as pd

import analyse_keystrokes
import user_management
import capture_keystrokes
import monitor_keystrokes





if __name__ == "__main__":

    monitor_keystrokes.mon_keystrokes()
    # user_management.manage_users()