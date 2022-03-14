from pynput import keyboard
import time
import analyse_keystrokes

start = 0
end = 0
keystroke_array = []
count = 0
prev_key = None



def monitor_on_press(key):
    global start, keystroke_array, count, prev_key 
    start = time.perf_counter_ns()
    start /= 1000000

    try:
        keystroke_array.append([key.char, start, "Pressed", prev_key])
    except AttributeError:
        keystroke_array.append([key, start, "Pressed", prev_key])

    count += 1

def monitor_on_release(key):
    global end, start, keystroke_array, count, prev_key
    end = time.perf_counter_ns()
    end /= 1000000
    # print(f'{key} released after {end - start} milliseconds')

    try:
        keystroke_array.append([key.char, end, "Released", prev_key])
    except AttributeError:
        keystroke_array.append([key, end, "Released", prev_key])

    prev_key = key


def monitor_keystrokes(duration):
    global keystroke_array, count
    keystroke_array = []

    listener = keyboard.Listener(on_press=monitor_on_press, on_release=monitor_on_release)
    listener.start()

    while True:
        if count >= duration:
            features = analyse_keystrokes.calc_features(keystroke_array)
            