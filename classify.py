import pickle

import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split
from sklearn.utils import shuffle

import analyse_keystrokes
import capture_keystrokes

with open("lauren_keystroke_features", 'rb') as file:
    lauren_keystroke_features = pickle.load(file)
file.close()

with open("oliver_keystroke_features", 'rb') as file:
    oliver_keystroke_features = pickle.load(file)
file.close()

with open("test_keystroke_features", "rb") as file:
    test_keystroke_features = pickle.load(file)
file.close()

lauren_keystroke_features['user'] = 0

oliver_keystroke_features['user'] = 1

test_keystroke_features['user'] = 2

keystroke_features = pd.concat([oliver_keystroke_features, lauren_keystroke_features, test_keystroke_features])

keystroke_features = keystroke_features.reset_index(drop=True)

features_values = keystroke_features.loc[:, keystroke_features.columns != 'user']

x = features_values
y = keystroke_features['user']
index = keystroke_features.index


# x_train, x_test, y_train, y_test, index_train, index_test = train_test_split(x, y, index, train_size=0.6, shuffle=True)
x_train, x_test, y_train, y_test, index_train, index_test = train_test_split(x, y, index, train_size=0.9, shuffle=True)

y_train = y_train.astype('int')
y_test = y_test.astype('int')

print("Training ML Classifier...")

logistic_reg = LogisticRegression(random_state=0, max_iter=4000)
logistic_reg.fit(x_train, y_train)


keystroke_array = capture_keystrokes.record_keystrokes()

with open("test_keystroke_data", 'wb') as file:
    pickle.dump(keystroke_array, file)

file.close()


with open("test_keystroke_data", 'rb') as file:
            keystroke_array = pickle.load(file)

file.close()

test_keystroke_features = analyse_keystrokes.calc_features(keystroke_array)




lr_pred = logistic_reg.predict(test_keystroke_features.head(1))

print(lr_pred)

# if lr_pred[0] == 1:
#     print("Current user: Oliver")
# else:
#     print("Current user: Lauren")
