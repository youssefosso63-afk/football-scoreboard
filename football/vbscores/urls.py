from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('setup/', views.match_setup, name='match_setup'),
    path('live-redirect/', views.live_redirect, name='live_redirect'),
    path('live/<int:team1_id>/<int:team2_id>/', views.live_match, name='live_match'),
    path('submit-score/', views.submit_score, name='submit_score'),
    path('mvp/', views.mvp_list, name='mvp_list'),
    path('schedule/', views.schedule_match, name='schedule_match'),
    path('matches/', views.upcoming_matches, name='upcoming_matches'),
    path('old/', views.played_matches, name='played_matches'),
]