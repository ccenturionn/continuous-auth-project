import pickle

test_string = "hello"

with open("test_file", 'wb') as file:
    pickle.dump(test_string, file)
file.close()

with open("test_file", 'rb') as file:
    file_output = pickle.load(file)
file.close()

print(file_output)

