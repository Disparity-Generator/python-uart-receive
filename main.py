import time

import imageio as imageio
import scipy
import serial
import os

from scipy.io import matlab
from serial import PARITY_NONE, STOPBITS_ONE
import numpy as np
from PIL import Image
import cv2 as cv

s = serial.Serial("COM7", baudrate=115200, bytesize=8, parity=PARITY_NONE, stopbits=STOPBITS_ONE, rtscts=True)

pairCount = 1

image_count = 1

def receive_image(path, title, width, height):
    data_sent = 0
    current_row_data = []
    current_pixel_data = []
    current_color = 0
    current_row = 0
    current_column = 0
    received_data = np.zeros(shape=(480, 640, 3), dtype=np.uint8)

    while (data_sent < width * height * 1):
        data = s.read()
        current_pixel_data.append(int(data.hex(), 16))
        current_pixel_data.append(int(data.hex(), 16))
        current_pixel_data.append(int(data.hex(), 16))

        current_row_data.append(current_pixel_data)
        current_pixel_data = []
        current_color = 0

        if current_column < 639:
            current_column = current_column + 1
        else:
            received_data[current_row] = current_row_data
            current_row_data = []
            current_column = 0
            current_row = current_row + 1

        if (data_sent % 600 == 0):
            print(str(data.hex()) + " " + str(
                str(data_sent) + " / " + str(307200 * 1) + " - " + str(round(data_sent / (307200 * 1) * 100)) + "%"))
        data_sent = data_sent + 1
        print(str(data_sent))

    cv.imwrite(path + "/" + title, received_data)

while(1):
    if not os.path.exists("./empfangeneBilder"):
        os.makedirs("./empfangeneBilder")

    if pairCount == 1:
        title = "Bild_links_" + str(image_count) + ".png"
        pairCount = 2
    elif pairCount == 2:
        title = "Bild_rechts_" + str(image_count) + ".png"
        pairCount = 3
    else:
        title = "Bild_rektifiziert_" + str(image_count) + ".png"
        pairCount = 1
        image_count = image_count + 1

    receive_image("./empfangeneBilder/", title, 640, 480)
