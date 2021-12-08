from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about-us/', views.about_us, name='about-us'),
    path('customer-feedback/', views.customer_feedback, name='customer-feedback'),
    path('future/', views.future, name='future'),
    path('weather-app/', views.weather_app, name='weather-app'),
    path('chat-bot/', views.chat_bot, name='chat-bot')
]
