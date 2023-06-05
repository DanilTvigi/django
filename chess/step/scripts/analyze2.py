import cv2  
import numpy as np  
from PIL import Image
import pyzbar.pyzbar as pyzbar

class Analyse:   
    def step(image): #, temp1, temp2
       
        def get_board_coordinates(image):
            font = cv2.FONT_HERSHEY_PLAIN
            decodedObjects = pyzbar.decode(image)
            # print(decodedObjects)
            temp = []
            arrX = []
            arrY = []
            # Отделяем данные 
            for w in decodedObjects:
                temp.append(w[3])
                
            minX = False
            maxX = False

            for w in temp:
                print(w[3])

            return temp
        
        temp = get_board_coordinates(image)

        return temp
