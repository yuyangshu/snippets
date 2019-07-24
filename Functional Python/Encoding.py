def read_data(file_name, encoding_function, expected_length):
    with open(file_name, 'r') as f:
        return numpy.array([encoding_function(row) for row in f.read().split('\n') if len(row) == expected_length])

def encode_string(s):
    return [one_hot_encode_character(c) for c in s]

def one_hot_encode_character(c):
    base = [0] * 26
    index = ord(c) - ord('a')
    if index >= 0 and index <= 25:
        base[index] = 1
    return base


input_dimension = 9
label_dimension = 1

training_input = read_data("training_input.txt", encode_string, input_dimension)
training_label = read_data("training_label.txt", one_hot_encode_character, label_dimension)