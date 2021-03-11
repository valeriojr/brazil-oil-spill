# -*- coding: utf-8 -*-
"""Untitled1.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1CuWmlKWsGjnkHMo7c3IZQ-1SQb4Hg5kv
"""

import json
from os import path

from keras import layers, losses, metrics, models
from keras.preprocessing.image import ImageDataGenerator

"""# Constantes"""

INP = 128
NUM_CLASSES = 2
BATCH_SIZE = 32
DATA_PATH = '../brazil-oil-spill_data'

"""# Parâmetros"""

with open('params.json') as fp:
    param_grid = json.load(fp)

"""# Modelo"""


def create_model(conv_layers=1, filters=16, kernel_size=3, dense_units=(25,)):
    model = models.Sequential()

    # Convolutional layers
    for i in range(conv_layers):
        model.add(layers.Conv2D(filters, (kernel_size, kernel_size), input_shape=(INP, INP, 3), activation='relu'))
        model.add(layers.MaxPooling2D(pool_size=(2, 2)))

    model.add(layers.Flatten())

    # Dense layers
    for units in dense_units:
        model.add(layers.Dense(units=units, activation='relu'))

    model.add(layers.Dense(units=NUM_CLASSES, activation='softmax'))
    model.compile(optimizer='adam', loss=losses.categorical_crossentropy,
                  metrics=['accuracy', metrics.categorical_accuracy])

    return model


"""# Dados"""

train_datagen = ImageDataGenerator(rescale=1. / 255,
                                   # zoom_range = 0.05,
                                   # rotation_range=20,
                                   vertical_flip=True,
                                   horizontal_flip=True)

test_datagen = ImageDataGenerator(rescale=1. / 255)

training_set = train_datagen.flow_from_directory(path.join(DATA_PATH, 'dados/train'),
                                                 shuffle=True,
                                                 target_size=(INP, INP),
                                                 batch_size=BATCH_SIZE,
                                                 class_mode='categorical')

test_set = train_datagen.flow_from_directory(path.join(DATA_PATH, 'dados/valid'),
                                             shuffle=False,
                                             target_size=(INP, INP),
                                             batch_size=1,
                                             class_mode='categorical')

soma = 1251.0 + 476.0

class_weights = {
    0: 476.0 / soma * 2,
    1: 1251.0 / soma
}
experiments = []

for conv_layers in param_grid['conv_layers']:
    for filters in param_grid['filters']:
        for kernel_size in param_grid['kernel_size']:
            for dense_units in param_grid['dense_units']:
                model = create_model(conv_layers, filters, kernel_size, dense_units)
                experiments.append({
                    'params': {
                        'conv_layers': conv_layers,
                        'filters': filters,
                        'kernel_size': kernel_size,
                        'dense_units': dense_units,
                    },
                    'history': model.fit(training_set,
                                         steps_per_epoch=training_set.samples // BATCH_SIZE,
                                         epochs=10,
                                         validation_data=test_set,
                                         validation_steps=test_set.samples // 1,
                                         workers=4,
                                         class_weight=class_weights).history
                })

with open('grid_search_result.json', 'w') as fp:
    json.dump(experiments, fp)
