from django.http import HttpResponse
from subprocess import Popen, PIPE
import cv2
import numpy as np
import camera
from analyse import Analyse
from users.models import SessionConnection
from datetime import datetime
from step.models import Steps
from django.shortcuts import render, redirect
from django.db.models import Max
from main.models import GameHistory
from newAnalyse import newAnalyse
from Chessnut import Game

def step_runner(step_base):
    chessgame = Game()
    step_base = list(step_base)
    step_base.remove('0')
    print(f"step base | {step_base}")
    if len(step_base) == 0: 
        return chessgame

    for step in step_base:
        chessgame.apply_move(step)

    return chessgame

def print_area(pole):
    for num in range(8,0,-1):
        for letter in ['a','b','c','d','e','f','g','h']:
            key = letter + str(num)
            print(f"{key} = {pole[key]}", end=" | ")
        print()
    print()

def analyse(request):
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
    pin_game = request.session.get('pin')
    # Get coordinates
    cords_ancle = request.session.get('cords_ancle')
    # Get kletki
    kletki, color, step_v, step_g = Analyse.search_cell(cords_ancle)
    color = Analyse.color_pixel(img_np, kletki, color, step_v, step_g)   #

    # save kletki and color
    request.kletki = kletki
    request.color = color

    # Create furyres base
    step_base = Steps.objects.filter(pin_game=pin_game).values_list('step', flat=True)
    chessgame = step_runner(step_base)

    new_analyse = newAnalyse(request)
    new = new_analyse.check_color_figure()


    queue_step = request.GET.get("variable")
    location_figur = request.session.get('location_figur')
    print("*"*70)
    print('OLD:')
    print_area(location_figur)

    step, location_figur = Analyse.step(color, location_figur, queue_step, new, chessgame) 
    print(f'step {step}')
    print(step)
    print('NEW:')
    print_area(location_figur)
    print("*"*70)


    request.session['location_figur'] = location_figur
    record = SessionConnection.objects.get(pin_game=pin_game)
    user_id_W = record.user1_id
    user_id_B = record.user2_id
    time = datetime.now()
    new_record = Steps.objects.create(pin_game=pin_game,
                                      queue_step=queue_step,
                                      user_id_W=user_id_W,
                                      user_id_B=user_id_B,
                                      step=step,
                                      time=time)
    return HttpResponse('ok')

def ViewGame(request, pin):
    players = GameHistory.objects.get(pin_game=pin)
    max_queue_step = Steps.objects.filter(pin_game=pin).aggregate(max_queue_step=Max('queue_step'))['max_queue_step']
    steps = Steps.objects.filter(pin_game=pin).values_list('step', flat=True)[1:]
    mylist = list()
    for i in steps:
        mylist.append(i)
    tmp = ','.join([str(i) for i in mylist])
    data = {
        'players':players,
        'steps':tmp,
    }
    return render(request, "ViewGame.html", context=data)


def EndGame(request):
    if SessionConnection.objects.filter(user2_id = request.user.id).exists():
        obj = SessionConnection.objects.get(user2_id = request.user.id)
    else:
        obj = SessionConnection.objects.get(user1_id = request.user.id)
    obj.delete()
    return redirect('Home')