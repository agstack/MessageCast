# chat/urls.py
from django.urls import path

from . import views

urlpatterns = [
    path('', views.Chat.as_view(), name='index'),
    path('<str:room_name>/', views.room, name='room'),
]
