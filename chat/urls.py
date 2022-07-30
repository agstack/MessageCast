# chat/urls.py
from django.urls import path

from api.views import ChatMessageView
from . import views

urlpatterns = [
    path('', views.Chat.as_view(), name='index'),
    path('<str:room_name>/', views.room, name='room'),
]
