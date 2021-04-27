import argparse
import os

import cv2
from keras.models import load_model
import pandas
from tqdm import tqdm

from split_image import *
from gpsinfo import getGPS

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('dir')
    args = parser.parse_args()

    data = {
        'Latitude': [],
        'Longitude': [],
        'Imagem': [],
        'Probabilidade': []
    }

    model = load_model('model.h5')

    for path in tqdm(os.listdir(args.dir)):
        image = cv2.imread(os.path.join(args.dir, path)).astype('float32')
        image *= (1.0 / 255.0)
        # result = numpy.zeros(image.shape)

        p = 0
        # i = 0
        # r = 0
        # c = 0
        subimages = [cv2.resize(sub, (128, 128)) for sub in split_image_fixed(image, 512, 512)]
        subimages = numpy.array(subimages)
        predict = model.predict(subimages)
        argmax = numpy.argmax(predict, axis=1)
        p += argmax.sum()

        # if (c + 1) * 128 > image.shape[1]:
        #     c = 0
        #     r += 1
        # result[r * 128:(r+1) * 128, c * 128:(c+1) * 128, :] = numpy.argmax(predict) * 255
        # c += 1
        # i += 1

        # cv2.imwrite(os.path.join(args.dir, 'prob-map-{}'.format(path)), result)
        p /= subimages.shape[0]
        gps = getGPS(os.path.join(args.dir, path))
        try:
            data['Latitude'].append(','.join((str(gps['longitude']), str(gps['latitude']))))
        except Exception as e:
            data['Latitude'].append('')
            print(e)
            exit(-1)
        data['Longitude'].append('')
        data['Imagem'].append(path)
        data['Probabilidade'].append(p)

    df = pandas.DataFrame(data)
    df.to_csv(f'oleo-{os.path.basename(args.dir)}.csv', index=False, sep=';')
