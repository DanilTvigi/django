import cv2  
import numpy as np  
from PIL import Image
import pyzbar.pyzbar as pyzbar

class Analyse:   
    def step(image): #, temp1, temp2
        def search(image, temp):
                if type(image) == type(""):
                    img_rgb = cv2.imread(image,1)
                else:
                    img_rgb = image
                img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)  
                edges_K = cv2.Canny(img_gray,50,70)
                cv2.imwrite('res22.png', edges_K)
                img = cv2.imread('res22.png')
                template = cv2.imread(temp,0)  
                res = cv2.matchTemplate(img_gray,template,cv2.TM_CCOEFF_NORMED)   
                threshold = 0.8  
                loc = np.where( res >= threshold) 
                return img, loc

        def color_pixel(kletki, img, color):
            img = img.convert('RGB')    
            for key in kletki:
                sum_r, sum_g, sum_b = 0,0,0
                for i in range(0,45,1):
                    for j in range(0,45,1):
                        x, y = kletki[key]
                        r, g, b = img.getpixel((x + i, y + j))
                        sum_r += r
                        sum_g += g
                        sum_b += b
                color[key] = round((sum_r / 45) + (sum_g / 45) + (sum_b / 45))
                # if round((sum_r / 45) + (sum_g / 45) + (sum_b / 45)) > 0:
                #     color[key] = 1
            return color
        
        def get_board_coordinates(image):
            temp = []
            arrX = []
            arrY = []
            # Отделяем данные 
            minX = False
            maxX = False

            for w in temp:
                x,y = w
                cv2.rectangle(image, (x,y), (x+45,y+45), (0,255,0), 1)
            cv2.imwrite('res.png', image) 
            return ""

        image = r'C:\\Users\\danil\\Desktop\\chess\\main\\images\\board.jpg'
        temp = r'C:\\Users\\danil\\Desktop\\chess\\main\\images\\template_edge.jpg'
        img_rgb, loc1 = search(image, temp1)
        img_rgb1, loc2 = search(image, temp2)
        os_y_min = list()
        os_x_min = list()
        os_y_max = list()
        os_x_max = list()
        for pt in zip(*loc1[::-1]):
            os_x_min.append(pt[0])
            os_y_min.append(pt[1])
        for pt in zip(*loc2[::-1]):
            os_x_max.append(pt[0])
            os_y_max.append(pt[1])
        x_min, y_min =  min(os_x_min) + 100, min(os_y_min) + 95
        x_max, y_max =  min(os_x_max), min(os_y_max)
        kletki = dict()
        color = dict()
        pole_def = {'A1': 'WR', 'B1': 'WH', 'C1': 'WB', 'D1': 'WQ', 'E1': 'WK', 'F1': 'WB', 'G1': 'WH', 'H1': 'WR', 
                'A2': 'WP', 'B2': 'WP', 'C2': 'WP', 'D2': 'WP', 'E2': 'WP', 'F2': 'WP', 'G2': 'WP', 'H2': 'WP', 
                'A3': '', 'B3': '', 'C3': '', 'D3': '', 'E3': '', 'F3': '', 'G3': '', 'H3': '', 
                'A4': '', 'B4': '', 'C4': '', 'D4': '', 'E4': '', 'F4': '', 'G4': '', 'H4': '', 
                'A5': '', 'B5': '', 'C5': '', 'D5': '', 'E5': '', 'F5': '', 'G5': '', 'H5': '', 
                'A6': '', 'B6': '', 'C6': '', 'D6': '', 'E6': '', 'F6': '', 'G6': '', 'H6': '', 
                'A7': 'BP', 'B7': 'BP', 'C7': 'BP', 'D7': 'BP', 'E7': 'BP', 'F7': 'BP', 'G7': 'BP', 'H7': 'BP', 
                'A8': 'BR', 'B8': 'BH', 'C8': 'BB', 'D8': 'BQ', 'E8': 'BK', 'F8': 'BB', 'G8': 'BH', 'H8': 'BR'}
        cords = list()
        step_v = int((y_max - y_min) / 8)  
        step_g = int((x_max - x_min) / 8)  
        letter = ['A','B','C','D','E','F','G','H']
        # letter = ['H','G','F','E','D','C','B','A']
        for i in range(y_min,y_max-step_v, step_v):
            for j in range(x_min,x_max-step_g,step_g):
                img_rgb[i][j] = (0,0,255)
                cord = j, i
                cords.append(cord)
        chet = 0
        for i in range(1,9):
            for j in letter:
                mark = j + str(i)
                kletki[mark] = cords[chet]
                color[mark] = ''
                chet += 1

        img = Image.open('res22.png')
        color = color_pixel(kletki, img, color)
        for pt in cords:
            x,y = pt
            cv2.rectangle(img_rgb, (x,y), (x+45,y+45), (0,255,0), 1)
        for key in kletki:
            cv2.putText(img_rgb, str(color[key]), kletki[key], cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0,255,0), 1)
        cv2.imwrite('res.png', img_rgb)   
        return color
        print(get_board_coordinates(image))
        return ""
