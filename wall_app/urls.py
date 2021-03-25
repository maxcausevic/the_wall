from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('registration', views.registration),
    path('login', views.login),
    path('logout', views.logout),
    path('message', views.message),
    path('comment', views.comment),
    path('show_wall', views.show_wall)
]