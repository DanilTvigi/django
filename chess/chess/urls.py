"""
URL configuration for chess project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))

"""
from django.contrib import admin
from django.urls import path, include, re_path
from main import views as main_views
from users import views as users_views
from step import views as step_views
from django.contrib.auth import views as auth_views
from django.conf import settings



urlpatterns = [
    # path("admin", admin.site.urls),
    path("", main_views.Home, name='Home'),
    path("PlayerRating", main_views.PlayerRating, name='PlayerRating'),
    path("GameHistoryPage", main_views.GameHistoryPage, name='GameHistory'),
    
    re_path(r"^Timer", main_views.Timer, name='Timer'),
    
    path("LoginGame", users_views.LoginGame, name='LoginGame'),
    path("PINGame", users_views.PINGame, name='PINGame'),
    re_path(r"^DeskGame",users_views.DeskGame, name='DeskGame'),
    path("Registration", users_views.Registration, name='Registration'),
    path("PersonalProfile?<int:id>", users_views.PersonalProfile, name='PersonalProfile'),
    path("PlayerProfile?<int:id>", users_views.PlayerProfile, name='PlayerProfile'),


    # path('Login', auth_views.LoginView.as_view(template_name='Login.html'), name='Login'),
    path('Login', users_views.Login, name='Login'),

    path('Logout', auth_views.LogoutView.as_view(template_name='Home.html'), name='Logout'),


    path('analyse', step_views.analyse, name='analyse'),
    # path('endGame', step_views.endGame, name='endGame')

    path("ViewGame?<int:pin>", step_views.ViewGame, name='ViewGame')
]

