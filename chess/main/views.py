from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from users.models import SessionConnection, CustomUser
from main.models import GameHistory

def Home(request):
    return render(request, 'Home.html')

def PlayerRating(request):
    users = CustomUser.objects.all()
    for user in users:
        filt_record = CustomUser.objects.get(username=user)
        username = filt_record.username
        win = filt_record.win
        lose = filt_record.lose
        if lose == 0:
            rating = 0
        else:
            rating = win / lose
        filt_record.rating = rating
        filt_record.save()
    users = CustomUser.objects.all().order_by('-rating')
    return render(request, 'PlayerRating.html',{'users':users})

def GameHistoryPage(request):
    games = GameHistory.objects.all()
    return render(request, 'GameHistoryPage.html', {'games':games})

def Timer(request):
    filt_record = SessionConnection.objects.get(user2_id = request.user.id)
    min = filt_record.min
    data = {'min':min}
    return render(request, 'Timer.html', context=data) 





    

