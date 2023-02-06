import pandas as pd
import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
import os

# just some preprocessing
raw_data = pd.read_csv(
    "EEG_Data.csv", 
    names=["AF3", "F7", "F3", "FC5", "T7", "P7", "O1", "O2", "P8", "T8", "FC6", "F4", "F8", "AF4", "target"]
 )

checkpoint_path = "checkpoints/eeg.ckpt"
checkpoint_dir = os.path.dirname(checkpoint_path)

# Create a callback that saves the model's weights
cp_callback = tf.keras.callbacks.ModelCheckpoint(filepath=checkpoint_path,
                                                 save_weights_only=True,
                                                 verbose=1)


#raw_data.head()
raw_data_features = raw_data.copy()
target = raw_data_features.pop("target")
target_shape = (14980, 1)

tf.convert_to_tensor(raw_data_features)
normalize = layers.Normalization()
normalize.adapt(raw_data_features)


#model !!!!
input_shapes = (1, 14)
hid1 = layers.LSTM(units=14, input_shape=input_shapes, return_sequences=True) #random hiddne layers
hid2 =layers.LSTM(units=14)
output = layers.Dense(units=1) #random output layers 
model = keras.Sequential([
    hid1,
    hid2,
    output
])

raw_data_features = tf.reshape(raw_data_features, [14980, 1, 14])
#raw_data_features = tf.convert_to_tensor(raw_data_features)
#print(raw_data_features)

loss = tf.losses.binary_crossentropy
model.compile(optimizer='adam', loss = loss)

model.summary()

history = model.fit(raw_data_features, target, epochs=50, validation_split=0.75, verbose=2, callbacks=[cp_callback])
#dot_img_file = '/model_1.png'
#tf.keras.utils.plot_model(model, to_file=dot_img_file, show_shapes=True)

print(history.history)

from matplotlib import pyplot as plt

plt.plot(history.history['loss'])
plt.plot(history.history['val_loss'])
plt.title('model loss')
plt.ylabel('loss')
plt.xlabel('epoch')
plt.legend(['train', 'val'], loc='upper left')
plt.show()