import cv2
import numpy as np
from PIL import Image

class Analyse:
    def search_qr_code(temp):
        QRs = {}
        for w in temp:
            if   w.data == b"1":
                print("1")
                x = max(list(map(lambda a: a.x, w.polygon)))
                y = min(list(map(lambda a: a.y, w.polygon)))
                QRs['1'] = [x,y]
            elif w.data == b"2":
                print("2")
                x = max(list(map(lambda a: a.x, w.polygon)))
                y = max(list(map(lambda a: a.y, w.polygon)))
                QRs['2'] = [x,y]
                
            elif w.data == b"3":
                print("3")
                x = min(list(map(lambda a: a.x, w.polygon)))
                y = max(list(map(lambda a: a.y, w.polygon)))
                QRs['3'] = [x,y]
                
                
            elif w.data == b"4":
                print("4")
                x = min(list(map(lambda a: a.x, w.polygon)))
                y = min(list(map(lambda a: a.y, w.polygon)))
                QRs['4'] = [x,y]
        return QRs
    
    def cords_ancle_board(QRs):
        # search 'One' coordinate
        cords_ancle = []
        if len(QRs.keys()) >= 2:
            # One side or diagonal?
            if ('1' in QRs.keys() and '3' in QRs.keys()) or ('2' in QRs.keys() and '4' in QRs.keys()): #diagonal
                if ('1' in QRs.keys() and '3' in QRs.keys()):
                    cords_ancle.append(QRs['1'])
                    cords_ancle.append([QRs['1'][0],QRs['3'][1]])
                    cords_ancle.append(QRs['3'])
                    cords_ancle.append([QRs['3'][0],QRs['1'][1]])
                elif ("2" in QRs.keys() and "4" in QRs.keys()):
                    cords_ancle.append([QRs['2'][0],QRs['4'][1]])
                    cords_ancle.append(QRs['2'])
                    cords_ancle.append([QRs['4'][0],QRs['2'][1]])
                    cords_ancle.append(QRs['4'])
            else: #one side
                if('1' in QRs.keys() and '2' in QRs.keys()):
                    a1 = QRs['1'][1] - QRs['2'][1]
                    cords_ancle.append(QRs['1'])
                    cords_ancle.append(QRs['2'])
                    cords_ancle.append([QRs['2'][0]+a1, QRs['2'][1]])
                    cords_ancle.append([QRs['1'][0]+a1, QRs['1'][1]])


                elif('1' in QRs.keys() and '4' in QRs.keys()):
                    b2 = QRs['4'][0] - QRs['1'][0]
                    cords_ancle.append(QRs['1'])
                    cords_ancle.append([QRs['1'][0],QRs['1'][1]-b2])
                    cords_ancle.append([QRs['4'][0],QRs['4'][1]-b2])
                    cords_ancle.append(QRs['4'])


                elif('3' in QRs.keys() and '2' in QRs.keys()):
                    b1 = QRs['3'][0] - QRs['2'][0]
                    cords_ancle.append([QRs['2'][0],QRs['2'][1]+b1])
                    cords_ancle.append(QRs['2'])
                    cords_ancle.append(QRs['3'])
                    cords_ancle.append([QRs['3'][0],QRs['3'][1]+b1])


                elif('3' in QRs.keys() and '4' in QRs.keys()):
                    a2 = QRs['4'][1] - QRs['3'][1]
                    cords_ancle.append([QRs['4'][0]-a2,QRs['4'][1]])
                    cords_ancle.append([QRs['3'][0]-a2,QRs['3'][1]])
                    cords_ancle.append(QRs['3'])
                    cords_ancle.append(QRs['4'])
        return cords_ancle
    

    def search_cell(cords_ancle):
        kletki = dict()
        color = dict()
        print(cords_ancle)
        print(cords_ancle[0][1])
        print(cords_ancle[1][1])
        v = cords_ancle[0][1] - cords_ancle[1][1]
        g = cords_ancle[2][0] - cords_ancle[1][0]

        step_v = int(v / 8)
        step_g = int(g / 8)
        ref_point1 = cords_ancle[1] #[651, 350]
        ref_point2 = cords_ancle[2] #[1225, 350]
        ref_point3 = cords_ancle[0] #[651, 942]
        ref_point4 = cords_ancle[3] #[1225, 942]
        centre = [int((cords_ancle[2][0] - cords_ancle[1][0]) / 2 + cords_ancle[1][0]),
                  int((cords_ancle[0][1] - cords_ancle[1][1]) / 2 + cords_ancle[1][1])]
        quarter1, quarter2, quarter3, quarter4 = dict(), dict(), dict(), dict()
        f = 0                    
        # 1 четверть 9-12ч
        chet_quarter1 = 0 
        cords_quarter1 = []
        for i in range(ref_point1[1], centre[1], step_v):
            f += 1
            s = 0
            if f>4: break
            for j in range(ref_point1[0], centre[0]+step_g, step_g):
                s += 1
                if s>4: break
                cord = j+5, i+3
                cords_quarter1.append(cord)
        # print('1')
        # print(cords_quarter1)
        for i in range(8,4,-1):
            for j in ['a', 'b', 'c', 'd']:
                mark =  j + str(i)
                quarter1[mark] = cords_quarter1[chet_quarter1]
                chet_quarter1 += 1
        # 2 четверть 12-3ч
        f = 0  
        chet_quarter2 = 0 
        cords_quarter2 = []
        for i in range(ref_point2[1], centre[1], step_v):
            f += 1
            s = 0
            if f>4: break
            for j in range(ref_point2[0], centre[0]-step_g, -step_g):
                s += 1
                if s>4: break
                cord = j-55, i+10
                cords_quarter2.append(cord)
        # print('2')
        # print(cords_quarter2)
        for i in range(8,4,-1):
            for j in ['h', 'g', 'f', 'e']:
                mark = j + str(i)
                quarter2[mark] = cords_quarter2[chet_quarter2]
                chet_quarter2 += 1
        # 3 четверть 6-9ч
        chet_quarter3 = 0 
        cords_quarter3 = []
        f = 0  
        for i in range(ref_point3[1], centre[1]-step_v, -step_v):
            f += 1
            s = 0
            if f>4: break
            for j in range(ref_point3[0], centre[0]+step_g, step_g):
                s += 1
                if s>4: break
                cord = j, i-65
                cords_quarter3.append(cord)
        # print('3')
        # print(cords_quarter3)
        for i in range(1,5,1):
            for j in ['a', 'b', 'c', 'd']:
                mark = j + str(i)
                quarter3[mark] = cords_quarter3[chet_quarter3]
                chet_quarter3 += 1

        # 4 четверть 3-6ч
        chet_quarter4 = 0 
        cords_quarter4 = []
        f = 0 
        for i in range(ref_point4[1], centre[1]+step_v, -step_v):
            f += 1
            s = 0
            if f>4: break
            for j in range(ref_point4[0], centre[0]-step_g, -step_g):
                s += 1
                if s>4: break
                cord = j-55, i-55
                cords_quarter4.append(cord)
        # print('4')
        # print(cords_quarter4)
        for i in range(1,5,1):
            for j in ['h', 'g', 'f', 'e']:
                mark = j + str(i)
                quarter4[mark] = cords_quarter4[chet_quarter4]
                chet_quarter4 += 1

        letter = ['a','b','c','d','e','f','g','h']
        chet = 0 
        for i in range(1,9):
            for j in letter:
                mark = j + str(i)
                kletki[mark] = ''
                color[mark] = 0
                chet += 1

        for key in kletki:
            if key in quarter1.keys():
                kletki[key] = quarter1[key]
            elif key in quarter2.keys():
                kletki[key] = quarter2[key]
            elif key in quarter3.keys():
                kletki[key] = quarter3[key]
            elif key in quarter4.keys():
                kletki[key] = quarter4[key]
        # cv2.imwrite('res.png', img_np)
        return kletki, color
    
    def color_pixel(img_np, kletki, color):
        img_gray = cv2.cvtColor(img_np, cv2.COLOR_BGR2GRAY)  
        # ret, thresh1 = cv2.threshold(img_gray, 200, 300, cv2.THRESH_BINARY)
        edges_K = cv2.Canny(img_gray,120,400)
        cv2.imwrite('res2.png', edges_K)
        img = Image.open('res2.png')
        img = img.convert('RGB')    
        for key in kletki:
            sum_r, sum_g, sum_b = 0,0,0
            for i in range(0,55,1):
                for j in range(0,55,1):
                    x, y = kletki[key]
                    r, g, b = img.getpixel((x + i, y + j))
                    sum_r += r
                    sum_g += g
                    sum_b += b
            if round((sum_r / 45) + (sum_g / 45) + (sum_b / 45)) > 1000:
                color[key] = 1
            else:
                color[key] = 0
        return color
    
    def step(color, moves):
        
        past_pole = {'a1': 2, 'b1': 2, 'c1': 2, 'd1': 2, 'e1': 2, 'f1': 2, 'g1': 2, 'h1': 2, 
                     'a2': 2, 'b2': 2, 'c2': 2, 'd2': 2, 'e2': 2, 'f2': 2, 'g2': 2, 'h2': 2, 
                     'a3': 2, 'b3': 2, 'c3': 2, 'd3': 2, 'e3': 2, 'f3': 2, 'g3': 2, 'h3': 2, 
                     'a4': 2, 'b4': 2, 'c4': 2, 'd4': 2, 'e4': 2, 'f4': 2, 'g4': 2, 'h4': 2, 
                     'a5': 2, 'b5': 2, 'c5': 2, 'd5': 2, 'e5': 2, 'f5': 2, 'g5': 2, 'h5': 2, 
                     'a6': 2, 'b6': 2, 'c6': 2, 'd6': 2, 'e6': 2, 'f6': 2, 'g6': 2, 'h6': 2, 
                     'a7': 2, 'b7': 2, 'c7': 2, 'd7': 2, 'e7': 2, 'f7': 2, 'g7': 2, 'h7': 2, 
                     'a8': 2, 'b8': 2, 'c8': 2, 'd8': 2, 'e8': 2, 'f8': 2, 'g8': 2, 'h8': 2}

        keys = list(past_pole.keys())  
        for i in range(len(keys)):
            past_pole[keys[i]] = int(moves[i])

        past_cell, new_cell = '', ''
        step = ''
        for key in color:
            if color[key] != past_pole[key]:
                if color[key] == 1:
                    new_cell = key
                else:
                    past_cell = key
        step = past_cell + new_cell
        past_pole[new_cell] = 1
        past_pole[past_cell] = 0
        moves = ''.join(str(value) for value in past_pole.values())
        return moves, step