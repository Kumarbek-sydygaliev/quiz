from django.urls import path
from .views import (
    register, confirm, login
)

app_name = 'authe'

urlpatterns = [
    path('register/', register, name = 'register'),
    path('confirm/<str:code>', confirm, name = 'confirm'),
    path('login/', login, name = 'login')    
]