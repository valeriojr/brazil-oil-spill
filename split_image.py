import argparse
import os

import cv2
import numpy


def split_image(image, rows, columns):
    height, width, channels = image.shape
    subimages = []

    for i in range(rows):
        for j in range(columns):
            subheight = height // rows
            subwidth = width // columns
            subimage = numpy.zeros((subheight, subwidth, channels))

            print(subimage.shape)

            subimage[:, :, :] = image[i * subheight:(i + 1) * subheight, j * subwidth:(j + 1) * subwidth, :]
            subimages.append(subimage)

    return subimages


def split_image_fixed(image, width, height):
    img_height, img_width, channels = image.shape

    i = 0
    while (i + 1) * height < img_height:
        j = 0
        while (j + 1) * width < img_width:
            subimage = numpy.zeros((height, width, channels))
            subimage[:, :, :] = image[i * height:(i + 1) * height, j * width:(j + 1) * width, :]
            j += 1
            yield subimage
        i += 1


def split_image_generator(image, rows, columns):
    height, width, channels = image.shape

    for i in range(rows):
        for j in range(columns):
            subheight = rows
            subwidth = columns
            subimage = numpy.zeros((subheight, subwidth, channels))

            print(subimage.shape)

            subimage[:, :, :] = image[i * subheight:(i + 1) * subheight, j * subwidth:(j + 1) * subwidth, :]
            yield subimage


def save_subimages(subimages, filename, dest):
    for i, subimage in enumerate(subimages):
        cv2.imwrite(os.path.join(dest, '{}-{}.png'.format(i, filename)), subimage)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('source')
    parser.add_argument('rows', type=int)
    parser.add_argument('columns', type=int)
    parser.add_argument('dest')
    args = parser.parse_args()

    print(args.source)

    if os.path.isfile(args.source):
        image = cv2.imread(args.source)
        subimages = split_image(image, args.rows, args.columns)
        save_subimages(subimages, args.source, args.dest)
    elif os.path.isdir(args.source):
        for root, dirs, files in os.walk(args.source):
            for file in files:
                image = cv2.imread(os.path.join(root, file))
                try:
                    subimages = split_image(image, args.rows, args.columns)
                    save_subimages(subimages, file, args.dest)
                except Exception as e:
                    print(str(e))

