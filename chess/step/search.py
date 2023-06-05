import pyzbar.pyzbar as pyzbar
from pyzbar.pyzbar import ZBarSymbol
import cv2
import numpy as np

def search(image):
    font = cv2.FONT_HERSHEY_PLAIN
    decodedObjects = pyzbar.decode(image, symbols=[ZBarSymbol.QRCODE])
    temp = []
        # Отделяем данные 
    for w in decodedObjects:
        temp.append(w[3])
    return decodedObjects
