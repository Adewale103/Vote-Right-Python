from django.urls import path
from .views import create_account,login

urlpatterns = [
    path('create-account/', create_account, name='create_account'),
    path('login/', login, name='login'),
]
