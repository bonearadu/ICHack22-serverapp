from . import views
from django.urls import path

urlpatterns = [
    path('start/', views.start, name='start'),
    path('register_player/', views.register_player, name='register_player'),
    path('login_player/', views.login_player, name='login_player'),
    path('player_get_target/', views.player_get_target, name='player_get_target'),
    path('player_scan/', views.player_scan, name='player_scan'),
    path('get_questions/', views.get_questions, name='get_questions'),
    path('user_score/', views.user_score, name='user_score'),
    path('score/', views.score, name='score'),
    path('reset/', views.reset, name='reset'),
    path('get_tasks/', views.get_tasks, name='get_tasks'),
]
