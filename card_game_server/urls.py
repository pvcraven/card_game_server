"""card_game_server URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.urls import path
from .views import create_game_view
from .views import list_games
from .views import join_game_view
from .views import get_game_view
from .views import start_game_view
from .views import move_to_hold_view
from .views import move_to_pile_view
from .views import add_computer_player

urlpatterns = [
    path('admin/', admin.site.urls),
    path('create_game/', create_game_view, name='create_game'),
    path('join_game/', join_game_view, name='join_game'),
    path('list_games/', list_games, name='list_games'),
    path('get_game/', get_game_view, name='get_game'),
    path('start_game/', start_game_view, name='start_game'),
    path('move_to_hold/', move_to_hold_view, name='move_to_hold'),
    path('move_to_pile/', move_to_pile_view, name='move_to_pile'),
    path('add_computer_player/', add_computer_player, name='add_computer_player'),
]
