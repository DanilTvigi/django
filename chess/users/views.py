from django.shortcuts import render, redirect

from users.models import SessionConnection, CustomUser
from main.models import GameHistory
from step.models import desk
from .forms import UserRegisterForm
from django.contrib.auth.decorators import login_required
from .forms import CustomLoginForm
from django.contrib.auth import authenticate, login
import random
from datetime import datetime, timedelta


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
    is_exists = SessionConnection.objects.filter(pin_game=pin_input).exists()
    if is_exists:
        filt_record = SessionConnection.objects.get(pin_game=pin_input)
        user1 = filt_record.user1_id
        user2 = filt_record.user2_id
        curent_user = request.user.id
        if user1 != curent_user and user2 == None and user2 != curent_user:
            filt_record.user2_id = curent_user
            filt_record.save()
            name1 = CustomUser.objects.get(id=user1)
            name2 = CustomUser.objects.get(id=curent_user)
            username_W = name1.username
            print(username_W)
            username_B = name2.username
            print(username_B)
            new_record = GameHistory.objects.create(user_W_id=user1,
                                                    username_W=username_W,
                                                    user_B_id=curent_user,
                                                    username_B=username_B,
                                                    result=0,
                                                    dateTime=datetime.now(),
                                                    lenght_game=0)
            return redirect('Timer')
        else:
            data = {'message' : 'Комната заполнена или вы уже в ней!'}
            return render(request, 'LoginGame.html', context=data)
    else:
        data = {'message' : 'Такой игры не существует!'}
        return render(request, 'LoginGame.html', context=data)

    


@login_required
def PINGame(request):
    min = request.GET.get('min')
    sec = request.GET.get('sec')
    # request.session['min'] = min
    # request.session['sec'] = sec 
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
                                                      sec = sec,
                                                      delete_time=delete_time)
        # data = {'pin' : random_number}  
        return redirect('Desk')
         
    return render(request, 'PINGame.html', context=data)

def Desk(request):
     return render(request, 'Desk.html')
 