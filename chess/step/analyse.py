import cv2
import numpy as np
from PIL import Image

class Analyse:
    def search_qr_code(temp):
        QRs = {}
        for w in temp:
            if   w.data == b"1":
                # print("1")
                x = max(list(map(lambda a: a.x, w.polygon)))
                y = min(list(map(lambda a: a.y, w.polygon)))
                QRs['1'] = [x,y]
            elif w.data == b"2":
                # print("2")
                x = max(list(map(lambda a: a.x, w.polygon)))
                y = max(list(map(lambda a: a.y, w.polygon)))
                QRs['2'] = [x,y]
                
            elif w.data == b"3":
                # print("3")
                x = min(list(map(lambda a: a.x, w.polygon)))
                y = max(list(map(lambda a: a.y, w.polygon)))
                QRs['3'] = [x,y]
                
                
            elif w.data == b"4":
                # print("4")
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
    

    def search_cell(cords_ancle, img_np):
        kletki = dict()
        color = dict()
        past_pole =  dict()
        #[[651, 942], [651, 350], [1225, 350], [1225, 942]]
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
                color[mark] = ''
                past_pole[mark] = ''
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
            

        # for key in cords_quarter4:
        #     x, y = key
        #     cv2.rectangle(img_np, (x, y), (x+50,y+50), (0,0,255), 2)

        # for key in kletki:
        #     x, y = kletki[key]
        #     cv2.rectangle(img_np, (x, y), (x+50,y+50), (0,0,255), 2)

        cv2.imwrite('res.png', img_np)
        return img_np, kletki, color, past_pole
    
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
            # color[key] = round((sum_r / 55) + (sum_g / 55) + (sum_b / 55))
            if round((sum_r / 45) + (sum_g / 45) + (sum_b / 45)) > 1000:
                color[key] = 1
            else:
                color[key] = 0
        return color
    
    def step(color, moves, past_pole):
        lenght = len(moves)
        # past_pole = {'A1': 'WR', 'B1': 'WH', 'C1': 'WB', 'D1': 'WQ', 'E1': 'WK', 'F1': 'WB', 'G1': 'WH', 'H1': 'WR', 
        #             'A2': 'WP', 'B2': 'WP', 'C2': 'WP', 'D2': 'WP', 'E2': 'WP', 'F2': 'WP', 'G2': 'WP', 'H2': 'WP', 
        #             'A3': '', 'B3': '', 'C3': '', 'D3': '', 'E3': '', 'F3': '', 'G3': '', 'H3': '', 
        #             'A4': '', 'B4': '', 'C4': '', 'D4': '', 'E4': '', 'F4': '', 'G4': '', 'H4': '', 
        #             'A5': '', 'B5': '', 'C5': '', 'D5': '', 'E5': '', 'F5': '', 'G5': '', 'H5': '', 
        #             'A6': '', 'B6': '', 'C6': '', 'D6': '', 'E6': '', 'F6': '', 'G6': '', 'H6': '', 
        #             'A7': 'BP', 'B7': 'BP', 'C7': 'BP', 'D7': 'BP', 'E7': 'BP', 'F7': 'BP', 'G7': 'BP', 'H7': 'BP', 
        #             'A8': 'BR', 'B8': 'BH', 'C8': 'BB', 'D8': 'BQ', 'E8': 'BK', 'F8': 'BB', 'G8': 'BH', 'H8': 'BR'}


        for i in range(lenght):
            past_pole[i]=moves[i]

        # past_pole = {'A1': '1', 'B1': '1', 'C1': '1', 'D1': '1', 'E1': '1', 'F1': '1', 'G1': '1', 'H1': '1', 
        #              'A2': '1', 'B2': '1', 'C2': '1', 'D2': '1', 'E2': '1', 'F2': '1', 'G2': '1', 'H2': '1', 
        #              'A3': '0', 'B3': '0', 'C3': '0', 'D3': '0', 'E3': '0', 'F3': '0', 'G3': '0', 'H3': '0', 
        #              'A4': '0', 'B4': '0', 'C4': '0', 'D4': '0', 'E4': '0', 'F4': '0', 'G4': '0', 'H4': '0', 
        #              'A5': '0', 'B5': '0', 'C5': '0', 'D5': '0', 'E5': '0', 'F5': '0', 'G5': '0', 'H5': '0', 
        #              'A6': '0', 'B6': '0', 'C6': '0', 'D6': '0', 'E6': '0', 'F6': '0', 'G6': '0', 'H6': '0', 
        #              'A7': '1', 'B7': '1', 'C7': '1', 'D7': '1', 'E7': '1', 'F7': '1', 'G7': '1', 'H7': '1', 
        #              'A8': '1', 'B8': '1', 'C8': '1', 'D8': '1', 'E8': '1', 'F8': '1', 'G8': '1', 'H8': '1'}
        
        current_pole = color

        past_cell, new_cell = '', ''
        step = ''

        for key in current_pole:
            if current_pole[key] == past_pole[key]:
                continue
            else:
                if current_pole[key] == '0':
                    past_cell = key
                    past_pole[key] = '0' 
                elif current_pole[key] == '1':
                    new_cell = key
                    past_pole[key] = '1'
            if past_cell != '' and new_cell != '':
                break
        step = past_cell + new_cell
        
        for i in range(lenght):
            moves[i]=past_pole[i]

        return moves, step