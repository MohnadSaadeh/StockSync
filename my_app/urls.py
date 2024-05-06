
from django.urls import path
from . import views

urlpatterns = [
    
    path('', views.display_homepage),
    path('index', views.index),
    path('signup', views.sign_up),

    path('signin', views.sign_in),


]