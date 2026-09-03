from django.urls import path
from . import views

app_name = 'agentApp'

urlpatterns = [
    path('', views.chat, name='chat'),
]
