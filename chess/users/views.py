from django.shortcuts import render, redirect
from users.models import SessionConnection, CustomUser
from main.models import GameHistory
from step.models import Desk
from .forms import UserRegisterForm
from django.contrib.auth.decorators import login_required
from .forms import CustomLoginForm
from django.contrib.auth import authenticate, login
import random
from datetime import datetime, timedelta
from step.models import Steps
import search
import camera
from analyse import Analyse
import cv2
import numpy as np




def generate_random_number():
    random_number = random.randint(100000, 999999)
    return random_number

def Registration(request):
	if request.method == 'POST':
		form = UserRegisterForm(request.POST)
		if form.is_valid():
			form.save()
			return redirect('Home')
	else:
		form = UserRegisterForm()
	return render(request, 'Registration.html', {'form': form})


def Login(request):
    if request.method == 'POST':
        form = CustomLoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('Home')
    else:	
        form = CustomLoginForm()
    return render(request, 'Login.html', {'form': form})


@login_required
def PersonalProfile(request, id):
    user_record = CustomUser.objects.get(id=id)
    username = user_record.username 
    play_count = user_record.play_count
    win = user_record.win
    lose = user_record.lose
    minute_in_game = user_record.minuteInGame
    rating = user_record.rating
    email = user_record.email
    data = {'username':username,
            'play_count':play_count,
            'win':win,
            'lose':lose,
            'minute_in_game':minute_in_game,
            'rating':rating,
            'email':email
            }
    return render(request, 'PlayerProfile.html', context=data)


def PlayerProfile(request, id):
    print(id)
    user_record = CustomUser.objects.get(id=id)
    username = user_record.username 
    play_count = user_record.play_count
    win = user_record.win
    lose = user_record.lose
    minute_in_game = user_record.minuteInGame
    rating = user_record.rating
    email = user_record.email
    data = {'username':username,
            'play_count':play_count,
            'win':win,
            'lose':lose,
            'minute_in_game':minute_in_game,
            'rating':rating,
            'email':email
            }
    return render(request, 'PlayerProfile.html', context=data)


@login_required
def LoginGame(request):
    if request.method == 'GET':
        return render(request, 'LoginGame.html')
    if request.method == 'POST':
        pin_input = request.POST.get("pin", "Undefined")
        request.session['pin'] = pin_input
    is_exists = SessionConnection.objects.filter(pin_game=pin_input).exists()
    if is_exists:
        filt_record = SessionConnection.objects.get(pin_game=pin_input)
        user1 = filt_record.user1_id
        user2 = filt_record.user2_id
        curent_user = request.user.id
        if user1 != curent_user and user2 == None and user2 != curent_user:
            a = True
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

             
            location_figur = {'a8': 'WR', 'b8': 'WH', 'c8': 'WB', 'd8': 'WQ', 'e8': 'WK', 'f8': 'WB', 'g8': 'WH', 'h8': 'WR',
                            'a7': 'WP', 'b7': 'WP', 'c7': 'WP', 'd7': 'WP', 'e7': 'WP', 'f7': 'WP', 'g7': 'WP', 'h7': 'WP',
                            'a6': '', 'b6': '', 'c6': '', 'd6': '', 'e6': '', 'f6': '', 'g6': '', 'h6': '', 
                            'a5': '', 'b5': '', 'c5': '', 'd5': '', 'e5': '', 'f5': '', 'g5': '', 'h5': '',
                            'a4': '', 'b4': '', 'c4': '', 'd4': '', 'e4': '', 'f4': '', 'g4': '', 'h4': '', 
                            'a3': '', 'b3': '', 'c3': '', 'd3': '', 'e3': '', 'f3': '', 'g3': '', 'h3': '', 
                            'a2': 'BP', 'b2': 'BP', 'c2': 'BP', 'd2': 'BP', 'e2': 'BP', 'f2': 'BP', 'g2': 'BP', 'h2': 'BP',  
                            'a1': 'BR', 'b1': 'BH', 'c1': 'BB', 'd1': 'BQ', 'e1': 'BK', 'f1': 'BB', 'g1': 'BH', 'h1': 'BR'}
            request.session['cords_ancle'] = cords_ancle
            request.session['location_figur'] = location_figur
            filt_record.user2_id = curent_user
            filt_record.save()
            name1 = CustomUser.objects.get(id=user1)
            name2 = CustomUser.objects.get(id=curent_user)
            username_W = name1.username
            username_B = name2.username
            new_record = GameHistory.objects.create(user_W_id=user1,
                                                    username_W=username_W,
                                                    user_B_id=curent_user,
                                                    username_B=username_B,
                                                    result=0,
                                                    pin_game = pin_input,
                                                    dateTime=datetime.now(),
                                                    lenght_game=0)
            moves = ('1') * 16 + ('0') * 32 + ('1') * 16
            new_record = Steps.objects.create(pin_game=pin_input,
                                              queue_step=0,
                                              moves=moves,
                                              user_id_W=user1,
                                              user_id_B=curent_user,
                                              step=0,
                                              time=datetime.now())


            return redirect('Timer')
        else:
            data = {'message' : 'Комната заполнена или вы уже в ней!'}
            return render(request, 'LoginGame.html', context=data)
    else:
        data = {'message' : 'Такой игры не существует!'}
        return render(request, 'LoginGame.html', context=data)

    
@login_required
def DeskGame(request):
    min = request.GET.get('min')
    request.session['min']=min
    is_exists = SessionConnection.objects.filter(user1_id = request.user.id).exists()
    if is_exists:
        filt_record = SessionConnection.objects.get(user1_id = request.user.id)             
        pin = filt_record.pin_game
        data = {'pin' : pin, 'message':"У Вас уже имеется созданная игровая сессия, вот ее номер"} 
    else:
        desks = Desk.objects.all()
        data = {'desks':desks}
        return render(request, 'Desk.html', context=data)
         
    return render(request, 'Desk.html', context=data)



@login_required
def PINGame(request):
    min = request.session.get('min')
    data = list(Desk.objects.values_list('id', flat=True))
    if request.method == 'POST':
        if 'button' in request.POST:
            button_value = int(request.POST['button'])
        else:
             data = {'message':'Не выбран стол'}
             return render(request, 'PINGame.html', context=data)
    is_exists = SessionConnection.objects.filter(user1_id = request.user.id).exists()
    if is_exists:
        filt_record = SessionConnection.objects.get(user1_id = request.user.id)             
        pin = filt_record.pin_game
        data = {'pin' : pin, 'message':"У Вас уже имеется созданная игровая сессия, вот ее номер"} 
    else:
       
        random_number = generate_random_number()
        delete_time = datetime.now() + timedelta(seconds=15)
        new_record = SessionConnection.objects.create(pin_game=random_number, 
                                                        user1_id=request.user.id, 
                                                        user2_id=None, 
                                                        min = min,
                                                    #   sec = sec,
                                                        delete_time=delete_time,
                                                        desk = button_value,
                                                        cords_ancle=0)
        data = {'pin' : random_number}  
        return render(request, 'PINGame.html', context=data)

 