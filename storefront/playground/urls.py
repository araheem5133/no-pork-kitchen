from django.urls import path
from . import views

urlpatterns = [
    path('guest/', views.guest),
    path('chef/', views.chef),
    path('register/', views.register),
    path('login/', views.login),
    path('profile/', views.profile),
    path('food/', views.food),
    path('forum/', views.forum),
    path('menu/', views.menu),
    path('checkout/', views.checkout),
    path('home/', views.homepage),
    path('chefd/', views.chefd),
]