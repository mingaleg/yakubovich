from django.urls import path

from game.views import GameView, ShoutView, JoinView, StartView, LeadView, GuessView, StandingsView

urlpatterns = [
    path('standings/', StandingsView.as_view(), name="standings"),
    path('<uuid>/', GameView.as_view(), name="game"),
    path('<uuid>/shout/<chars>/', ShoutView.as_view(), name="shout"),
    path('<uuid>/join/', JoinView.as_view(), name="join"),
    path('<uuid>/lead/', LeadView.as_view(), name="lead"),
    path('<uuid>/start/', StartView.as_view(), name="start"),
    path('<uuid>/guess/', GuessView.as_view(), name="guess"),
]