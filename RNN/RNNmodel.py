import pandas as pd
import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers

# just some preprocessing
raw_data = pd.read_csv(
    "EEG_Data.csv", 
    names=["AF3", "F7", "F3", "FC5", "T7", "P7", "O1", "O2", "P8", "T8", "FC6", "F4", "F8", "AF4", "target"]
 )

raw_data.head()
raw_data_features = raw_data.copy()
target = raw_data_features.pop("target")

tf.convert_to_tensor(raw_data_features)

normalize = layers.Normalization()
normalize.adapt(raw_data_features)


#model !!!!
input_shapes = (14980, 14)
inputs = keras.Input((input_shapes),)
hid1 = layers.LSTM(units=14, input_shape=(input_shapes))(inputs) #random hiddne layers
hid2 = layers.LSTM(units=10)(hid1)
output = layers.Dense(units=1)(hid2) #random output layers 
model = keras.Model(inputs, output)
model.summary()