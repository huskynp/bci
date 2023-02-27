import numpy as np
import tensorflow as tf
from keras.models import Sequential
from keras.layers.core import Dense
from keras.layers import LSTM
import time

tf.config.list_physical_devices('GPU')

rnn = Sequential()
rnn.add(LSTM(50, activation='relu', return_sequences=True, input_shape=(1, 1)))
rnn.add(LSTM(50, activation='relu'))
rnn.add(Dense(1, activation='sigmoid'))
rnn.compile(optimizer='adam', loss='mse', metrics=['accuracy'])
print(rnn.summary())

rnn.load_weights("./checkpoints/tuned")


def run_ai(epoch):
    start = time.time()
    test = np.array(epoch).reshape((len(epoch), 1, 1))
    output = rnn.predict(test, verbose=0)
    result = output > 0.04
    match = is_match(result, 0.13)
    return match


def is_match(data, HIGH_CONF_THRESHOLD):
    for conf in data:
        if conf >= HIGH_CONF_THRESHOLD:
            return True
    return False
