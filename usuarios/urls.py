from django.urls import path
from .views import cadastro, logar, logar_home

urlpatterns = [
    path('', logar_home, name='logar_home'),
    path('logar/', logar, name='logar'),
    path('cadastro/', cadastro, name='cadastro'),
]
