import pandas as pd
import numpy as np
np.set_printoptions(precision=3, suppress=True)
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers

# just some preprocessing
def preProcess():
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


#model time

def RNN_Model():
    