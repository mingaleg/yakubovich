"""yakubovich URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required


import game.urls
import tools.urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('game/', include(game.urls), name="game"),
    path('tools/', include(tools.urls), name="game"),
    path('login/', auth_views.login, name='login'),
    path('', TemplateView.as_view(template_name='yakubovich/index.html'), name="index"),
]
