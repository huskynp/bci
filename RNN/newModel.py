import pandas as pd
import numpy as np
import tensorflow as tf
import os
from tensorflow import keras
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Dense, Dropout, Bidirectional, LSTM, Input, Flatten
from sklearn.metrics import roc_auc_score, roc_curve, confusion_matrix, accuracy_score
from scipy import stats
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt

df = pd.read_csv(
    "EEG_Data.csv")

df = df[(np.abs(stats.zscore(df)) < 5).all(axis=1)]

# Select all numerical EEG columns and standardize them
X = df.iloc[:, :-1].to_numpy()
X = StandardScaler().fit_transform(X)
# Select the classificaiton labels
y = df.iloc[:,14].to_numpy()

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42)
checkpoint_path = "checkpoints/eeg.ckpt"
checkpoint_dir = os.path.dirname(checkpoint_path)

num_feature = X_train[0].size

cp_callback = tf.keras.callbacks.ModelCheckpoint(filepath=checkpoint_path,
                                                 save_weights_only=True,
                                                 verbose=1)

# define model layers
inputs = Input(num_feature)
dense1 = Dense(64, activation = 'relu')(inputs)
dropout1 = Dropout(0.2)(dense1)
dense2 = Dense(64, activation = 'relu')(dropout1)
dropout2 = Dropout(0.2)(dense2)
dense3 = Dense(64, activation = 'relu')(dropout2)
outputs = Dense(1, activation='sigmoid')(dense3)

model = Model(inputs, outputs)
model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])

model.summary()

history = model.fit(X_train, y_train, epochs=300, batch_size=32, verbose=2, validation_split=.1)
            
_, acc = model.evaluate(X_test, y_test)
ypred = model.predict(X_test)
auc = roc_auc_score(y_test, ypred)
print("Accuracy = %.2f - AUC = %.2f", acc, auc)

# plot the accuracy and loss during the training
fig, axs = plt.subplots(1, 2, figsize=(8, 4))
axs[0].plot(history.history['accuracy'])
axs[0].plot(history.history['val_accuracy'])
axs[0].set_title('model accuracy')
axs[0].set_ylabel('accuracy')
axs[0].set_xlabel('epoch')
axs[0].legend(['train', 'test'], loc='lower right')

axs[1].plot(history.history['loss'])
axs[1].plot(history.history['val_loss'])
axs[1].set_title('model loss')
axs[1].set_ylabel('loss')
axs[1].set_xlabel('epoch')
axs[1].legend(['train', 'test'], loc='upper right')
plt.tight_layout()
plt.savefig("eyestate_train_acc_loss.png")