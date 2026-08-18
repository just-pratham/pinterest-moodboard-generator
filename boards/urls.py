from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('create/', views.create_moodboard, name='create_moodboard'),
    path('my-boards/', views.my_boards, name='my_boards'),
    path('boards/<int:board_id>/', views.moodboard_detail, name='moodboard_detail'),

]