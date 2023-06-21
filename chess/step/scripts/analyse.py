import cv2
import numpy as np
from PIL import Image
import statistics
import copy

class Analyse():
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
                cord = j, i
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
                cord = j-70, i #  -10
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
                cord = j-80, i-65
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
        for i in range(8,0, -1):
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
        
        return kletki, color, step_v, step_g
    
    def color_pixel(img_np, kletki, color, step_v, step_g): #
        # test = img_np
        # for key in kletki:
        #     x, y = kletki[key]
        #     cv2.rectangle(test, (x, y), (x+50,y+50), (0,0,255), 2)
        # # # x, y = kletki['f8']
        # cv2.rectangle(test, (x, y), (x+50,y+50), (0,0,255), 2)

        # cv2.imwrite('test.png', test)
        # test_color = copy.deepcopy(color)

        img_gray = cv2.cvtColor(img_np, cv2.COLOR_BGR2GRAY)  
        blurred = cv2.GaussianBlur(img_gray, (11,11), 0)
        edges_K = cv2.Canny(blurred,0, 85)    # 0 50  5 85
        cv2.imwrite('res2.png', edges_K)
        img = Image.open('res2.png')
        img = img.convert('RGB')    
        for key in kletki:
            sum_r, sum_g, sum_b = 0,0,0
            total_brightness = 0
            for i in range(0,60,1):
                for j in range(0,60,1):
                    x, y = kletki[key]
                    r, g, b = img.getpixel((x + i, y + j))
                    sum_r += r
                    sum_g += g
                    sum_b += b
                    
            if round((sum_r / 60) + (sum_g / 60) + (sum_b / 60)) > 1500:
                color[key] = 1
            else:
                color[key] = 0
            # test_color[key] = round((sum_r / 50) + (sum_g / 50) + (sum_b / 50))
        return color
    
    def step(color, old_step, queue_step, new_step, chessgame):   
        print("^^^^^^^^^")
        print(chessgame)
        print("^^^^^^^^^")

        # color наличние фигур на текущем поле
        # old_step растановка фигур на прошлом ходе W or B or ''
        # new_step определение цвета фигуры белая/черная на текущем поле
        # past_pole растановка фигру на прошлом ходе 0 or 1
        step = ""
        # past_pole = copy.deepcopy(color)
        # tmp_location_figur = copy.deepcopy(location_figur)

        if int(queue_step) == 0: # Базовая расстановка
            print(f'step1 {step}')
            return "", new_step
        
        dropF = []
        changeF = []

        for key in old_step.keys():
            if old_step[key] != new_step[key]:
                # Ход
                if new_step[key] == 0: dropF.append(key)
                # Рубка
                else: changeF.append(key)
        

        print(f"dropF = {dropF}")
        print(f"changeF = {changeF}")
        print("^^^^^^^^^")
        # Проверка пропажи
        ## Пропала 1 фигура
        if len(dropF) == 1:
            if len(changeF) == 1:
                # Возможно условие на проверку валидности хода
                step = dropF[0] + changeF[0]
                print(f'step2 {step}')
                
                drop = step[0:2]
                change = step[2:4]
                old_step[change] = old_step[drop]
                old_step[drop] = 0

                return step, new_step
            else:
                for change in changeF:
                    # White
                    if int(queue_step) % 2 == 1:
                        if old_step[changeF] == "W" and new_step[changeF] == "B":
                            changeF.remove(change)
                    # Black
                    else:
                        if old_step[changeF] == "B" and new_step[changeF] == "W":
                            changeF.remove(change)
                if len(changeF) == 1: 
                    step = dropF[0] + changeF[0]
                    print(f'step3 {step}')

                    return step, new_step
                        
        elif len(dropF) == 0:
            step = ""
            print(f'step4 {step}')

            return step, old_step
        else:
            for drop in dropF:
                tmp = drop + changeF[0]
                valid_steps = chessgame.get_moves()

                if tmp in valid_steps:
                    step = tmp
                    return step, new_step

        print(f'step5 {step}')
        
        return step, old_step