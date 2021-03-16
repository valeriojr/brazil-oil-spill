import json

import pandas
from tqdm import tqdm
from keras.callbacks import EarlyStopping

import main

pandas.options.display.width = 0

if __name__ == '__main__':
    df = pandas.read_csv('grid_search_results.csv', header=0, dtype={
        'conv_layers': int,
        'filters': int,
        'kernel_size': int,
    })
    df.dense_units = df.dense_units.apply(json.loads)

    need_retraining = df[(df.need_retraining == True) & (df.val_accuracy > 0.85)]

    for i, row in tqdm(need_retraining.iterrows()):
        model = main.create_model(conv_layers=row.conv_layers, filters=row.filters, kernel_size=row.kernel_size,
                                  dense_units=row.dense_units)
        history = model.fit(main.training_set,
                            steps_per_epoch=main.training_set.samples // main.BATCH_SIZE,
                            epochs=100,
                            callbacks=[EarlyStopping(monitor='val_accuracy', patience=3, restore_best_weights=True)],
                            validation_data=main.test_set,
                            validation_steps=main.test_set.samples // 1,
                            workers=4,
                            class_weight=main.class_weights).history

        df.val_accuracy.iloc[row.name] = max(history['val_accuracy'])
        df.need_retraining.iloc[row.name] = False

    df.to_csv('grid_search_results_retrained.csv', index=False)
