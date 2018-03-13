from django.urls import path

from .views import EjContestView

urlpatterns = [
    path('ejcontest/<runid>', EjContestView.as_view(), name="ejcontest"),
]