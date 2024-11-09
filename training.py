import pandas as pd
import numpy as np
import os
import cv2
import matplotlib.pyplot as plt
from src import *
from sklearn.model_selection import train_test_split
from keras.models import Sequential
from keras.optimizers import Adam
from keras.callbacks import ModelCheckpoint
from keras.layers import Lambda, Conv2D, Dropout, Dense, Flatten

# Define hyperparameters
nb_epoch = 10
samples_per_epoch = 1000
batch_size = 32
save_best_only = True
learning_rate = 1e-4

# Read data
print('Reading data...')
data_dir = 'data/processed/track1'
data_df = pd.read_csv(os.path.join(data_dir, 'driving_log.csv'))

# Take image for training, steering angle for label
print('Processing data...')
X = data_df[['image_path']].values
y = data_df['steering_angle'].values

# Remove zero steering angle data, just keep 1000 of them
pos_zero = np.array(np.where(y==0)).reshape(-1, 1)
pos_none_zero = np.array(np.where(y!=0)).reshape(-1, 1)
np.random.shuffle(pos_zero)
pos_zero = pos_zero[:1000]
pos_combined = np.vstack((pos_zero, pos_none_zero))
pos_combined = pos_combined.flatten()

y = y[pos_combined].reshape(len(pos_combined))
X = X[pos_combined, :]

X_train, X_valid, y_train, y_valid = train_test_split(X, y, test_size=0.2, \
random_state=0)

# Define model
print('Defining model...')
model = Sequential()
model.add(Lambda(lambda x: x / 127.5 - 1.0, input_shape=(66, 200, 3)))
model.add(Conv2D(24, (5, 5), activation='elu', strides=(2, 2)))
model.add(Conv2D(36, (5, 5), activation='elu', strides=(2, 2)))
model.add(Conv2D(48, (5, 5), activation='elu', strides=(2, 2)))
model.add(Conv2D(64, (3, 3), activation='elu'))
model.add(Conv2D(64, (3, 3), activation='elu'))
model.add(Dropout(0.5))
model.add(Flatten())
model.add(Dense(100, activation='elu'))
model.add(Dropout(0.5))
model.add(Dense(50, activation='elu'))
model.add(Dense(10, activation='elu'))
model.add(Dense(1))

# Checkpoint to save the best model after each epoch
checkpoint = ModelCheckpoint(
    filepath='models/model.keras',
    monitor='val_loss',
    save_best_only=save_best_only,
    mode='auto'
)

# Use mean squared error for loss function and Adam optimizer
model.compile(loss='mean_squared_error', optimizer=Adam(learning_rate=learning_rate))

# Train model
print('Training model...')
H = model.fit(
    batch_generator(X_train, y_train, batch_size),
    steps_per_epoch=samples_per_epoch,
    epochs=nb_epoch,
    validation_data=batch_generator(X_valid, y_valid, batch_size),
    validation_steps=len(X_valid) // batch_size,
    callbacks=[checkpoint],
    verbose=1
)