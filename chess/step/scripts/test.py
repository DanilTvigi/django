# from django.http import HttpResponse
from subprocess import Popen, PIPE
import cv2
import numpy as np
import camera
from analyse import Analyse
# from users.models import SessionConnection
from datetime import datetime
# from step.models import Steps
# from django.shortcuts import render, redirect
# from django.db.models import Max
# from main.models import GameHistory
from newAnalyse import newAnalyse
import search

def step_runner(step_base):
    figures = {
        'a8': 'L', 'b8': 'H', 'c8': 'B', 'd8': 'K', 'e8': 'F', 'f8': 'B', 'g8': 'H', 'h8': 'L',
        'a7': 'P', 'b7': 'P', 'c7': 'P', 'd7': 'P', 'e7': 'P', 'f7': 'P', 'g7': 'P', 'h7': 'P',
        'a6': '', 'b6': '', 'c6': '', 'd6': '', 'e6': '', 'f6': '', 'g6': '', 'h6': '', 
        'a5': '', 'b5': '', 'c5': '', 'd5': '', 'e5': '', 'f5': '', 'g5': '', 'h5': '',
        'a4': '', 'b4': '', 'c4': '', 'd4': '', 'e4': '', 'f4': '', 'g4': '', 'h4': '', 
        'a3': '', 'b3': '', 'c3': '', 'd3': '', 'e3': '', 'f3': '', 'g3': '', 'h3': '', 
        'a2': 'P', 'b2': 'P', 'c2': 'P', 'd2': 'P', 'e2': 'P', 'f2': 'P', 'g2': 'P', 'h2': 'P',  
        'a1': 'L', 'b1': 'H', 'c1': 'B', 'd1': 'K', 'e1': 'F', 'f1': 'B', 'g1': 'H', 'h1': 'L'
    }
    
    for step in step_base:
        old = step[0:2]
        new = step[2:4]

        figures[new] = figures[old]
        figures[old] = ""

    return figures


def print_area(pole):
    for num in range(8,0,-1):
        for letter in ['a','b','c','d','e','f','g','h']:
            key = letter + str(num)
            print(f"{key} = {pole[key]}", end=" | ")
        print()

def get_base():
    while True:
        try:
            temp = []
            while len(temp) < 2:  
                print('1')
                img = camera.get_img("10.2.31.25","admin","Skills39!", True)
                tmp = bytes()
                for t in img:
                    tmp += t
                nparr = np.frombuffer(tmp, np.uint8)
                img_np = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
                cv2.imwrite('tmp.png', img_np)
                img_np = cv2.imread('tmp.png', 1)
                temp = search.search(img_np) 
            QRs = Analyse.search_qr_code(temp)
            cords_ancle = Analyse.cords_ancle_board(QRs)
            kletki, color, step_v, step_g = Analyse.search_cell(cords_ancle)
            break
        except Exception as a:
                continue
    location_figur = {'a8': 'B', 'b8': 'B', 'c8': 'B', 'd8': 'B', 'e8': 'B', 'f8': 'B', 'g8': 'B', 'h8': 'B',
                    'a7': 'B', 'b7': 'B', 'c7': 'B', 'd7': 'B', 'e7': 'B', 'f7': 'B', 'g7': 'B', 'h7': 'B',
                    'a6': '', 'b6': '', 'c6': '', 'd6': '', 'e6': '', 'f6': '', 'g6': '', 'h6': '', 
                    'a5': '', 'b5': '', 'c5': '', 'd5': '', 'e5': '', 'f5': '', 'g5': '', 'h5': '',
                    'a4': '', 'b4': '', 'c4': '', 'd4': '', 'e4': '', 'f4': '', 'g4': '', 'h4': '', 
                    'a3': '', 'b3': '', 'c3': '', 'd3': '', 'e3': '', 'f3': '', 'g3': '', 'h3': '', 
                    'a2': 'W', 'b2': 'W', 'c2': 'W', 'd2': 'W', 'e2': 'W', 'f2': 'W', 'g2': 'W', 'h2': 'W',  
                    'a1': 'W', 'b1': 'W', 'c1': 'W', 'd1': 'W', 'e1': 'W', 'f1': 'W', 'g1': 'W', 'h1': 'W'}
    
    return [cords_ancle, location_figur]

def analyse(old, cords_ancle, queue_step, step_base):
    figures = step_runner(step_base)
    # Get image
    img = camera.get_img("10.2.31.25","admin","Skills39!", True)
    tmp = bytes()
    for t in img:
        tmp += t
    nparr = np.frombuffer(tmp, np.uint8)
    img_np = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    cv2.imwrite('tmp.png', img_np)
    img_np = cv2.imread('tmp.png', 1)

    # Get pin
    # pin_game = request.session.get('pin')
    # Get coordinates
    # cords_ancle = request.session.get('cords_ancle')
    # Get kletki
    
    kletki, color, step_v, step_g = Analyse.search_cell(cords_ancle)
    color = Analyse.color_pixel(img_np, kletki, color, step_v, step_g)   #

    # save kletki and color

    class req:
        def __init__(self, kletki, color):
            self.kletki = kletki
            self.color = color

    request = req(kletki, color)
    new_analyse = newAnalyse(request)
    
    new = new_analyse.check_color_figure()

    step, old = Analyse.step(color, old, queue_step, new) 
    
    print("*"*70)
    print(f"step = '{step}'")
    print_area(new)
    print()
    print_area(old)
    print("*"*70)

    return step, old

    # request.session['location_figur'] = location_figur
    # record = SessionConnection.objects.get(pin_game=pin_game)
    # user_id_W = record.user1_id
    # user_id_B = record.user2_id
    # time = datetime.now()
    # new_record = Steps.objects.create(pin_game=pin_game,
    #                                   queue_step=queue_step,
    #                                   user_id_W=user_id_W,
    #                                   user_id_B=user_id_B,
    #                                   step=step,
    #                                   time=time)
    

if __name__ == "__main__":
    base = get_base()
    cords_ancle = base[0]
    # location_figur = base[1]
    old = {
        'a8': 'B', 'b8': 'B', 'c8': 'B', 'd8': 'B', 'e8': 'B', 'f8': 'B', 'g8': 'B', 'h8': 'B',
        'a7': 'B', 'b7': 'B', 'c7': 'B', 'd7': 'B', 'e7': 'B', 'f7': 'B', 'g7': 'B', 'h7': 'B',
        'a6': 0, 'b6': 0, 'c6': 0, 'd6': 0, 'e6': 0, 'f6': 0, 'g6': 0, 'h6': 0, 
        'a5': 0, 'b5': 0, 'c5': 0, 'd5': 0, 'e5': 0, 'f5': 0, 'g5': 0, 'h5': 0,
        'a4': 0, 'b4': 0, 'c4': 0, 'd4': 0, 'e4': 0, 'f4': 0, 'g4': 0, 'h4': 0, 
        'a3': 0, 'b3': 0, 'c3': 0, 'd3': 0, 'e3': 0, 'f3': 0, 'g3': 0, 'h3': 0, 
        'a2': 'W', 'b2': 'W', 'c2': 'W', 'd2': 'W', 'e2': 'W', 'f2': 'W', 'g2': 'W', 'h2': 'W',  
        'a1': 'W', 'b1': 'W', 'c1': 'W', 'd1': 'W', 'e1': 'W', 'f1': 'W', 'g1': 'W', 'h1': 'W'
    }

    queue_step = 1

    print("START")
    while(queue_step < 10):
        
        step_base = []
        step, old = analyse(old, cords_ancle, queue_step, step_base)

        if step != "":
            print(f"{queue_step} | step = '{step}'")
            input("NEXT")
            step_base.append(step)
            queue_step+=1