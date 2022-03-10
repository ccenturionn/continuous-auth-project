from sklearn.utils import shuffle
import capture_keystrokes
import pickle
import pandas as pd
import analyse_keystrokes
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report

reps = 3

def add_user(username):
    for i in range(reps):
        keystroke_array = capture_keystrokes.record_keystrokes()

        # print(keystroke_array)

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

# add_user("test")

# with open("oliver_keystroke_features", 'rb') as file:
#             print(pickle.load(file))

# file.close()

with open("lauren_keystroke_features", 'rb') as file:
            lauren_keystroke_features = pickle.load(file)
file.close()

with open("oliver_keystroke_features", 'rb') as file:
            oliver_keystroke_features = pickle.load(file)
file.close()

lauren_keystroke_features['user'] = 0

oliver_keystroke_features['user'] = 1

keystroke_features = pd.concat([oliver_keystroke_features, lauren_keystroke_features])

keystroke_features = keystroke_features.reset_index(drop=True)

features_values = keystroke_features.loc[:, keystroke_features.columns != 'user']

x = features_values
y = keystroke_features['user']
index = keystroke_features.index

# tfidf_vectorizer = TfidfVectorizer(use_idf=True)
# x_vectors = tfidf_vectorizer.fit_transform(x)

# x_train, x_test, y_train, y_test, index_train, index_test = train_test_split(x, y, index, train_size=0.6, shuffle=True)
x_train, x_test, y_train, y_test, index_train, index_test = train_test_split(x, y, index, train_size=0.9, shuffle=True)

y_train = y_train.astype('int')
y_test = y_test.astype('int')

print("Training ML Classifier...")

logistic_reg = LogisticRegression(random_state=0)
logistic_reg.fit(x_train, y_train)

# lr_pred = logistic_reg.predict(x_test)

# print(classification_report(y_test, lr_pred))
# print(lr_pred)





keystroke_array = capture_keystrokes.record_keystrokes()

with open("test_keystroke_data", 'wb') as file:
    pickle.dump(keystroke_array, file)

file.close()


with open("test_keystroke_data", 'rb') as file:
            keystroke_array = pickle.load(file)

file.close()

test_keystroke_features = analyse_keystrokes.calc_features(keystroke_array)





# with open("lauren_keystroke_features", 'rb') as file:
#             oliver_keystroke_features = pickle.load(file)
# file.close()


lr_pred = logistic_reg.predict(test_keystroke_features.head(1))

if lr_pred[0] == 1:
    print("Current user: Oliver")
else:
    print("Current user: Lauren")