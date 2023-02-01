from keras.models import load_model
import numpy as np
from keras.utils.np_utils import to_categorical
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

model = load_model('trainedModel.h5')

model.summary()

df = pd.read_csv(
    "EEG_Data.csv")

numbers = [0, 0]
for number in numbers:
    df = df.drop(df.columns[number], axis=1)
X = df.iloc[:, :-1].to_numpy()
X = StandardScaler().fit_transform(X)
# Select the classificaiton labels
y = df.iloc[:,1].to_numpy()

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42)



model.fit(
  X_train, 
  y_train,
  epochs=300, 
  validation_split=0.1
)