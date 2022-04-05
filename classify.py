import pickle

from sklearn.linear_model import LogisticRegression


def train_classifier():
    """
    Trains the machine learning classifier using keystroke_features_store and stores the trained classifier as trained_classifier
    """

    # Load the keystroke features
    with open("user_data\\keystroke_features_store", 'rb') as file:
        keystroke_features = pickle.load(file)
    file.close()

    # Separate the values from the class label
    features = keystroke_features.loc[:, keystroke_features.columns != 'user']

    x_train = features
    y_train = keystroke_features['user']
    index_train = keystroke_features.index

    y_train = y_train.astype('int')

    print("Training ML Classifier...")

    # Init the ML classifier and fit the training data
    logistic_reg = LogisticRegression(random_state=0, max_iter=4000)
    logistic_reg.fit(x_train, y_train)

    # Store the trained ML classifier
    with open("user_data\\trained_classifier", 'wb') as file:
        pickle.dump(logistic_reg, file)
    file.close()


def predict_class(ml_classifier, keystroke_features):
    """
    Predicts the class of a set of keystroke features and returns the predicted class and probabilities
    """

    # Predict the class and probability of the keystroke features
    pred = ml_classifier.predict(keystroke_features)
    pred_proba = ml_classifier.predict_proba(keystroke_features)

    print(ml_classifier.classes_)

    return(pred, pred_proba)


# with open("user_data\\trained_classifier", 'rb') as file:
#     ml_classifier = pickle.load(file)
# file.close()

# pred, pred_proba = predict_class(ml_classifier, analyse_keystrokes.calc_features(capture_keystrokes.record_keystrokes()))

# print(f"Prediction: {pred}\t\tProbability: {pred_proba}")
