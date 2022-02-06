from . import views
from django.urls import path

urlpatterns = [
    path('register_gm/', views.register_gm, name='register_gm'),
    path('gm_start/', views.gm_start, name='gm_start'),
    path('gm_stop/', views.gm_stop, name='gm_stop'),
    path('register_player/', views.register_player, name='register_player'),
    path('login_player/', views.login_player, name='login_player'),
    path('player_get_target/', views.player_get_target, name='player_get_target'),
    path('player_scan/', views.player_scan, name='player_scan'),
    path('get_questions/', views.get_questions, name='get_questions'),
    path('score/', views.score, name='score'),

]
