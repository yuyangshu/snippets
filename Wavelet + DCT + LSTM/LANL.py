import os
import collections
import csv
import math
import random

import numpy
import scipy.fftpack
import scipy.signal
import pywt
import tensorflow
import matplotlib.pyplot


# hyper parameters
batch_size = 25
sequence_length = 15000
transformed_sequence_length = 3000
break_threshold = 0.005
state_size = 108
learning_rate = 0.01


# extract data
with open("sample.csv", encoding="utf-8-sig", errors="ignore") as csvfile:
    reader = csv.reader(csvfile, delimiter=",")
    raw_data = [[float(entry[0]), float(entry[1])] for entry in list(reader)[1:]]

data = []
for i in range(0, len(raw_data), 1000):
    # sanity check
    if i + sequence_length >= len(raw_data):
        break

    if raw_data[i][1] - raw_data[i + sequence_length][1] > break_threshold:
        continue
    # defaultdict(<class 'int'>, {3202983: 264, 4198477: 113, 4298478: 219, 3102983: 16, 4198478: 190, 3202984: 56, 4298477: 162, 3102984: 14})

    data_slice = [entry[0] for entry in raw_data[i : i + sequence_length]]
    expected_output = raw_data[i + sequence_length][1]

    # apply wavelet and dct
    cA, cD = pywt.dwt(data_slice, 'db2')
    dct_result = scipy.fftpack.dct(cA, norm="ortho")[:transformed_sequence_length]

    data.append(list(dct_result) + [expected_output])

numpy.random.shuffle(data)
border = math.floor(len(data) * 0.8)
X, Y = [entry[:-1] for entry in data[:border]], [entry[-1] for entry in data[:border]]


# define model
input_data = tensorflow.placeholder(shape=[batch_size, transformed_sequence_length, 1], dtype=tensorflow.float32)
labels = tensorflow.placeholder(shape=[batch_size, 1], dtype=tensorflow.float32)
state = tensorflow.zeros(shape=[batch_size, state_size], dtype=tensorflow.float32)

lstm_cell = tensorflow.contrib.cudnn_rnn.CudnnCompatibleLSTMCell(num_units=state_size)
rnn_output, state = tensorflow.nn.dynamic_rnn(cell=lstm_cell, inputs=input_data, dtype=tensorflow.float32)

rnn_output = tensorflow.transpose(rnn_output, [1, 0, 2])
rnn_output = tensorflow.gather(rnn_output, int(rnn_output.get_shape()[0]) - 1)

w = tensorflow.Variable(tensorflow.random.truncated_normal(shape=[state_size, 1], stddev=0.1), dtype=tensorflow.float32)
b = tensorflow.Variable(tensorflow.constant(0.1, shape=[batch_size, 1], dtype=tensorflow.float32))
result = tensorflow.matmul(rnn_output, w) + b

loss = tensorflow.math.reduce_mean(tensorflow.math.abs(result - labels))
optimizer = tensorflow.train.AdamOptimizer(learning_rate).minimize(loss)


# train model
tensorflow.summary.scalar("loss", loss)
tensorflow.summary.scalar("validation_loss", loss)
summary_op = tensorflow.summary.merge_all()

sess = tensorflow.InteractiveSession()
sess.run(tensorflow.global_variables_initializer())

logdir = "tensorboard/"
writer = tensorflow.summary.FileWriter(logdir, sess.graph)
all_saver = tensorflow.train.Saver()

for i in range(0, round(len(data) * 10 / batch_size)):
    start_index = random.randint(0, border - batch_size)
    end_index = min(start_index + batch_size, len(data) - 1)
    batch_data, batch_labels = numpy.reshape(X[start_index : end_index], (-1, transformed_sequence_length, 1)), numpy.array(Y[start_index : end_index]).reshape(-1, 1)
    sess.run(optimizer, {input_data: batch_data, labels: batch_labels})
    # test every 100 run
    if (i % 100 == 0):
        # training loss
        training_loss, summary = sess.run([loss, summary_op], {input_data: batch_data, labels: batch_labels})
        writer.add_summary(summary, i)
        print(f"Iteration {i}:\ntraining loss: {training_loss}")

        # validation loss
        validation_batch = random.sample(data[border:], batch_size)
        validation_data, validation_labels = numpy.reshape([entry[:-1] for entry in validation_batch], (-1, transformed_sequence_length, 1)), numpy.array([entry[-1] for entry in validation_batch]).reshape(-1, 1)
        validation_loss, summary = sess.run([loss, summary_op], {input_data: validation_data, labels: validation_labels})
        writer.add_summary(summary, i)
        print(f"validation loss: {validation_loss}")

        if (i % 10000 == 0 and i != 0):
            all_saver.save(sess, "trained_model.ckpt", global_step=i)


# predict
with open("predictions.csv", 'w') as f:
    for name in os.listdir("test"):
        with open("test/" + name, 'r') as f:
            data = [float(entry) for entry in f.read().split()[1:]]
        f.write(name + ',' + str(sess.run(result, {input_data: data})) + '\n')

# keras version, NOT WORKING :/
# lstm = tensorflow.keras.layers.CuDNNLSTM(units=108, dtype=tensorflow.float32)(num_units=108, dtype=tensorflow.float32)
# dense = tensorflow.layers.Dense(units=32, activation=tensorflow.nn.relu, use_bias=True)
# result = tensorflow.layers.Dense(units=1, activation=tensorflow.nn.relu, use_bias=True)
# model = tensorflow.keras.Sequential([lstm, dense, result])
# model.compile(optimizer=tensorflow.train.AdamOptimizer(), loss=numpy.linalg.norm)