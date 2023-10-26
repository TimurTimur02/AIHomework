import os
import random
import shutil
import scipy
import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense

base_dir = 'archive'

input_shape = (150, 150, 3)
learning_rate = 0.001
batch_size = 64
epochs = 20

train_dir = os.path.join(base_dir, 'train')
val_dir = os.path.join(base_dir, 'val')
demo_dir = os.path.join(base_dir, 'demo')

train_datagen = ImageDataGenerator(rescale=1.0/255.0)
train_generator = train_datagen.flow_from_directory(train_dir, target_size=input_shape[:2], batch_size=batch_size, class_mode='categorical')

val_datagen = ImageDataGenerator(rescale=1.0/255.0)
val_generator = val_datagen.flow_from_directory(val_dir, target_size=input_shape[:2], batch_size=batch_size, class_mode='categorical')

model = Sequential()
model.add(Conv2D(32, (3, 3), activation='relu', input_shape=input_shape))
model.add(MaxPooling2D((2, 2)))
model.add(Conv2D(64, (3, 3), activation='relu'))
model.add(MaxPooling2D((2, 2)))
model.add(Flatten())
model.add(Dense(64, activation='relu'))
model.add(Dense(2, activation='softmax'))

model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=learning_rate), loss='categorical_crossentropy', metrics=['accuracy'])

model.fit(train_generator, validation_data=val_generator, epochs=epochs)

demo_datagen = ImageDataGenerator(rescale=1.0/255.0)
demo_generator = demo_datagen.flow_from_directory(demo_dir, target_size=input_shape[:2], batch_size=batch_size, class_mode='categorical')
test_loss, test_accuracy = model.evaluate(demo_generator)

with open('результаты.txt', 'a') as f:
    f.write(f'Learning Rate: {learning_rate}, Batch Size: {batch_size}, Epochs: {epochs}\n')
    f.write(f'Test Loss: {test_loss}, Test Accuracy: {test_accuracy}\n\n')

