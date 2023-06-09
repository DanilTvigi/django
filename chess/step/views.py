from django.http import HttpResponse
from subprocess import Popen, PIPE
import cv2
import numpy as np
from PIL import Image
import search
import camera
from analyse import Analyse
from step.models import Desk
from users.models import SessionConnection
from datetime import datetime
from step.models import Steps
from django.shortcuts import render, redirect



def analyse(request):
    img = camera.get_img("10.2.31.25","admin","Skills39!", True)
    tmp = bytes()
    for t in img:
        tmp += t
    nparr = np.frombuffer(tmp, np.uint8)
    img_np = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    cv2.imwrite('tmp.png', img_np)
    img_np = cv2.imread('tmp.png', 1)

    # color = {'a1': 1, 'b1': 1, 'c1': 1, 'd1': 1, 'e1': 1, 'f1': 1, 'g1': 1, 'h1': 1, 
    #                  'a2': 0, 'b2': 1, 'c2': 0, 'd2': 1, 'e2': 1, 'f2': 1, 'g2': 1, 'h2': 1, 
    #                  'a3': 0, 'b3': 0, 'c3': 0, 'd3': 0, 'e3': 0, 'f3': 0, 'g3': 0, 'h3': 0, 
    #                  'a4': 1, 'b4': 0, 'c4': 1, 'd4': 0, 'e4': 0, 'f4': 0, 'g4': 0, 'h4': 0, 
    #                  'a5': 0, 'b5': 0, 'c5': 0, 'd5': 0, 'e5': 0, 'f5': 0, 'g5': 0, 'h5': 0, 
    #                  'a6': 1, 'b6': 0, 'c6': 0, 'd6': 0, 'e6': 0, 'f6': 0, 'g6': 0, 'h6': 0, 
    #                  'a7': 0, 'b7': 1, 'c7': 1, 'd7': 1, 'e7': 1, 'f7': 1, 'g7': 1, 'h7': 1, 
    #                  'a8': 1, 'b8': 1, 'c8': 1, 'd8': 1, 'e8': 1, 'f8': 1, 'g8': 1, 'h8': 1}
    pin_game = request.session.get('pin')
    # QRs = Analyse.search_qr_code(temp)
    # cords_ancle = Analyse.cords_ancle_board(QRs)
    # cords = SessionConnection.objects.get(pin_game=pin_game)
    # cords_ancle = list(cords.cords_ancle)
    cords_ancle = request.session.get('cords_ancle')

    kletki, color, step_v, step_g = Analyse.search_cell(cords_ancle)
    color = Analyse.color_pixel(img_np, kletki, color, step_v, step_g)
    steps = Steps.objects.filter(pin_game=pin_game).order_by('-queue_step')
    y = steps.first()
    moves = y.moves
    moves, step = Analyse.step(color, moves) # moves массив прошлого хода
    record = SessionConnection.objects.get(pin_game=pin_game)
    user_id_W = record.user1_id
    user_id_B = record.user2_id
    time = datetime.now()
    queue_step = request.GET.get("variable")



    new_record = Steps.objects.create(pin_game=pin_game,
                                      queue_step=queue_step,
                                      moves=moves,
                                      user_id_W=user_id_W,
                                      user_id_B=user_id_B,
                                      step=step,
                                      time=time)
    return HttpResponse('ok')

def ViewGame(request, pin):
    records = Steps.objects.filter(pin_game=pin)




    return render(request, "ViewGame.html")